# Setup Guide

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Supabase account and project
- Redis (for background tasks - optional for basic usage)

## Initial Setup

### 1. Supabase Setup

1. Create a new Supabase project at https://supabase.com
2. Copy your project URL and anon key from Project Settings > API
3. Run the SQL schema:
   - Go to SQL Editor in Supabase dashboard
   - Copy and paste the contents of `supabase/schema.sql`
   - Execute the script

### 2. Environment Variables

Create a `.env` file in the root directory:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
API_URL=http://localhost:8000

# OpenAI (optional - for enhanced AI capabilities)
OPENAI_API_KEY=your_openai_api_key

# Redis (optional - for background tasks)
REDIS_URL=redis://localhost:6379/0
```

### 3. Install Dependencies

**Frontend:**
```bash
npm install
```

**Backend:**
```bash
cd backend
pip install -r ../requirements.txt
```

### 4. Run the Application

**Terminal 1 - Frontend:**
```bash
npm run dev
```

**Terminal 2 - Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 3 - Celery Worker (Optional):**
```bash
cd backend
celery -A tasks.celery_app worker --loglevel=info
```

### 5. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## First Steps

1. **Verify Database Connection**: Check that Supabase connection is working
2. **Test Chat Interface**: Try asking questions in the chat interface
3. **Explore Dashboard**: View the security dashboard metrics
4. **Import Data**: Use the data ingestion API to import your first dataset

## Troubleshooting

### Backend won't start
- Check that all environment variables are set
- Verify Supabase credentials
- Ensure Python dependencies are installed

### Frontend can't connect to backend
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings in backend
- Ensure backend is running on port 8000

### Database errors
- Verify schema has been run in Supabase
- Check RLS policies if getting permission errors
- Verify service role key has correct permissions
