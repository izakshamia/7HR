from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def update_table_structure():
    try:
        # Initialize Supabase client
        supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        )
        
        # Check current columns
        response = supabase.table('cv_profiles').select('*').limit(1).execute()
        
        if not hasattr(response, 'data') or not response.data:
            print("No data in the table. Cannot determine structure.")
            return False
            
        current_columns = set(response.data[0].keys())
        print(f"Current columns: {', '.join(current_columns)}")
        
        # Add missing columns
        columns_to_add = {
            'updated_at': 'TIMESTAMP WITH TIME ZONE DEFAULT NOW()',
            'source': 'TEXT DEFAULT \'unknown\'',
            'source_file_name': 'TEXT'
        }
        
        for column, data_type in columns_to_add.items():
            if column not in current_columns:
                print(f"Adding column: {column} {data_type}")
                # Use the Supabase RPC to execute raw SQL
                sql = f"ALTER TABLE public.cv_profiles ADD COLUMN {column} {data_type};"
                result = supabase.rpc('execute_sql', {'query': sql}).execute()
                
                if hasattr(result, 'error') and result.error:
                    print(f"Error adding column {column}: {result.error}")
                    return False
                
                print(f"Successfully added column: {column}")
            else:
                print(f"Column already exists: {column}")
        
        # Convert data column to JSONB if needed
        if 'data' in current_columns:
            print("Checking data column type...")
            sql = """
            SELECT data_type 
            FROM information_schema.columns 
            WHERE table_name = 'cv_profiles' 
            AND column_name = 'data';
            """
            result = supabase.rpc('execute_sql', {'query': sql}).execute()
            
            if hasattr(result, 'data') and result.data:
                data_type = result.data[0].get('data_type')
                if data_type != 'jsonb':
                    print("Converting data column to JSONB...")
                    sql = """
                    ALTER TABLE public.cv_profiles 
                    ALTER COLUMN data TYPE JSONB USING data::jsonb;
                    """
                    result = supabase.rpc('execute_sql', {'query': sql}).execute()
                    if hasattr(result, 'error') and result.error:
                        print(f"Error converting data column: {result.error}")
                    else:
                        print("Successfully converted data column to JSONB")
                else:
                    print("Data column is already JSONB")
        
        return True
        
    except Exception as e:
        print(f"Error updating table structure: {e}")
        return False

if __name__ == "__main__":
    print("Updating Supabase table structure...")
    if update_table_structure():
        print("\nTable structure updated successfully!")
        print("\nPlease verify the table structure in the Supabase dashboard.")
    else:
        print("\nFailed to update table structure. Please check the error messages above.")
