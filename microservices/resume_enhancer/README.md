# Resume Enhancer Microservice

This microservice parses resumes, analyzes them for ATS compatibility, and provides suggestions for improvement.

## Features

- Parse resumes into structured sections
- Analyze ATS compatibility score
- Provide enhancement suggestions
- Optimize resumes for applicant tracking systems

## API Endpoints

### POST /parse

Parse a resume and provide structural suggestions.

**Request Body:**
```json
{
  "resume_text": "string"
}
```

**Response:**
```json
{
  "parsed_data": {
    "PROFESSIONAL EXPERIENCE": "string",
    "EDUCATION": "string",
    "SKILLS": "string"
  },
  "suggestions": [
    {
      "type": "string",
      "issue": "string",
      "suggestion": "string",
      "priority": "string"
    }
  ]
}
```

### POST /enhance

Parse, analyze, and enhance a resume for ATS optimization.

**Request Body:**
```json
{
  "resume_text": "string"
}
```

**Response:**
```json
{
  "enhanced_resume": "string",
  "suggestions": [
    {
      "type": "string",
      "issue": "string",
      "suggestion": "string",
      "priority": "string"
    }
  ],
  "ats_score": 0.75
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

## Enhancement Types

1. **Formatting**: Suggestions for consistent spacing, fonts, and layout
2. **Keywords**: Recommendations for industry-specific keywords
3. **Phrasing**: Improvements to action verbs and descriptions
4. **Structure**: Guidance on organizing sections and information

## Running the Service

### Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
uvicorn main:app --reload --port 8107
```

### Docker

1. Build the Docker image:
```bash
docker build -t resume-enhancer .
```

2. Run the container:
```bash
docker run -p 8107:8107 resume-enhancer
```

## Integration with Docker Compose

The service is included in the main `docker-compose.yml` file and can be started with:
```bash
docker-compose up resume_enhancer
```