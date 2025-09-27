# Personalized Job Recommender Microservice

This microservice generates personalized job recommendations based on career trajectory, preferences, and activity history.

## Features

- Personalized "For You" job feed
- Career growth opportunity identification
- Skill-based job matching
- Activity history-based recommendation adjustment
- Multi-category recommendation system

## API Endpoints

### POST /recommend

Get comprehensive personalized job recommendations.

**Request Body:**
```json
{
  "user_id": "string",
  "career_trajectory": {
    "current_role": "string",
    "years_experience": 5,
    "skills": ["string"],
    "career_goals": ["string"],
    "past_roles": [
      {
        "role": "string",
        "duration": "string",
        "achievements": ["string"]
      }
    ]
  },
  "preferences": {
    "preferred_roles": ["string"],
    "preferred_industries": ["string"],
    "preferred_locations": ["string"],
    "job_types": ["string"],
    "salary_range": {"min": 50000, "max": 100000},
    "experience_level": "string"
  },
  "activity_history": [
    {
      "job_id": "string",
      "action": "string",
      "timestamp": "string"
    }
  ],
  "job_pool": [
    {
      "id": "string",
      "title": "string",
      "company": "string",
      "location": "string",
      "type": "string",
      "description": "string",
      "requirements": ["string"],
      "salary": "string",
      "posted_date": "string",
      "is_remote": true,
      "industry": "string",
      "experience_level": "string"
    }
  ]
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "job_id": "string",
      "title": "string",
      "company": "string",
      "location": "string",
      "match_score": 0.85,
      "reasons": ["string"],
      "recommendation_type": "string",
      "apply_probability": 0.75
    }
  ],
  "personalized_feed": [],
  "career_growth_opportunities": [],
  "skill_based_matches": [],
  "new_opportunities": []
}
```

### POST /for-you

Get personalized "For You" job feed.

**Request Body:**
```json
{
  "user_id": "string",
  "career_trajectory": {},
  "preferences": {},
  "activity_history": [],
  "job_pool": []
}
```

**Response:**
```json
[
  {
    "job_id": "string",
    "title": "string",
    "company": "string",
    "location": "string",
    "match_score": 0.85,
    "reasons": ["string"],
    "recommendation_type": "string",
    "apply_probability": 0.75
  }
]
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Recommendation Types

1. **For You**: General personalized recommendations
2. **Career Growth**: Jobs representing advancement opportunities
3. **Skill Match**: Jobs matching user's skill set
4. **New Opportunities**: Novel roles outside user's typical preferences

## Running the Service

### Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
uvicorn main:app --reload --port 8111
```

### Docker

1. Build the Docker image:
```bash
docker build -t job-recommender .
```

2. Run the container:
```bash
docker run -p 8111:8111 job-recommender
```

## Integration with Docker Compose

The service is included in the main `docker-compose.yml` file and can be started with:
```bash
docker-compose up job_recommender
```