import sys
import os
import psycopg2

# Add the server directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'server')))

import config

def create_indexes():
    conn = None
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(**config.DB_CONFIG)
        cur = conn.cursor()
        print("Database connection established. Creating indexes...")

        # Create index on 'id' column
        cur.execute("CREATE INDEX IF NOT EXISTS idx_cv_profiles_id ON cv_profiles (id);")
        print("Index 'idx_cv_profiles_id' created or already exists.")

        # Enable pg_trgm extension for better text search
        cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
        
        # Create GIN index on 'data->'candidate'->>'fullName' using gin_trgm_ops
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_cv_profiles_full_name 
            ON cv_profiles USING GIN ((data->'candidate'->>'fullName') gin_trgm_ops);
        """)
        print("GIN Index 'idx_cv_profiles_full_name' created or already exists.")
        
        # Create a functional index for case-insensitive search
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_cv_profiles_full_name_lower 
            ON cv_profiles USING GIN (LOWER(data->'candidate'->>'fullName') gin_trgm_ops);
        """)
        print("GIN Index 'idx_cv_profiles_full_name_lower' created or already exists.")

        conn.commit()
        print("Indexes created successfully.")

    except Exception as e:
        print(f"An error occurred during index creation: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    create_indexes()
