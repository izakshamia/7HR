import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def execute_sql(sql):
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
            json={"query": sql}
        )
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": response.text}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

def update_table_structure():
    """Update the cv_profiles table structure"""
    try:
        # SQL to alter the table
        sql_commands = [
            # Add updated_at column if it doesn't exist
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'cv_profiles' AND column_name = 'updated_at'
                ) THEN
                    ALTER TABLE public.cv_profiles 
                    ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
                END IF;
            END $$;
            """,
            # Add source column if it doesn't exist
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'cv_profiles' AND column_name = 'source'
                ) THEN
                    ALTER TABLE public.cv_profiles 
                    ADD COLUMN source TEXT DEFAULT 'unknown';
                END IF;
            END $$;
            """,
            # Add source_file_name column if it doesn't exist
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'cv_profiles' AND column_name = 'source_file_name'
                ) THEN
                    ALTER TABLE public.cv_profiles 
                    ADD COLUMN source_file_name TEXT;
                END IF;
            END $$;
            """,
            # Convert data column to JSONB if it's not already
            """
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'cv_profiles' 
                    AND column_name = 'data' 
                    AND data_type != 'jsonb'
                ) THEN
                    ALTER TABLE public.cv_profiles 
                    ALTER COLUMN data TYPE JSONB USING data::jsonb;
                END IF;
            END $$;
            """
        ]
        
        # Execute each SQL command
        for i, sql in enumerate(sql_commands, 1):
            print(f"Executing command {i}...")
            result = execute_sql(sql)
            
            if not result["success"]:
                print(f"Error executing command {i}: {result.get('error', 'Unknown error')}")
                return False
            
            print(f"Command {i} executed successfully!")
        
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
