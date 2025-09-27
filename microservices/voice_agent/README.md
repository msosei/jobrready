# Voice Agent Service

An AI-powered voice agent for hands-free job application assistance.

## Features

- **Voice Command Processing**: Understands and responds to voice commands for job search tasks
- **Speech-to-Text Conversion**: Converts spoken words to text for processing
- **Text-to-Speech Generation**: Converts text responses to natural-sounding speech
- **Voice Analysis**: Analyzes tone, sentiment, and confidence in speech
- **Voice Interview Practice**: Conducts mock interviews via voice interaction
- **Command Library**: Provides a comprehensive library of voice commands

## Endpoints

- `POST /process-command` - Process a voice command and return appropriate response
- `POST /speech-to-text` - Convert speech to text
- `POST /text-to-speech` - Convert text to speech
- `POST /analyze-voice` - Analyze voice characteristics and provide feedback
- `POST /voice-interview` - Conduct a voice-based interview practice session
- `GET /voice-commands` - Get a list of available voice commands
- `POST /upload-audio` - Upload audio file for processing
- `GET /health` - Health check endpoint

## Usage

```bash
curl -X POST "http://localhost:8117/process-command" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Help me with my resume",
    "user_id": "user123"
  }'
```

## Environment Variables

- `PORT`: Port to run the service on (default: 8117)

## Port

This service runs on port 8117.