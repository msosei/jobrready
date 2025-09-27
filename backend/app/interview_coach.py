"""
AI Interview Coach Service for MyBrand Job Application Platform
Version: v2
Purpose: Generates personalized interview questions and preparation materials using AI
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for interview coaching functionality
# ============================================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from typing import List

# ============================================================================
# ROUTER CONFIGURATION
# Create router for interview coach endpoints with appropriate prefix and tags
# ============================================================================

router = APIRouter(prefix="/ai/interview-coach", tags=["AI Interview Coach"])

# ============================================================================
# DATA MODELS
# Pydantic models for interview coaching data structures and API requests/responses
# ============================================================================

class InterviewPrepRequest(BaseModel):
    """
    Request model for interview preparation.
    
    Contains resume text, job description, and preferred question types
    for generating personalized interview preparation materials.
    """
    resume_text: str
    job_description: str
    question_types: List[str] = ["behavioral", "technical", "situational"]

class InterviewQuestion(BaseModel):
    """
    Individual interview question with supporting information.
    
    Contains the question text, type, category, difficulty level, and tips
    for answering effectively.
    """
    question: str
    type: str
    category: str
    difficulty: str
    tips: List[str]

class InterviewPrepResponse(BaseModel):
    """
    Response model for interview preparation results.
    
    Contains generated interview questions, preparation tips, and estimated
    preparation duration.
    """
    questions: List[InterviewQuestion]
    preparation_tips: List[str]
    estimated_duration: int

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for interview coaching functionality
# ============================================================================

@router.post("/generate-questions", response_model=InterviewPrepResponse)
async def generate_interview_questions(request: InterviewPrepRequest):
    """
    Generate personalized interview questions based on resume and job description.
    
    This endpoint forwards the interview preparation request to a dedicated
    microservice that uses AI to analyze the candidate's resume and the job
    description to generate relevant interview questions and preparation tips.
    
    Args:
        request (InterviewPrepRequest): Contains resume text, job description,
            and preferred question types for preparation
            
    Returns:
        InterviewPrepResponse: Generated interview questions, tips, and duration
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = InterviewPrepRequest(
        ...     resume_text="Experienced Python developer with 5 years in web development...",
        ...     job_description="Looking for a senior Python developer with AWS experience...",
        ...     question_types=["technical", "behavioral"]
        ... )
        >>> response = await generate_interview_questions(request)
        >>> print(f"Generated {len(response.questions)} questions")
    """
    try:
        # ============================================================================
        # SERVICE DISCOVERY
        # Get the interview coach service URL from environment variables
        # ============================================================================
        
        # Get the interview coach service URL
        # In development, this would be http://localhost:8108
        # In production, this would be the deployed service URL
        coach_service_url = os.getenv("INTERVIEW_COACH_SERVICE_URL", "http://localhost:8108")
        
        # ============================================================================
        # SERVICE REQUEST
        # Forward the request to the interview coach microservice
        # ============================================================================
        
        # Forward the request to the interview coach microservice
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{coach_service_url}/generate-questions",
                json=request.dict(),
                timeout=30.0
            )
            
            # Handle non-success responses from the microservice
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Interview coach service error: {response.text}"
                )
            
            # Return the generated interview preparation materials from the microservice
            return response.json()
    except httpx.RequestError as e:
        # Handle connection errors to the microservice
        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to interview coach service: {str(e)}"
        )
    except Exception as e:
        # Handle any other unexpected errors during question generation
        raise HTTPException(
            status_code=500,
            detail=f"Error generating interview questions: {str(e)}"
        )