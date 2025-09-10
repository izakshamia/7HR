from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def update_records():
    try:
        # Initialize Supabase client
        supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        )
        
        # Get all records to update
        response = supabase.table('cv_profiles').select('*').execute()
        
        if not hasattr(response, 'data') or not response.data:
            print("No records found in the table.")
            return False
            
        records = response.data
        print(f"Found {len(records)} records to update...")
        
        # Update each record with the correct source and source_file_name
        for record in records:
            record_id = record.get('id')
            
            # Skip if already updated
            if record.get('source') != 'unknown' or record.get('source_file_name'):
                continue
                
            # Update the record
            update_data = {
                'source': 'telegram',
                'source_file_name': f"cv_{record_id}.pdf"
            }
            
            result = supabase.table('cv_profiles').update(update_data).eq('id', record_id).execute()
            
            if hasattr(result, 'error') and result.error:
                print(f"Error updating record {record_id}: {result.error}")
            else:
                print(f"Updated record {record_id}")
        
        print("\nUpdate completed!")
        return True
        
    except Exception as e:
        print(f"Error updating records: {e}")
        return False

if __name__ == "__main__":
    print("Updating Supabase records with source information...")
    if update_records():
        print("\nRecords updated successfully!")
        print("\nYou can verify the updates in the Supabase dashboard.")
    else:
        print("\nFailed to update records. Please check the error messages above.")
