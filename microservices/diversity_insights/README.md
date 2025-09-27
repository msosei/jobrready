# Diversity & Inclusion Insights Service

An AI-powered microservice that analyzes job postings and companies for diversity and inclusion metrics.

## Features

- **Job Posting Analysis**: Evaluates job descriptions for inclusive language and potential bias
- **Company Inclusivity Metrics**: Provides detailed scores across multiple diversity dimensions
- **Bias Detection**: Identifies biased language and suggests inclusive alternatives
- **Industry Benchmarks**: Compares diversity metrics against industry standards
- **Language Analysis**: Analyzes text for inclusive language usage

## Endpoints

- `POST /analyze-job` - Analyze a job posting for diversity and inclusion metrics
- `POST /analyze-company` - Analyze a company's inclusivity across multiple dimensions
- `POST /detect-bias` - Detect bias in text content and suggest revisions
- `POST /analyze-language` - Analyze text for inclusive language usage
- `GET /industry-benchmarks` - Get diversity and inclusion benchmarks for different industries
- `GET /health` - Health check endpoint

## Usage

```bash
curl -X POST "http://localhost:8115/analyze-job" \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Software Engineer",
    "company_name": "TechCorp",
    "job_description": "We are looking for a rockstar developer with 5+ years experience",
    "company_description": "Equal opportunity employer"
  }'
```

## Environment Variables

- `PORT`: Port to run the service on (default: 8115)

## Port

This service runs on port 8115.