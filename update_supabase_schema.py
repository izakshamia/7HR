from supabase import create_client
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def execute_sql(query):
    """Execute SQL using Supabase REST API"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}'
        }
        
        # Use the SQL endpoint to execute raw SQL
        sql_url = f"{supabase_url}/rest/v1/rpc/execute_sql"
        
        response = requests.post(
            sql_url,
            headers=headers,
            json={"query": query}
        )
        
        if response.status_code == 200:
            return {"data": response.json(), "error": None}
        else:
            return {"data": None, "error": response.text}
            
    except Exception as e:
        return {"data": None, "error": str(e)}

def update_supabase_schema():
    try:
        # SQL commands to alter the table
        sql_commands = [
            # First, add the new columns if they don't exist
            """
            DO $$
            BEGIN
                -- Add updated_at if it doesn't exist
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='cv_profiles' AND column_name='updated_at') THEN
                    ALTER TABLE cv_profiles 
                    ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
                END IF;
                
                -- Add source if it doesn't exist
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='cv_profiles' AND column_name='source') THEN
                    ALTER TABLE cv_profiles 
                    ADD COLUMN source VARCHAR NOT NULL DEFAULT 'unknown';
                END IF;
                
                -- Add source_file_name if it doesn't exist
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                              WHERE table_name='cv_profiles' AND column_name='source_file_name') THEN
                    ALTER TABLE cv_profiles 
                    ADD COLUMN source_file_name VARCHAR;
                END IF;
                
                -- Convert data to JSONB if it's not already
                IF EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='cv_profiles' AND column_name='data' 
                          AND data_type != 'jsonb') THEN
                    ALTER TABLE cv_profiles 
                    ALTER COLUMN data TYPE JSONB USING data::jsonb;
                END IF;
                
                -- Change id type to INTEGER if it's not already
                IF EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='cv_profiles' AND column_name='id' 
                          AND data_type != 'integer') THEN
                    -- We need to drop and recreate the primary key constraint first
                    ALTER TABLE cv_profiles 
                    DROP CONSTRAINT IF EXISTS cv_profiles_pkey;
                    
                    -- Change the column type
                    ALTER TABLE cv_profiles 
                    ALTER COLUMN id TYPE INTEGER;
                    
                    -- Recreate the primary key constraint
                    ALTER TABLE cv_profiles 
                    ADD PRIMARY KEY (id);
                END IF;
            END $$;
            """
        ]
        
        # Execute each SQL command
        for sql in sql_commands:
            try:
                print("Executing schema updates...")
                result = execute_sql(sql)
                
                if result["error"]:
                    print(f"Error executing SQL: {result['error']}")
                else:
                    print("Schema updates completed successfully!")
                    
            except Exception as e:
                print(f"Error: {e}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Updating Supabase table schema...")
    update_supabase_schema()
    print("Done!")
