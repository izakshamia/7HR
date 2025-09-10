# Supabase Utilities

This directory contains all the necessary tools and scripts for working with Supabase in the Telegram CV Bot project.

## Directory Structure

```
supabase/
├── __init__.py          # Package initialization
├── README.md            # This file
├── migrations/          # Database migration scripts
│   ├── __init__.py
│   ├── 001_initial_migration.py
│   ├── 002_update_columns.py
│   └── 003_update_data.py
└── utils/               # Utility modules
    ├── __init__.py
    ├── client.py        # Supabase client initialization
    ├── check_schema.py  # Schema verification
    └── verify.py        # Data verification
```

## Getting Started

1. **Prerequisites**:
   - Python 3.8+
   - Required packages (install via `pip install -r requirements.txt`)
   - Environment variables set in `.env` file

2. **Environment Variables**:
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_SERVICE_ROLE_KEY`: Your Supabase service role key
   - `DB_*`: Database connection variables for the source database

## Available Commands

### Run Migrations

Migrations should be run in order:

```bash
# Run all migrations
python -m supabase.migrations.001_initial_migration
python -m supabase.migrations.002_update_columns
python -m supabase.migrations.003_update_data
```

### Verify Database

```bash
# Check database schema
python -m supabase.utils.check_schema

# Verify data
python -m supabase.utils.verify
```

## Development

When adding new migrations:
1. Create a new file in `migrations/` with the next sequential number
2. Update the `__all__` list in `migrations/__init__.py`
3. Test the migration thoroughly before committing

## Best Practices

- Always back up your database before running migrations
- Test migrations in a development environment first
- Document any schema changes in the migration files
- Keep migration scripts idempotent (safe to run multiple times)
