import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from supabase.utils.client import get_supabase_client

# Load environment variables
load_dotenv()

# Source database configuration (your current database)
source_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

# Supabase configuration
supabase_url = os.getenv("SUPABASE_URL")
# Use service role key for bypassing RLS
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase = get_supabase_client()

if not supabase_key or not supabase_url:
    print("Error: Missing Supabase URL or API key in environment variables")
    print("Please make sure to set SUPABASE_URL and either SUPABASE_KEY or SUPABASE_SERVICE_ROLE_KEY")
    exit(1)

def get_source_data():
    """Fetch data from the source database"""
    try:
        conn = psycopg2.connect(**source_config)
        cursor = conn.cursor()
        
        # Fetch data from cv_profiles table with all columns
        cursor.execute("""
            SELECT id, created_at, updated_at, source, source_file_name, data
            FROM cv_profiles 
            ORDER BY id
        """)
        
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        # Convert rows to list of dictionaries and handle datetime serialization
        data = []
        for row in rows:
            row_dict = {}
            for i, value in enumerate(row):
                column_name = columns[i]
                # Skip None values to use database defaults
                if value is None:
                    continue
                    
                # Convert datetime objects to ISO format strings
                if hasattr(value, 'isoformat'):
                    row_dict[column_name] = value.isoformat()
                # Convert JSON/JSONB to dict if it's a string
                elif column_name == 'data' and isinstance(value, str):
                    try:
                        row_dict[column_name] = json.loads(value)
                    except json.JSONDecodeError:
                        row_dict[column_name] = value
                else:
                    row_dict[column_name] = value
            data.append(row_dict)
            
        return data
        
    except Exception as e:
        print(f"Error fetching data from source database: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def insert_into_supabase(data):
    """Insert data into Supabase"""
    try:
        
        # Get existing IDs to avoid duplicates
        existing_ids = set()
        response = supabase.table('cv_profiles').select('id').execute()
        if hasattr(response, 'data'):
            existing_ids = {str(item['id']) for item in response.data}
        
        # Filter out existing records
        new_data = [item for item in data if str(item.get('id')) not in existing_ids]
        
        if not new_data:
            print("No new records to insert. All records already exist in Supabase.")
            return True
            
        print(f"Found {len(new_data)} new records to insert out of {len(data)} total records.")
        
        # Insert data in smaller batches to avoid timeouts
        batch_size = 20
        success_count = 0
        
        for i in range(0, len(new_data), batch_size):
            batch = new_data[i:i + batch_size]
            try:
                # For each record, insert or update
                for record in batch:
                    # Ensure we only include fields that exist in the table
                    clean_record = {
                        'id': record.get('id'),
                        'data': record.get('data', {}),
                        'created_at': record.get('created_at')
                    }
                    
                    # Add optional fields if they exist in the source data
                    if 'source' in record:
                        clean_record['source'] = record['source']
                    if 'source_file_name' in record:
                        clean_record['source_file_name'] = record['source_file_name']
                    if 'updated_at' in record:
                        clean_record['updated_at'] = record['updated_at']
                    
                    # Use upsert to handle both insert and update
                    response = supabase.table('cv_profiles').upsert(
                        clean_record,
                        on_conflict='id'
                    ).execute()
                    
                    if hasattr(response, 'error') and response.error:
                        print(f"Error with record ID {record.get('id')}: {response.error}")
                    else:
                        success_count += 1
                        if success_count % 10 == 0:
                            print(f"Processed {success_count}/{len(new_data)} records...")
                
            except Exception as e:
                print(f"Error processing batch {i//batch_size + 1}: {e}")
                print(f"Problematic batch: {batch}")
        
        print(f"Successfully processed {success_count} out of {len(new_data)} new records.")
        return success_count == len(new_data)           
            
        
    except Exception as e:
        print(f"Error inserting data into Supabase: {e}")
        return False

def main():
    print("Starting data migration to Supabase...")
    
    # Step 1: Fetch data from source database
    print("Fetching data from source database...")
    data = get_source_data()
    
    if not data:
        print("No data found in source database or error occurred.")
        return
    
    print(f"Found {len(data)} records to migrate.")
    
    # Show a sample of the data being migrated
    print("\nSample record to be migrated:")
    import pprint
    pprint.pprint(data[0] if len(data) > 0 else {})
    
    # Ask for confirmation before proceeding
    confirm = input("\nDo you want to proceed with the migration? (y/n): ")
    if confirm.lower() != 'y':
        print("Migration cancelled by user.")
        return
    
    # Step 2: Insert data into Supabase
    print("\nStarting data insertion into Supabase...")
    success = insert_into_supabase(data)
    
    if success:
        print("\nMigration completed successfully!")
        print(f"Migrated {len(data)} records to Supabase.")
    else:
        print("\nMigration failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
