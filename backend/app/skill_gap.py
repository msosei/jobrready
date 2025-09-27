"""
AI Skill Gap Analysis Service for MyBrand Job Application Platform
Version: v2
Purpose: Analyzes skill gaps between resumes and job descriptions using AI
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for skill gap analysis
# ============================================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from typing import List

# Local imports
from .config import app_settings
from .error_handlers import ServiceClient, ServiceUnavailableError, ExternalAPIError

# ============================================================================
# ROUTER CONFIGURATION
# Create router for skill gap analysis endpoints with appropriate prefix and tags
# ============================================================================

router = APIRouter(prefix="/ai/skill-gap", tags=["AI Skill Gap Analysis"])

# ============================================================================
# DATA MODELS
# Pydantic models for request/response validation and documentation
# ============================================================================

class SkillGapRequest(BaseModel):
    """
    Request model for skill gap analysis.
    
    Contains the resume text and job description to be analyzed for skill gaps.
    """
    resume_text: str
    job_description: str

class SkillGapResponse(BaseModel):
    """
    Response model for skill gap analysis results.
    
    Provides detailed information about skill matches, gaps, and recommendations.
    """
    missing_skills: List[str]
    matched_skills: List[str]
    skill_gap_score: float
    recommendations: List[str]

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for skill gap analysis functionality
# ============================================================================

@router.post("/analyze", response_model=SkillGapResponse)
async def analyze_skill_gaps(request: SkillGapRequest):
    """
    Analyze skill gaps between a resume and job description.
    
    This endpoint forwards the skill gap analysis request to a dedicated
    microservice that uses AI to compare the provided resume text with
    the job description and identify skill gaps.
    
    Args:
        request (SkillGapRequest): Contains resume text and job description
        
    Returns:
        SkillGapResponse: Analysis results including missing skills,
            matched skills, gap score, and recommendations
            
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = SkillGapRequest(
        ...     resume_text="Experienced Python developer...",
        ...     job_description="Looking for React and Node.js developer..."
        ... )
        >>> response = await analyze_skill_gaps(request)
        >>> print(f"Skill gap score: {response.skill_gap_score}")
    """
    # Create a service client with fallback capability
    client = ServiceClient(
        service_name="skill_gap_analyzer",
        primary_url=app_settings.skill_gap_service_url
    )
    
    try:
        # Forward the request to the skill gap analyzer microservice
        response_data = await client.post(
            "/analyze",
            {
                "resume_text": request.resume_text,
                "job_description": request.job_description
            },
            timeout=30.0
        )
        
        # Return the analysis results from the microservice
        return response_data
    except ServiceUnavailableError as e:
        # Handle service unavailability with a user-friendly error
        raise HTTPException(
            status_code=503,
            detail=f"Skill gap analyzer service is temporarily unavailable. Please try again later."
        )
    except ExternalAPIError as e:
        # Handle external API errors
        raise HTTPException(
            status_code=e.status_code,
            detail=f"Skill gap analyzer service error: {e.message}"
        )
    except Exception as e:
        # Handle any other unexpected errors during analysis
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing skill gaps: {str(e)}"
        )