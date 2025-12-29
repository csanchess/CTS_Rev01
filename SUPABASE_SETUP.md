# Supabase Setup Guide - Step by Step

Since you already have a Supabase account, follow these steps:

## Step 1: Create a New Project (or Use Existing)

1. Go to https://supabase.com/dashboard
2. Click **"New Project"** (or select an existing project if you prefer)
3. Fill in the project details:
   - **Name**: e.g., "Cybersecurity Intelligence Platform" or "CTS"
   - **Database Password**: Create a strong password (save this!)
   - **Region**: Choose the closest region to you
   - **Pricing Plan**: Free tier is fine for development
4. Click **"Create new project"**
5. Wait 1-2 minutes for the project to initialize

## Step 2: Get Your API Keys

1. In your Supabase dashboard, go to **Settings** (gear icon in left sidebar)
2. Click on **"API"** in the settings menu
3. You'll see several important values:

   **Project URL**: 
   - Look for "Project URL" - it looks like: `https://xxxxxxxxxxxxx.supabase.co`
   - Copy this value

   **anon/public key**: 
   - Look for "Project API keys" section
   - Find the `anon` `public` key (starts with `eyJ...`)
   - Click the eye icon to reveal it, then copy it

   **service_role key**:
   - In the same "Project API keys" section
   - Find the `service_role` `secret` key (also starts with `eyJ...`)
   - ⚠️ **WARNING**: This key has admin privileges - keep it secret!
   - Click the eye icon to reveal it, then copy it

4. Save these three values somewhere safe - you'll need them in Step 4

## Step 3: Run the Database Schema

1. In your Supabase dashboard, go to **SQL Editor** (left sidebar)
2. Click **"New query"** button (or the + icon)
3. Open the file `supabase/schema.sql` from this project in a text editor
4. Copy **ALL** the contents of that file (Ctrl+A, Ctrl+C)
5. Paste it into the SQL Editor in Supabase (Ctrl+V)
6. Click **"Run"** button (or press Ctrl+Enter)
7. You should see a success message: "Success. No rows returned"
8. ✅ If you see errors, let me know and I'll help troubleshoot

## Step 4: Create Your .env File

1. In your project root directory (`CTS_Rev01`), create a file named `.env`
   - **Note**: On Windows, you might need to create it as `.env.` (with a dot at the end) or use a code editor

2. Open the `.env` file and paste this template:

```env
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=your_project_url_here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
API_URL=http://localhost:8000

# OpenAI (optional - for enhanced AI capabilities)
OPENAI_API_KEY=

# Redis (optional - for background tasks)
REDIS_URL=redis://localhost:6379/0
```

3. Replace the placeholder values:
   - `your_project_url_here` → Your Project URL from Step 2
   - `your_anon_key_here` → Your anon/public key from Step 2
   - `your_service_role_key_here` → Your service_role key from Step 2

4. Save the file

**Example of what it should look like:**
```env
NEXT_PUBLIC_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzODk4NzY1MCwiZXhwIjoxOTU0NTYzNjUwfQ.example...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjM4OTg3NjUwLCJleHAiOjE5NTQ1NjM2NTB9.example...
```

## Step 5: Verify the Setup

1. Go back to Supabase dashboard
2. Click on **"Table Editor"** in the left sidebar
3. You should see all the tables we created:
   - `users`
   - `organizations`
   - `individuals`
   - `transactions`
   - `threats`
   - `incidents`
   - `agents`
   - `sanctions_entries`
   - And more...
4. ✅ If you see all these tables, the schema was created successfully!

## Troubleshooting

### "Relation already exists" errors
- This means some tables already exist. You can either:
  - Delete the existing tables and run the schema again, OR
  - The schema uses `CREATE TABLE IF NOT EXISTS` so it should be safe to run again

### Can't find the API keys
- Make sure you're in **Settings > API** (not Settings > General)
- Look for "Project URL" and "Project API keys" sections
- The keys are long strings starting with `eyJ...`

### .env file not working
- Make sure the file is named exactly `.env` (not `.env.txt`)
- Make sure there are no spaces around the `=` sign
- Make sure the values don't have quotes around them (unless they're part of the actual value)
- On Windows, if you can't create `.env`, try creating it through your code editor or PowerShell

### SQL errors when running schema
- Make sure you copied the ENTIRE schema.sql file
- Check that you're running it as a new query (not appending to existing query)
- Share the error message and I'll help you fix it

## Next Steps

Once you've completed these steps, you're ready to:
1. Install dependencies (`npm install` and `pip install -r requirements.txt`)
2. Start the application
3. Test the connection

Let me know if you encounter any issues!
