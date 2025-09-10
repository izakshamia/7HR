# Supabase Setup Guide

This guide will help you set up Supabase for your application.

## 1. Create a Supabase Project

1. Go to [Supabase](https://supabase.com/) and sign up/log in
2. Click "New Project"
3. Choose a name for your project and set a secure database password
4. Select a region close to your users for better performance
5. Click "Create new project"

## 2. Set Up Database Schema

1. In the Supabase dashboard, go to the Table Editor
2. Create a new table called `cv_profiles` with the following columns:
   - `id` (bigint, primary key, auto-increment)
   - `data` (jsonb, not null)
   - `created_at` (timestamp with time zone, default: now())

3. Click "Save" to create the table

## 3. Configure Row Level Security (RLS)

1. Go to Authentication > Policies
2. Click "New Policy" on the `cv_profiles` table
3. Select "Create a policy from scratch"
4. Name it "Enable read access for all users"
5. Use this SQL (adjust as needed for your security requirements):
   ```sql
   CREATE POLICY "Enable read access for all users" 
   ON public.cv_profiles 
   FOR SELECT 
   USING (true);
   ```
6. Click "Review" and then "Create policy"

## 4. Get API Keys

1. Go to Project Settings (gear icon) > API
2. Note down:
   - Project URL (SUPABASE_URL)
   - anon/public key (SUPABASE_KEY)

## 5. Set Up Environment Variables

Create or update your `.env` file with:

```env
SUPABASE_URL=your_project_url_here
SUPABASE_KEY=your_anon_public_key_here
```

## 6. Import Data (if needed)

If you need to import existing data:

1. Go to Table Editor > `cv_profiles`
2. Click "Import data" and upload your data in CSV or JSON format
3. Map the columns appropriately

## 7. Update Application Code

The `supabase_utils.py` file has been created with methods that match your existing database interface. You'll need to update your application to use the Supabase client instead of the direct PostgreSQL connection.

## 8. Deploy to Vercel

Make sure to add the Supabase environment variables to your Vercel project:

1. Go to your Vercel project settings
2. Navigate to Environment Variables
3. Add:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

## 9. Testing

Test your application thoroughly to ensure all database operations work as expected with Supabase.
