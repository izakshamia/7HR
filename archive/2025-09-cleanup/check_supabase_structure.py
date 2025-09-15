#!/usr/bin/env python3
"""
Standalone script to check Supabase table structure.
"""

import os
from supabase import create_client
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Get Supabase credentials
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not supabase_key:
        print("Error: Missing Supabase URL or API key in environment variables")
        return
    
    try:
        # Initialize Supabase client
        supabase = create_client(supabase_url, supabase_key)
        
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
                
            # Count total records
            count_response = supabase.table('cv_profiles').select('*', count='exact').execute()
            count = len(count_response.data) if hasattr(count_response, 'data') else 0
            print(f"\nTotal records in cv_profiles: {count}")
            
            # Show sample data
            print("\nSample record:")
            print("-" * 50)
            for key, value in response.data[0].items():
                print(f"{key}: {value}")
            
        else:
            print("No data in the table.")
            
    except Exception as e:
        print(f"Error checking table structure: {e}")

if __name__ == "__main__":
    main()
