# AI Resume Builder Microservice

This microservice generates professional resumes from user-provided data or LinkedIn profile information.

## Features

- Generate resumes from structured data
- Support for multiple resume sections (personal info, experience, education, skills, projects, certifications)
- Multiple resume templates
- LinkedIn profile import support

## API Endpoints

### POST /generate

Generate a resume from structured data.

**Request Body:**
```json
{
  "data": {
    "personal_info": {
      "name": "string",
      "email": "string",
      "phone": "string",
      "address": "string (optional)",
      "linkedin": "string (optional)",
      "github": "string (optional)"
    },
    "summary": "string (optional)",
    "experiences": [
      {
        "company": "string",
        "position": "string",
        "start_date": "string",
        "end_date": "string (optional)",
        "description": ["string"],
        "location": "string (optional)"
      }
    ],
    "education": [
      {
        "institution": "string",
        "degree": "string",
        "field_of_study": "string",
        "start_date": "string",
        "end_date": "string (optional)",
        "gpa": "number (optional)"
      }
    ],
    "skills": [
      {
        "name": "string",
        "level": "string (optional, default: Intermediate)"
      }
    ],
    "projects": [
      {
        "name": "string",
        "description": "string",
        "technologies": ["string"],
        "url": "string (optional)"
      }
    ],
    "certifications": ["string"]
  },
  "template": "string (optional, default: professional)"
}
```

**Response:**
```json
{
  "resume_text": "string",
  "format": "txt"
}
```

### POST /from-linkedin

Generate a resume from LinkedIn data.

**Request Body:**
```json
{
  "name": "string",
  "email": "string",
  "phone": "string",
  "headline": "string",
  "location": "string",
  "linkedin_url": "string",
  "experiences": [
    {
      "company": "string",
      "title": "string",
      "start_date": "string",
      "end_date": "string",
      "description": "string",
      "location": "string"
    }
  ],
  "education": [
    {
      "school": "string",
      "degree": "string",
      "field_of_study": "string",
      "start_date": "string",
      "end_date": "string"
    }
  ],
  "skills": ["string"]
}
```

**Response:**
```json
{
  "resume_text": "string",
  "format": "txt"
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
uvicorn main:app --reload --port 8106
```

### Docker

1. Build the Docker image:
```bash
docker build -t resume-builder .
```

2. Run the container:
```bash
docker run -p 8106:8106 resume-builder
```

## Integration with Docker Compose

The service is included in the main `docker-compose.yml` file and can be started with:
```bash
docker-compose up resume_builder
```