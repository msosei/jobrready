# MyBrand Job Application Platform

A comprehensive job application platform with AI-powered career tools and services.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

The MyBrand Job Application Platform is a modern, AI-powered job search and career development platform. It provides job seekers with tools to find jobs, build resumes, prepare for interviews, and identify skill gaps. The platform integrates with multiple AI microservices to deliver personalized career guidance.

## Features

### Job Search
- Advanced job search with filtering by keyword, location, job type, and company
- Integration with Adzuna job API for real-time job listings
- Local job search fallback for offline development

### AI Career Tools
- **Skill Gap Analysis**: Compare your resume with job descriptions to identify missing skills
- **Resume Builder**: Generate professional resumes from your data
- **Resume Enhancer**: Improve existing resumes with AI-powered suggestions
- **Interview Coach**: Get personalized interview questions and preparation tips
- **Job Matcher**: Find jobs that match your skills and career goals
- **Mock Interviewer**: Practice interviews with AI-powered feedback
- **Document Summarizer**: Summarize job descriptions and other documents

### Real-time Features
- WebSocket-based real-time notifications
- Instant messaging between candidates and employers

### Additional Services
- Multi-language support
- Diversity and inclusion insights
- Course recommendations
- Voice agent for hands-free interaction

## Architecture

The platform follows a microservices architecture with the following components:

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Frontend      │    │   Backend API    │    │   Microservices  │
│   (React/Vite)  │◄──►│   (FastAPI)      │◄──►│   (15+ services) │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                              │                         │
                              ▼                         ▼
                       ┌─────────────┐         ┌─────────────────┐
                       │   Redis     │         │   External APIs │
                       │ (Caching)   │         │ (Adzuna, etc.)  │
                       └─────────────┘         └─────────────────┘
```

### Backend Services

1. **Main API Service** - Central API gateway
2. **Job Search Service** - Job listing and search functionality
3. **Notification Service** - Real-time messaging and notifications
4. **15+ AI Microservices** - Specialized AI-powered career tools

### Frontend

- Built with React and TypeScript
- Uses Vite for fast development and building
- Responsive design for all devices
- Real-time updates via WebSocket

## Prerequisites

- Python 3.10+
- Node.js 16+
- Docker and Docker Compose
- Redis server
- API keys for external services (Adzuna, OpenAI, etc.)

## Installation

### Backend Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd job-ready
   ```

2. Create a virtual environment:
   ```bash
   python -m venv backend/venv
   source backend/venv/bin/activate  # On Windows: backend\venv\Scripts\activate
   ```

3. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

### Microservices Setup

1. Build Docker images for microservices:
   ```bash
   docker-compose build
   ```

## Configuration

### Environment Variables

Create `.env` files in the root directory and in each service directory:

**Root .env:**
```bash
# Copy .env.example to .env and fill in your values
cp .env.example .env
```

**Frontend .env.development:**
```bash
# Copy frontend/.env.example to frontend/.env.development and fill in your values
cp frontend/.env.example frontend/.env.development
```

Required environment variables include:
- `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` for job search
- `OPENAI_API_KEY` for AI services
- `SUPABASE_URL` and `SUPABASE_ANON_KEY` for authentication
- `STRIPE_SECRET_KEY` for payment processing

## Running the Application

### Development Mode

1. Start Redis:
   ```bash
   redis-server
   ```

2. Start backend services:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

3. Start frontend:
   ```bash
   cd frontend
   npm run dev
   ```

4. Start microservices:
   ```bash
   docker-compose up
   ```

### Production Mode

1. Build and start all services:
   ```bash
   docker-compose -f docker-compose.yml up --build
   ```

## API Documentation

The API is documented using OpenAPI/Swagger:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### Key Endpoints

- `GET /jobs/search` - Search for jobs
- `POST /ai/skill-gap/analyze` - Analyze skill gaps
- `POST /ai/resume-builder/generate` - Generate resumes
- `POST /ai/interview-coach/generate-questions` - Generate interview questions
- `GET /health` - Health check endpoint

## Testing

### Backend Testing

Run backend tests:
```bash
cd backend
python -m pytest
```

### Frontend Testing

Run frontend tests:
```bash
cd frontend
npm test
```

### Integration Testing

Run integration tests with TestSprite:
```bash
# Run TestSprite tests
testsprite run
```

## Deployment

### Docker Deployment

1. Build and push Docker images:
   ```bash
   docker-compose build
   docker-compose push
   ```

2. Deploy to your preferred platform:
   ```bash
   docker-compose up -d
   ```

### Kubernetes Deployment

Kubernetes manifests are available in the `k8s/` directory.

### Cloud Deployment

The application can be deployed to major cloud platforms:
- AWS with ECS/EKS
- Google Cloud with GKE
- Azure with AKS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Code Style

- Backend: Follow PEP 8 guidelines
- Frontend: Use ESLint and Prettier configurations
- Documentation: Write clear, concise documentation

### Development Workflow

1. Create an issue describing the feature or bug fix
2. Assign yourself to the issue
3. Create a branch with a descriptive name
4. Make changes and commit with clear messages
5. Submit a pull request for review

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

---

*For support, contact [support@mybrand.com](mailto:support@mybrand.com)*