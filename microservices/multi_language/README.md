# Multi-Language Support Service

An AI service for translating and localizing job search content for global users.

## Features

- **Text Translation**: Translate content between multiple languages
- **Content Localization**: Adapt content for specific locales and cultural contexts
- **Language Detection**: Automatically detect the language of provided text
- **Cultural Adaptation**: Adjust content for cultural norms and expectations
- **Language Support**: Comprehensive support for major world languages

## Endpoints

- `POST /translate` - Translate text from source language to target language
- `POST /localize` - Localize content for a specific locale
- `POST /detect-language` - Detect the language of provided text
- `POST /cultural-adaptation` - Adapt content for specific cultural contexts
- `GET /supported-languages` - Get a list of supported languages
- `GET /language-pair-support` - Check if a specific language pair is supported
- `GET /health` - Health check endpoint

## Usage

```bash
curl -X POST "http://localhost:8118/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Software Engineer with 5 years of experience",
    "source_language": "en",
    "target_language": "es"
  }'
```

## Environment Variables

- `PORT`: Port to run the service on (default: 8118)

## Port

This service runs on port 8118.