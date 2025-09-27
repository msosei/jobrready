# Course Recommendation Engine

An AI-powered recommendation engine for courses and learning paths based on skill gaps and career goals.

## Features

- **Skill Assessment**: Analyze current skills and identify gaps for target roles
- **Course Recommendations**: Suggest relevant courses based on career goals and budget
- **Learning Path Generation**: Create personalized learning paths to reach career objectives
- **Progress Tracking**: Monitor course progress and provide next steps
- **Course Catalog**: Access a comprehensive catalog of available courses

## Endpoints

- `POST /assess-skills` - Assess skill gaps and recommend learning priorities
- `POST /recommend-courses` - Recommend courses based on skills to learn and career goals
- `POST /generate-learning-path` - Generate a personalized learning path to reach career goals
- `POST /track-progress` - Track course progress and provide next steps
- `GET /course-catalog` - Get the course catalog with optional filtering
- `GET /health` - Health check endpoint

## Usage

```bash
curl -X POST "http://localhost:8119/assess-skills" \
  -H "Content-Type: application/json" \
  -d '{
    "current_skills": ["Python", "SQL"],
    "target_role": "Data Scientist",
    "experience_level": "Entry-level"
  }'
```

## Environment Variables

- `PORT`: Port to run the service on (default: 8119)

## Port

This service runs on port 8119.