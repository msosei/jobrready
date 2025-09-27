# AI Career Chatbot Microservice

This microservice provides a conversational AI assistant for career guidance, job search assistance, and professional development advice.

## Features

- Conversational interface for career advice
- Contextual responses based on user input
- Career advice on multiple topics (resumes, interviews, job search, etc.)
- Suggested follow-up questions and actions
- Resource recommendations

## API Endpoints

### POST /chat

Handle chat conversations with the career assistant.

**Request Body:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "string"
    }
  ],
  "user_id": "string",
  "context": {
    "additionalProp1": "string"
  }
}
```

**Response:**
```json
{
  "response": "string",
  "suggestions": ["string"],
  "next_questions": ["string"]
}
```

### POST /career-advice

Get career advice on a specific topic.

**Request Body:**
```json
{
  "topic": "string",
  "user_profile": {
    "additionalProp1": "string"
  }
}
```

**Response:**
```json
{
  "advice": "string",
  "resources": [
    {
      "title": "string",
      "url": "string"
    }
  ],
  "action_items": ["string"]
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

## Supported Topics

1. **resume** - Resume writing tips and best practices
2. **interview** - Interview preparation and techniques
3. **job_search** - Job searching strategies and tips
4. **career_change** - Advice for changing careers
5. **skill_development** - Guidance on developing new skills

## Running the Service

### Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
uvicorn main:app --reload --port 8112
```

### Docker

1. Build the Docker image:
```bash
docker build -t career-chatbot .
```

2. Run the container:
```bash
docker run -p 8112:8112 career-chatbot
```

## Integration with Docker Compose

The service is included in the main `docker-compose.yml` file and can be started with:
```bash
docker-compose up career_chatbot
```