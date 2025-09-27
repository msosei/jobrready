# Interview Prep Coach Microservice

This microservice generates likely interview questions based on a candidate's resume and a job description, helping them prepare more effectively.

## Features

- Generate behavioral, technical, and situational interview questions
- Customize question types based on needs
- Provide preparation tips specific to the role
- Estimate practice session duration

## API Endpoints

### POST /generate-questions

Generate interview questions based on resume and job description.

**Request Body:**
```json
{
  "resume_text": "string",
  "job_description": "string",
  "question_types": ["behavioral", "technical", "situational"]
}
```

**Response:**
```json
{
  "questions": [
    {
      "question": "string",
      "type": "string",
      "category": "string",
      "difficulty": "string",
      "tips": ["string"]
    }
  ],
  "preparation_tips": ["string"],
  "estimated_duration": 45
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

## Question Types

1. **Behavioral**: Questions about past experiences and actions
2. **Technical**: Role-specific technical questions
3. **Situational**: Hypothetical scenarios relevant to the role

## Running the Service

### Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
uvicorn main:app --reload --port 8108
```

### Docker

1. Build the Docker image:
```bash
docker build -t interview-coach .
```

2. Run the container:
```bash
docker run -p 8108:8108 interview-coach
```

## Integration with Docker Compose

The service is included in the main `docker-compose.yml` file and can be started with:
```bash
docker-compose up interview_coach
```