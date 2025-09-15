import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Source database configuration
source_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

def get_table_columns():
    """Fetch column information from the cv_profiles table"""
    try:
        conn = psycopg2.connect(**source_config)
        cursor = conn.cursor()
        
        # Get column information
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'cv_profiles'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        
        print("\nColumns in cv_profiles table:")
        print("-" * 80)
        print(f"{'Column Name':<20} | {'Data Type':<20} | {'Nullable':<10} | {'Default'}")
        print("-" * 80)
        
        for col in columns:
            column_name, data_type, is_nullable, column_default = col
            print(f"{column_name:<20} | {data_type:<20} | {is_nullable:<10} | {column_default}")
        
        # Get sample data to understand the structure
        cursor.execute("SELECT * FROM cv_profiles LIMIT 1;")
        if cursor.rowcount > 0:
            sample = cursor.fetchone()
            col_names = [desc[0] for desc in cursor.description]
            
            print("\nSample data structure:")
            print("-" * 40)
            for name, value in zip(col_names, sample):
                print(f"{name}: {type(value).__name__} = {value}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    get_table_columns()
