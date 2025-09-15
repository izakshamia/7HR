from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

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
            required_columns = ['id', 'created_at', 'data']
            optional_columns = ['updated_at', 'source', 'source_file_name']
            
            print("\nRequired columns:")
            for col in required_columns:
                exists = col in response.data[0]
                print(f"- {col}: {'✅' if exists else '❌'}")
                
            print("\nOptional columns:")
            for col in optional_columns:
                exists = col in response.data[0]
                print(f"- {col}: {'✅' if exists else '❌'}")
                
        else:
            print("No data in the table.")
            
    except Exception as e:
        print(f"Error checking table structure: {e}")

def count_records():
    try:
        response = supabase.table('cv_profiles').select('*', count='exact').execute()
        count = len(response.data) if hasattr(response, 'data') else 0
        print(f"\nTotal records in cv_profiles: {count}")
        return count
    except Exception as e:
        print(f"Error counting records: {e}")
        return 0

if __name__ == "__main__":
    print("Verifying Supabase table...")
    check_table_structure()
    count_records()
