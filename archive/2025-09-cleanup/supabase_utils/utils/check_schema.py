import os
from dotenv import load_dotenv
from .client import get_supabase_client

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = get_supabase_client()

def check_table_structure():
    try:
        # Get table information
        response = supabase.table('cv_profiles').select("*").limit(1).execute()
        
        if hasattr(response, 'data') and response.data:
            print("\nTable structure:")
            print("-" * 50)
            for key, value in response.data[0].items():
                print(f"{key}: {type(value).__name__}")
            
            # Check for required columns
            required_columns = ['id', 'created_at', 'updated_at', 'source', 'source_file_name', 'data']
            missing_columns = [col for col in required_columns if col not in response.data[0]]
            
            if missing_columns:
                print("\nMissing columns:", ", ".join(missing_columns))
            else:
                print("\nAll required columns are present.")
                
        else:
            print("No data in the table or error occurred.")
            
    except Exception as e:
        print(f"Error checking table structure: {e}")

if __name__ == "__main__":
    print("Checking Supabase table structure...")
    check_table_structure()
