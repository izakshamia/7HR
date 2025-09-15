"""
Supabase client initialization and configuration.

This module provides a function to initialize and return a Supabase client
with the appropriate credentials from environment variables.
"""

import os
from supabase import create_client as create_supabase_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_supabase_client():
    """
    Initialize and return a Supabase client.
    
    Returns:
        A configured Supabase client instance.
        
    Raises:
        ValueError: If required environment variables are missing.
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError(
            "Missing Supabase URL or API key in environment variables. "
            "Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY."
        )
    
    return create_supabase_client(supabase_url, supabase_key)
