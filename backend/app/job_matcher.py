"""
AI Job Matcher Service for MyBrand Job Application Platform
Version: v2
Purpose: Performs semantic matching between candidate profiles and job postings using AI
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for job matching functionality
# ============================================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from typing import List, Dict, Any, Optional

# Local imports
from .config import app_settings

# ============================================================================
# ROUTER CONFIGURATION
# Create router for job matcher endpoints with appropriate prefix and tags
# ============================================================================

router = APIRouter(prefix="/ai/job-matcher", tags=["AI Job Matcher"])

# ============================================================================
# DATA MODELS
# Pydantic models for job matching data structures and API requests/responses
# ============================================================================

# ----------------------------------------------------------------------------
# CANDIDATE PROFILE MODEL
# Model representing a candidate's qualifications and preferences
# ----------------------------------------------------------------------------

class CandidateProfile(BaseModel):
    """
    Candidate profile for job matching.
    
    Contains information about a candidate's skills, experience, education,
    career goals, and preferences for job matching.
    """
    skills: List[str]
    experience: List[str]
    education: List[str]
    career_goals: List[str]
    preferred_locations: List[str] = []
    job_types: List[str] = []

# ----------------------------------------------------------------------------
# JOB POSTING MODEL
# Model representing a job opening with its requirements and details
# ----------------------------------------------------------------------------

class JobPosting(BaseModel):
    """
    Job posting information for matching.
    
    Contains structured information about a job opening including
    requirements, location, type, and benefits.
    """
    id: str
    title: str
    company: str
    description: str
    requirements: List[str]
    location: str
    type: str
    salary: Optional[str] = None
    benefits: List[str] = []

# ----------------------------------------------------------------------------
# REQUEST/RESPONSE MODELS
# Models for API communication with job matching service
# ----------------------------------------------------------------------------

class MatchRequest(BaseModel):
    """
    Request model for job matching operations.
    
    Contains a candidate profile and list of job postings to match against.
    """
    candidate: CandidateProfile
    jobs: List[JobPosting]

class JobMatch(BaseModel):
    """
    Individual job match result.
    
    Represents the matching score and analysis for a single job posting
    against a candidate profile.
    """
    job_id: str
    similarity_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    explanation: str

class MatchResponse(BaseModel):
    """
    Response model for job matching results.
    
    Contains a list of job matches and recommended job IDs.
    """
    matches: List[JobMatch]
    recommended_jobs: List[str]

# ============================================================================
# HELPER FUNCTIONS
# Utility functions for service communication and configuration
# ============================================================================

# ----------------------------------------------------------------------------
# SERVICE URL RETRIEVAL
# Function to get the semantic matcher service URL from configuration
# ----------------------------------------------------------------------------

def get_matcher_service_url() -> str:
    """
    Get the semantic matcher service URL from application settings.
    
    Returns the configured URL for the semantic matcher microservice,
    falling back to a default development URL if not configured.
    
    Returns:
        str: The URL of the semantic matcher service
    """
    # Get the semantic matcher service URL from configuration
    # Falls back to localhost URL for development environments
    return app_settings.semantic_matcher_service_url or "http://localhost:8110"

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for job matching functionality
# ============================================================================

# ----------------------------------------------------------------------------
# SEMANTIC JOB MATCHING ENDPOINT
# Main endpoint for performing semantic matching between candidates and jobs
# ----------------------------------------------------------------------------

@router.post("/match", response_model=MatchResponse)
async def semantic_job_matching(request: MatchRequest):
    """
    Perform semantic job matching for a candidate.
    
    This endpoint forwards the job matching request to a dedicated
    microservice that uses AI to semantically match the candidate profile
    with available job postings.
    
    Args:
        request (MatchRequest): Contains candidate profile and job postings to match
        
    Returns:
        MatchResponse: Detailed matching results and recommendations
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> candidate = CandidateProfile(
        ...     skills=["Python", "React", "AWS"],
        ...     experience=["Software Engineer", "Team Lead"],
        ...     education=["B.S. Computer Science"],
        ...     career_goals=["Senior Developer", "Architect"]
        ... )
        >>> jobs = [JobPosting(...), JobPosting(...)]
        >>> request = MatchRequest(candidate=candidate, jobs=jobs)
        >>> response = await semantic_job_matching(request)
        >>> print(f"Found {len(response.matches)} matches")
    """
    try:
        # ============================================================================
        # SERVICE DISCOVERY
        # Get the semantic matcher service URL from configuration
        # ============================================================================
        
        # Get the semantic matcher service URL
        matcher_service_url = get_matcher_service_url()
        
        # ============================================================================
        # SERVICE REQUEST
        # Forward the request to the semantic matcher microservice
        # ============================================================================
        
        # Forward the request to the semantic matcher microservice
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{matcher_service_url}/match",
                json=request.dict(),
                timeout=30.0
            )
            
            # Handle non-success responses from the microservice
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Semantic matcher service error: {response.text}"
                )
            
            # Return the matching results from the microservice
            return response.json()
    except httpx.RequestError as e:
        # Handle connection errors to the microservice
        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to semantic matcher service: {str(e)}"
        )
    except Exception as e:
        # Handle any other unexpected errors during job matching
        raise HTTPException(
            status_code=500,
            detail=f"Error performing job matching: {str(e)}"
        )

# ----------------------------------------------------------------------------
# JOB RANKING ENDPOINT
# Endpoint for ranking jobs by similarity to candidate profile
# ----------------------------------------------------------------------------

@router.post("/rank", response_model=List[JobMatch])
async def rank_jobs(request: MatchRequest):
    """
    Rank jobs by similarity to candidate profile.
    
    This endpoint forwards the job ranking request to a dedicated
    microservice that uses AI to rank job postings based on their
    similarity to the candidate profile.
    
    Args:
        request (MatchRequest): Contains candidate profile and job postings to rank
        
    Returns:
        List[JobMatch]: Ranked list of job matches with similarity scores
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> candidate = CandidateProfile(
        ...     skills=["Python", "React", "AWS"],
        ...     experience=["Software Engineer", "Team Lead"],
        ...     education=["B.S. Computer Science"],
        ...     career_goals=["Senior Developer", "Architect"]
        ... )
        >>> jobs = [JobPosting(...), JobPosting(...)]
        >>> request = MatchRequest(candidate=candidate, jobs=jobs)
        >>> ranked_jobs = await rank_jobs(request)
        >>> print(f"Top match score: {ranked_jobs[0].similarity_score}")
    """
    try:
        # ============================================================================
        # SERVICE DISCOVERY
        # Get the semantic matcher service URL from configuration
        # ============================================================================
        
        # Get the semantic matcher service URL
        matcher_service_url = get_matcher_service_url()
        
        # ============================================================================
        # SERVICE REQUEST
        # Forward the request to the semantic matcher microservice
        # ============================================================================
        
        # Forward the request to the semantic matcher microservice
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{matcher_service_url}/rank",
                json=request.dict(),
                timeout=30.0
            )
            
            # Handle non-success responses from the microservice
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Semantic matcher service error: {response.text}"
                )
            
            # Return the ranked job matches from the microservice
            return response.json()
    except httpx.RequestError as e:
        # Handle connection errors to the microservice
        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to semantic matcher service: {str(e)}"
        )
    except Exception as e:
        # Handle any other unexpected errors during job ranking
        raise HTTPException(
            status_code=500,
            detail=f"Error ranking jobs: {str(e)}"
        )