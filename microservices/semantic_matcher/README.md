# Semantic Job Matcher Microservice

This microservice ranks jobs by semantic similarity to a candidate's skills, experience, and career goals, providing more relevant job recommendations.

## Features

- Semantic matching of jobs to candidate profiles
- Multi-factor similarity scoring (skills, experience, location, job type)
- Detailed match explanations
- Customizable weighting of matching factors

## API Endpoints

### POST /match

Perform semantic job matching for a candidate.

**Request Body:**
```json
{
  "candidate": {
    "skills": ["string"],
    "experience": ["string"],
    "education": ["string"],
    "career_goals": ["string"],
    "preferred_locations": ["string"],
    "job_types": ["string"]
  },
  "jobs": [
    {
      "id": "string",
      "title": "string",
      "company": "string",
      "description": "string",
      "requirements": ["string"],
      "location": "string",
      "type": "string",
      "salary": "string",
      "benefits": ["string"]
    }
  ]
}
```

**Response:**
```json
{
  "matches": [
    {
      "job_id": "string",
      "similarity_score": 0.85,
      "matching_skills": ["string"],
      "missing_skills": ["string"],
      "explanation": "string"
    }
  ],
  "recommended_jobs": ["job_id"]
}
```

### POST /rank

Rank jobs by similarity to candidate profile.

**Request Body:**
```json
{
  "candidate": {
    "skills": ["string"],
    "experience": ["string"],
    "education": ["string"],
    "career_goals": ["string"],
    "preferred_locations": ["string"],
    "job_types": ["string"]
  },
  "jobs": [
    {
      "id": "string",
      "title": "string",
      "company": "string",
      "description": "string",
      "requirements": ["string"],
      "location": "string",
      "type": "string",
      "salary": "string",
      "benefits": ["string"]
    }
  ]
}
```

**Response:**
```json
[
  {
    "job_id": "string",
    "similarity_score": 0.85,
    "matching_skills": ["string"],
    "missing_skills": ["string"],
    "explanation": "string"
  }
]
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Matching Factors

1. **Skills**: 40% weight - Match between candidate skills and job requirements
2. **Experience**: 30% weight - Similarity between candidate experience and job description
3. **Location**: 15% weight - Match between preferred locations and job location
4. **Job Type**: 15% weight - Match between preferred job types and job type

## Running the Service

### Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
uvicorn main:app --reload --port 8110
```

### Docker

1. Build the Docker image:
```bash
docker build -t semantic-matcher .
```

2. Run the container:
```bash
docker run -p 8110:8110 semantic-matcher
```

## Integration with Docker Compose

The service is included in the main `docker-compose.yml` file and can be started with:
```bash
docker-compose up semantic_matcher
```