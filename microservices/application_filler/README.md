# Job Application Auto-Fill Microservice

This microservice extracts data from resumes and auto-fills job application forms, saving time for job seekers.

## Features

- Extract personal information, work experience, education, and skills from resumes
- Auto-fill application forms based on form field definitions
- Provide confidence scores for each filled field
- Identify missing required fields

## API Endpoints

### POST /auto-fill

Auto-fill job application form based on resume.

**Request Body:**
```json
{
  "resume_text": "string",
  "form_fields": [
    {
      "name": "string",
      "label": "string",
      "type": "string",
      "required": true,
      "options": ["string"]
    }
  ],
  "target_company": "string (optional)"
}
```

**Response:**
```json
{
  "filled_data": {
    "field_name": "field_value"
  },
  "confidence_scores": {
    "field_name": 0.9
  },
  "missing_fields": ["field_name"]
}
```

### POST /extract-data

Extract structured data from resume text.

**Request Body:**
```json
{
  "resume_text": "string"
}
```

**Response:**
```json
{
  "personal_info": {
    "name": "string",
    "email": "string",
    "phone": "string",
    "address": "string",
    "linkedin": "string",
    "github": "string",
    "website": "string"
  },
  "work_experience": [
    {
      "company": "string",
      "position": "string",
      "start_date": "string",
      "end_date": "string",
      "description": "string"
    }
  ],
  "education": [
    {
      "institution": "string",
      "degree": "string",
      "field_of_study": "string",
      "start_date": "string",
      "end_date": "string",
      "gpa": 3.8
    }
  ],
  "skills": ["string"],
  "certifications": ["string"],
  "portfolio_url": "string"
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

## Supported Form Field Types

1. **text**: Single-line text input
2. **email**: Email address input
3. **phone**: Phone number input
4. **textarea**: Multi-line text input
5. **select**: Dropdown selection
6. **checkbox**: Checkbox selection
7. **radio**: Radio button selection

## Running the Service

### Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
uvicorn main:app --reload --port 8109
```

### Docker

1. Build the Docker image:
```bash
docker build -t application-filler .
```

2. Run the container:
```bash
docker run -p 8109:8109 application-filler
```

## Integration with Docker Compose

The service is included in the main `docker-compose.yml` file and can be started with:
```bash
docker-compose up application_filler
```