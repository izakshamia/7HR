import psycopg2
import os
from contextlib import contextmanager

class Database:
    def __init__(self, db_config):
        self.db_config = db_config

    @contextmanager
    def db_connection(self):
        conn = None
        try:
            conn = psycopg2.connect(**self.db_config)
            yield conn
        finally:
            if conn:
                conn.close()

    def fetch_new_candidates(self, last_sent_id):
        with self.db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, data FROM cv_profiles WHERE id > %s ORDER BY id ASC;", (last_sent_id,))
                rows = cur.fetchall()
            return rows

    def fetch_candidate_by_id(self, candidate_id):
        with self.db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT data FROM cv_profiles WHERE id = %s;", (candidate_id,))
                row = cur.fetchone()
                if row:
                    return row[0]
                return None

    def get_adjacent_candidate_ids(self, current_id):
        with self.db_connection() as conn:
            with conn.cursor() as cur:
                # Get previous candidate ID
                cur.execute("""
                    SELECT id FROM cv_profiles 
                    WHERE id < %s 
                    ORDER BY id DESC 
                    LIMIT 1;
                """, (current_id,))
                prev_id = cur.fetchone()
                
                # Get next candidate ID
                cur.execute("""
                    SELECT id FROM cv_profiles 
                    WHERE id > %s 
                    ORDER BY id ASC 
                    LIMIT 1;
                """, (current_id,))
                next_id = cur.fetchone()
                
                return {
                    'prev': f"/candidate/{prev_id[0]}" if prev_id else None,
                    'next': f"/candidate/{next_id[0]}" if next_id else None
                }

    def fetch_all_candidates(self, limit=10):
        with self.db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT DISTINCT ON (data->'candidate'->>'fullName') id, data 
                    FROM cv_profiles 
                    ORDER BY data->'candidate'->>'fullName', id
                    LIMIT %s;
                """, (limit,))
                rows = cur.fetchall()
            return rows

    def fetch_all_candidates_with_details(self):
        with self.db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, data FROM cv_profiles ORDER BY id ASC;")
                rows = cur.fetchall()
            
            formatted_rows = []
            for row_id, data in rows:
                # Ensure data is a dictionary and has expected nested structures
                if not isinstance(data, dict):
                    data = {}
                
                candidate_data = data.get('candidate', {})
                skills_data = data.get('skills', [])

                # Provide default values for missing fields
                formatted_data = {
                    'candidate': {
                        'fullName': candidate_data.get('fullName', 'N/A'),
                        'primaryProfession': candidate_data.get('primaryProfession', 'N/A'),
                        'location': candidate_data.get('location', 'N/A'),
                        'seniority': candidate_data.get('seniority', 'N/A'),
                        'department': candidate_data.get('department', 'N/A'),
                    },
                    'skills': skills_data, # Skills are handled in the frontend render function
                    # Add other top-level keys if necessary
                }
                formatted_rows.append([row_id, formatted_data])
            return formatted_rows

    def fetch_all_jobs(self):
        with self.db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT data->'candidate'->>'primaryProfession' FROM cv_profiles;")
                rows = cur.fetchall()
            return [row[0] for row in rows]

    def remove_duplicates(self):
        with self.db_connection() as conn:
            with conn.cursor() as cur:
                delete_query = """
                    DELETE FROM cv_profiles
                    WHERE id IN (
                        SELECT id
                        FROM (
                            SELECT
                                id,
                                (data->'candidate'->>'fullName') AS full_name,
                                ROW_NUMBER() OVER(PARTITION BY (data->'candidate'->>'fullName') ORDER BY id) as rn
                            FROM cv_profiles
                        ) AS subquery
                        WHERE rn > 1
                    );
                """
                cur.execute(delete_query)
                conn.commit()
                print(f"Removed {cur.rowcount} duplicate entries.")