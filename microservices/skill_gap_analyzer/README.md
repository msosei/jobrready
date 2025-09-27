# Skill Gap Analyzer Microservice

This microservice analyzes the skill gaps between a user's resume and a job description, providing insights on missing skills and recommendations for improvement.

## Features

- Extracts skills from both resume text and job descriptions
- Identifies matched and missing skills
- Calculates a skill gap score (0-1 scale)
- Provides personalized learning recommendations

## API Endpoints

### POST /analyze

Analyzes skill gaps between a resume and job description.

**Request Body:**
```json
{
  "resume_text": "string",
  "job_description": "string"
}
```

**Response:**
```json
{
  "missing_skills": ["string"],
  "matched_skills": ["string"],
  "skill_gap_score": 0.75,
  "recommendations": ["string"]
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Running the Service

### Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
uvicorn main:app --reload --port 8105
```

### Docker

1. Build the Docker image:
```bash
docker build -t skill-gap-analyzer .
```

2. Run the container:
```bash
docker run -p 8105:8105 skill-gap-analyzer
```

## Integration with Docker Compose

The service is included in the main `docker-compose.yml` file and can be started with:
```bash
docker-compose up skill_gap_analyzer
```