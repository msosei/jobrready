# MyBrand Job Application Platform

Developer-ready scaffold for a full-stack job-application platform inspired by modern job tools. Includes Next.js frontend, FastAPI backend, Redis/BullMQ workers, AI microservices, and a Chrome Extension (MV3), with Supabase (Postgres, Auth, Storage) and Stripe billing integration.

## Tech Stack
- Frontend: Next.js + React + TailwindCSS (TypeScript)
- Backend: FastAPI (Python) with Supabase
- Queue: Redis + BullMQ (Node)
- AI Microservices: Python FastAPI services (Docker-ready)
- Chrome Extension: Manifest v3
- Billing: Stripe
- Auth/DB/Storage: Supabase

## Monorepo Structure
```
frontend/
backend/
  functions/
  workers/
microservices/
  resume_parser/
  cover_letter_generator/
  job_matcher/
  resume_scorer/
chrome_extension/
config/
scripts/
```

## Quickstart

### Automated Setup
```bash
# Run the setup script
./scripts/dev-setup.sh
```

### Manual Setup
1) Prerequisites: Node 18+, npm, Python 3.10+, Docker, Supabase project, Stripe account

2) Copy envs:
```bash
cp config/example.env config/.env
```
Fill values for Supabase, Stripe, OpenAI, Redis.

3) Database Setup:
```bash
# Run in Supabase SQL editor or local PostgreSQL
psql -f scripts/setup-db.sql
```

4) Start services:
```bash
# Redis
docker compose up -d redis

# Frontend
cd frontend && npm install && npm run dev

# Backend API
cd backend && python -m venv .venv && source .venv/bin/activate && pip install -e . && uvicorn app.main:app --reload

# Workers (BullMQ)
cd backend/workers && npm install && npm run start:dev

# Microservices (in separate terminals)
cd microservices/resume_parser && pip install -r requirements.txt && uvicorn main:app --reload --port 8101
cd microservices/cover_letter_generator && pip install -r requirements.txt && uvicorn main:app --reload --port 8103
cd microservices/job_matcher && pip install -r requirements.txt && uvicorn main:app --reload --port 8102
cd microservices/resume_scorer && pip install -r requirements.txt && uvicorn main:app --reload --port 8104
```

5) Chrome Extension
- Load `chrome_extension` as an unpacked extension in Chrome (Developer Mode).

### Testing
```bash
cd frontend && npm test
```

## Environment Variables (config/.env)
- SUPABASE_URL=
- SUPABASE_ANON_KEY=
- SUPABASE_SERVICE_ROLE=
- SUPABASE_STORAGE_BUCKET=resumes
- DATABASE_URL=postgresql://...  (if needed for local dev)
- STRIPE_SECRET_KEY=
- STRIPE_WEBHOOK_SECRET=
- OPENAI_API_KEY=
- REDIS_URL=redis://localhost:6379
- JWT_SECRET=
- APP_URL=http://localhost:3000
- API_URL=http://localhost:8000

## Database Schema (Supabase)
See `config/schema.sql` and `config/rls.sql` for tables and RLS policies.

## Scripts
See `scripts/` for helper scripts to run and seed services.

## New AI Microservices (Q-V)

### Q. Application Tailor-on-the-Fly
- Real-time resume & cover letter rewriting matched to specific job descriptions
- Integrated with existing ATS Optimizer
- API: `POST /api/ai/tailor-application`

### R. Mock Interview Simulator  
- Interactive Q&A with adaptive difficulty
- Session history stored in Supabase
- API: `POST /api/ai/mock-interview`

### S. Gap-to-Job Bridge
- Narrative generator to explain employment gaps
- User-generated gap narratives saved in DB
- API: `POST /api/ai/gap-narrative`

### T. Portfolio Project Generator
- Generate project ideas & starter code repos
- GitHub integration for repository creation
- API: `POST /api/ai/portfolio-project`

### U. Personal Website/Portfolio Generator
- Auto-generate personal websites (Next.js + Vercel)
- Template-based with customization options
- API: `POST /api/ai/personal-website`

### V. Bulk Apply Orchestrator
- Queue-based bulk job applications using Playwright
- Ethical guardrails (pause, confirm before submission)
- API: `POST /api/ai/bulk-apply`

## Billing Plans
- **Free**: Limited Q+R usage (5 applications, 5 cover letters, 20 AI requests)
- **Pro**: Full Q+R+S+T+U access (50 applications, 50 cover letters, 200 AI requests)  
- **Premium**: Everything + Bulk Apply (unlimited usage)

## Notes
- This scaffold assumes a hosted Supabase project. For local Postgres+Supabase Studio, use Supabase CLI or Docker setup separately.
- All services are TypeScript/Python with strict linting recommended.
- AI microservices include Jest test scaffolding for comprehensive testing.


