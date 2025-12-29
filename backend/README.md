# Backend Application

Python FastAPI backend for the Cybersecurity Intelligence Platform.

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
OPENAI_API_KEY=your_openai_api_key
REDIS_URL=redis://localhost:6379/0
```

3. Run the development server:
```bash
uvicorn main:app --reload --port 8000
```

4. Run Celery worker (in separate terminal):
```bash
celery -A tasks.celery_app worker --loglevel=info
```

5. API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
