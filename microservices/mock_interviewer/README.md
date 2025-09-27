# AI Mock Interviewer Service

An AI-powered microservice that simulates real interview scenarios with personalized questions and feedback.

## Features

- **Personalized Interview Questions**: Generates relevant questions based on job title, industry, and experience level
- **Multiple Interview Types**: Supports technical, behavioral, and situational interviews
- **Real-time Feedback**: Provides instant AI-generated feedback on answers
- **Adaptive Questioning**: Adjusts question difficulty based on performance
- **Comprehensive Analysis**: Delivers detailed interview completion reports

## Endpoints

- `POST /start-interview` - Start a new mock interview session
- `POST /next-question` - Get the next interview question
- `POST /submit-answer` - Submit an answer and receive feedback
- `POST /complete-interview` - Complete the interview and get overall feedback
- `GET /question-bank` - Access a database of practice questions
- `GET /health` - Health check endpoint

## Usage

```bash
curl -X POST "http://localhost:8114/start-interview" \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Software Engineer",
    "industry": "Technology",
    "experience_level": "Mid-level",
    "interview_type": "Technical",
    "skills": ["Python", "Docker", "AWS"]
  }'
```

## Environment Variables

- `PORT`: Port to run the service on (default: 8114)

## Port

This service runs on port 8114.