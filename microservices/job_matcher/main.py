"""
Job Matcher Service
Version: 1.0
Purpose: Match resumes with job postings based on compatibility scoring

This microservice provides functionality to:
1. Match resumes with job postings using compatibility scoring
2. Rank job opportunities based on relevance to candidate profile
3. Provide detailed matching scores for informed decision making
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for the application
# ============================================================================

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

# ============================================================================
# APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata and CORS middleware
# ============================================================================

# Initialize FastAPI application with descriptive title
app = FastAPI(
    title="Job Matcher",
    description="Match resumes with job postings based on compatibility scoring",
    version="1.0.0"
)

# Configure CORS middleware to allow cross-origin requests
# This enables the frontend to communicate with this service
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DATA MODELS
# Pydantic models for data validation and serialization
# ============================================================================

# ----------------------------------------------------------------------------
# REQUEST MODEL
# Model for job matching request data
# ----------------------------------------------------------------------------

class MatchRequest(BaseModel):
    """Request model for job matching"""
    resume_json: Dict[str, Any]
    jobs: List[Dict[str, Any]]

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the job matcher service
# ============================================================================

# ----------------------------------------------------------------------------
# JOB MATCHING ENDPOINT
# Main endpoint for matching resumes with job postings
# ----------------------------------------------------------------------------

@app.post('/match')
async def match(req: MatchRequest):
    """
    Match a resume with job postings and return ranked results
    
    Args:
        req (MatchRequest): Request containing resume data and job listings
        
    Returns:
        dict: Ranked job listings with compatibility scores
        
    Example:
        POST /match
        {
            "resume_json": {
                "experience": "Software Engineer with 5 years experience",
                "skills": ["Python", "JavaScript", "React"]
            },
            "jobs": [
                {
                    "id": 1,
                    "title": "Senior Software Engineer",
                    "description": "Looking for experienced Python developer"
                },
                {
                    "id": 2,
                    "title": "Data Scientist",
                    "description": "ML and data analysis position"
                }
            ]
        }
    """
    # Dummy scoring implementation: higher score if title contains 'Engineer'
    # In a real implementation, this would use more sophisticated matching algorithms
    ranked = [
        { **j, 'score': (100 if 'Engineer' in j.get('title','') else 50) }
        for j in req.jobs
    ]
    
    # Sort jobs by score in descending order (highest scores first)
    ranked.sort(key=lambda x: x['score'], reverse=True)
    
    # Return ranked job listings with scores
    return { 'ranked': ranked }