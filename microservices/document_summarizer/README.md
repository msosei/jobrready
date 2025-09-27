# Document Summarizer Service

An AI-powered microservice that summarizes resumes, job descriptions, and other career-related documents.

## Features

- **Document Summarization**: Creates concise summaries of various document types
- **Document Comparison**: Compares documents for compatibility and alignment
- **Keyword Extraction**: Identifies key skills, terms, and action verbs
- **Document Analysis**: Provides insights on readability, sentiment, and tone
- **Template Guidance**: Offers templates for different document types

## Endpoints

- `POST /summarize` - Summarize a document based on its type and desired length
- `POST /compare` - Compare two documents for similarities and differences
- `POST /extract-keywords` - Extract keywords, skills, and important terms from a document
- `POST /analyze` - Provide insights about a document's readability, sentiment, and tone
- `GET /templates` - Get templates for different types of document summaries
- `GET /health` - Health check endpoint

## Usage

```bash
curl -X POST "http://localhost:8116/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "document_text": "Experienced software engineer with 5 years of Python development experience...",
    "document_type": "resume",
    "summary_length": "medium"
  }'
```

## Environment Variables

- `PORT`: Port to run the service on (default: 8116)

## Port

This service runs on port 8116.