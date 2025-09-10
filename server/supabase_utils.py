from supabase import create_client, Client
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseDB:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        if not self.url or not self.key:
            raise ValueError("Missing Supabase URL or API key in environment variables")
        self.client: Client = create_client(self.url, self.key)

    async def fetch_new_candidates(self, last_sent_id: int) -> List[Dict]:
        """Fetch candidates with IDs greater than last_sent_id"""
        response = self.client.table('cv_profiles') \
            .select('*') \
            .gt('id', last_sent_id) \
            .order('id', desc=False) \
            .execute()
        return response.data if hasattr(response, 'data') else []

    async def fetch_candidate_by_id(self, candidate_id: int) -> Optional[Dict]:
        """Fetch a single candidate by ID"""
        response = self.client.table('cv_profiles') \
            .select('*') \
            .eq('id', candidate_id) \
            .single() \
            .execute()
        return response.data if hasattr(response, 'data') else None

    async def get_adjacent_candidate_ids(self, current_id: int) -> Dict[str, Optional[str]]:
        """Get the previous and next candidate IDs relative to current_id"""
        # Get previous candidate ID
        prev_response = self.client.table('cv_profiles') \
            .select('id') \
            .lt('id', current_id) \
            .order('id', desc=True) \
            .limit(1) \
            .execute()
        
        # Get next candidate ID
        next_response = self.client.table('cv_profiles') \
            .select('id') \
            .gt('id', current_id) \
            .order('id', desc=False) \
            .limit(1) \
            .execute()
        
        return {
            'prev': f"/candidate/{prev_response.data[0]['id']}" if prev_response.data else None,
            'next': f"/candidate/{next_response.data[0]['id']}" if next_response.data else None
        }

    async def fetch_all_candidates(self, limit: int = 10) -> List[Dict]:
        """Fetch all candidates with distinct full names"""
        # Note: This is a simplified implementation. 
        # For distinct names, you might need to adjust based on your exact requirements
        response = self.client.table('cv_profiles') \
            .select('*') \
            .order('data->>fullName') \
            .limit(limit) \
            .execute()
        return response.data if hasattr(response, 'data') else []

    async def fetch_all_candidates_with_details(self) -> List[List]:
        """Fetch all candidates with formatted details"""
        response = self.client.table('cv_profiles') \
            .select('*') \
            .order('id') \
            .execute()
        
        formatted_rows = []
        for row in response.data if hasattr(response, 'data') else []:
            candidate_data = row.get('data', {}).get('candidate', {})
            skills_data = row.get('data', {}).get('skills', [])

            formatted_data = {
                'candidate': {
                    'fullName': candidate_data.get('fullName', 'N/A'),
                    'primaryProfession': candidate_data.get('primaryProfession', 'N/A'),
                    'location': candidate_data.get('location', 'N/A'),
                    'seniority': candidate_data.get('seniority', 'N/A'),
                    'department': candidate_data.get('department', 'N/A'),
                },
                'skills': skills_data,
            }
            formatted_rows.append([row['id'], formatted_data])
        
        return formatted_rows

    async def fetch_all_jobs(self) -> List[str]:
        """Fetch all unique job titles"""
        response = self.client.table('cv_profiles') \
            .select('data->candidate->>primaryProfession') \
            .execute()
        
        # Extract unique job titles
        jobs = set()
        for item in response.data if hasattr(response, 'data') else []:
            if 'primaryProfession' in item and item['primaryProfession']:
                jobs.add(item['primaryProfession'])
        
        return list(jobs)

    async def remove_duplicates(self) -> int:
        """Remove duplicate candidates based on full name"""
        # This is a placeholder implementation
        # In a real scenario, you would need to implement deduplication logic
        # that matches your specific requirements
        print("Deduplication would be performed here")
        return 0
