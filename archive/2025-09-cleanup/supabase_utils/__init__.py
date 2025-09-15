"""
Supabase utilities and migration tools.

This package contains all the necessary tools to work with Supabase,
including database migrations, schema verification, and data updates.
"""

# Import only what's needed to avoid circular imports
from .utils.client import get_supabase_client as get_client

__all__ = ['get_client']
