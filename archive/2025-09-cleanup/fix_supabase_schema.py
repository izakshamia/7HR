import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def execute_sql(query):
    """Execute SQL using Supabase REST API"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}'
        }
        
        # Use the SQL endpoint to execute raw SQL
        sql_url = f"{SUPABASE_URL}/rest/v1/rpc/execute_sql"
        
        response = requests.post(
            sql_url,
            headers=headers,
            json={"query": query}
        )
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": response.text}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

def add_missing_columns():
    """Add missing columns to the cv_profiles table"""
    try:
        # SQL to add missing columns if they don't exist
        sql_commands = [
            """
            DO $$
            BEGIN
                -- Add updated_at if it doesn't exist
                IF NOT EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'cv_profiles' AND column_name = 'updated_at'
                ) THEN
                    ALTER TABLE cv_profiles 
                    ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
                END IF;
                
                -- Add source if it doesn't exist
                IF NOT EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'cv_profiles' AND column_name = 'source'
                ) THEN
                    ALTER TABLE cv_profiles 
                    ADD COLUMN source VARCHAR NOT NULL DEFAULT 'unknown';
                END IF;
                
                -- Add source_file_name if it doesn't exist
                IF NOT EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'cv_profiles' AND column_name = 'source_file_name'
                ) THEN
                    ALTER TABLE cv_profiles 
                    ADD COLUMN source_file_name VARCHAR;
                END IF;
                
                -- Convert data to JSONB if it's not already
                IF EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'cv_profiles' 
                    AND column_name = 'data' 
                    AND data_type != 'jsonb'
                ) THEN
                    ALTER TABLE cv_profiles 
                    ALTER COLUMN data TYPE JSONB USING data::jsonb;
                END IF;
            END $$;
            """
        ]
        
        # Execute each SQL command
        for sql in sql_commands:
            print("Executing SQL...")
            result = execute_sql(sql)
            
            if not result["success"]:
                print(f"Error executing SQL: {result.get('error', 'Unknown error')}")
                return False
            
            print("Schema update completed successfully!")
            return True
            
    except Exception as e:
        print(f"Error updating schema: {e}")
        return False

if __name__ == "__main__":
    print("Updating Supabase table schema...")
    if add_missing_columns():
        print("Schema update completed successfully!")
    else:
        print("Failed to update schema. Please check the error messages above.")
