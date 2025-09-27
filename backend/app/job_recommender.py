"""
AI Job Recommender Service for MyBrand Job Application Platform
Version: v2
Purpose: Provides personalized job recommendations using AI-powered analysis of user data
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for job recommendation functionality
# ============================================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from typing import List, Dict, Any, Optional

# ============================================================================
# ROUTER CONFIGURATION
# Create router for job recommender endpoints with appropriate prefix and tags
# ============================================================================

router = APIRouter(prefix="/ai/job-recommender", tags=["AI Job Recommender"])

# ============================================================================
# DATA MODELS
# Pydantic models for job recommendation data structures and API requests/responses
# ============================================================================

class UserActivity(BaseModel):
    """
    User activity record for recommendation personalization.
    
    Tracks user interactions with job postings to improve recommendation accuracy.
    """
    job_id: str
    action: str
    timestamp: str

class UserPreferences(BaseModel):
    """
    User preferences for job recommendations.
    
    Contains explicit user preferences for roles, industries, locations,
    job types, and other factors that influence recommendations.
    """
    preferred_roles: List[str]
    preferred_industries: List[str]
    preferred_locations: List[str]
    job_types: List[str]
    salary_range: Optional[Dict[str, int]] = None
    experience_level: str

class JobPosting(BaseModel):
    """
    Job posting information for recommendations.
    
    Contains structured information about a job opening including
    location, type, description, requirements, and metadata.
    """
    id: str
    title: str
    company: str
    location: str
    type: str
    description: str
    requirements: List[str]
    salary: Optional[str] = None
    posted_date: str
    is_remote: bool = False
    industry: str
    experience_level: str

class CareerTrajectory(BaseModel):
    """
    User's career trajectory for recommendation analysis.
    
    Contains information about the user's current role, experience,
    skills, career goals, and past roles for career progression insights.
    """
    current_role: str
    years_experience: int
    skills: List[str]
    career_goals: List[str]
    past_roles: List[Dict[str, Any]]

class RecommendationRequest(BaseModel):
    """
    Request model for job recommendation generation.
    
    Contains all user data needed to generate personalized job recommendations.
    """
    user_id: str
    career_trajectory: CareerTrajectory
    preferences: UserPreferences
    activity_history: List[UserActivity]
    job_pool: List[JobPosting]

class JobRecommendation(BaseModel):
    """
    Individual job recommendation with matching details.
    
    Contains information about a recommended job including match score,
    reasons for recommendation, and application probability.
    """
    job_id: str
    title: str
    company: str
    location: str
    match_score: float
    reasons: List[str]
    recommendation_type: str
    apply_probability: float

class RecommendationResponse(BaseModel):
    """
    Response model for comprehensive job recommendations.
    
    Contains multiple categories of job recommendations for a personalized experience.
    """
    recommendations: List[JobRecommendation]
    personalized_feed: List[JobRecommendation]
    career_growth_opportunities: List[JobRecommendation]
    skill_based_matches: List[JobRecommendation]
    new_opportunities: List[JobRecommendation]

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for job recommendation functionality
# ============================================================================

@router.post("/recommend", response_model=RecommendationResponse)
async def get_job_recommendations(request: RecommendationRequest):
    """
    Get comprehensive personalized job recommendations for a user.
    
    This endpoint forwards the recommendation request to a dedicated
    microservice that uses AI to analyze user data and generate multiple
    categories of personalized job recommendations.
    
    Args:
        request (RecommendationRequest): Contains user data for personalization
        
    Returns:
        RecommendationResponse: Comprehensive job recommendations in multiple categories
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> user_preferences = UserPreferences(
        ...     preferred_roles=["Software Engineer", "Developer"],
        ...     preferred_industries=["Technology", "Finance"],
        ...     preferred_locations=["San Francisco", "Remote"],
        ...     job_types=["Full-time"],
        ...     experience_level="Mid-level"
        ... )
        >>> request = RecommendationRequest(
        ...     user_id="user123",
        ...     career_trajectory=CareerTrajectory(...),
        ...     preferences=user_preferences,
        ...     activity_history=[...],
        ...     job_pool=[...]
        ... )
        >>> response = await get_job_recommendations(request)
        >>> print(f"Total recommendations: {len(response.recommendations)}")
    """
    try:
        # ============================================================================
        # SERVICE DISCOVERY
        # Get the job recommender service URL from environment variables
        # ============================================================================
        
        # Get the job recommender service URL
        # In development, this would be http://localhost:8111
        # In production, this would be the deployed service URL
        recommender_service_url = os.getenv("JOB_RECOMMENDER_SERVICE_URL", "http://localhost:8111")
        
        # ============================================================================
        # SERVICE REQUEST
        # Forward the request to the job recommender microservice
        # ============================================================================
        
        # Forward the request to the job recommender microservice
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{recommender_service_url}/recommend",
                json=request.dict(),
                timeout=30.0
            )
            
            # Handle non-success responses from the microservice
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Job recommender service error: {response.text}"
                )
            
            # Return the comprehensive recommendations from the microservice
            return response.json()
    except httpx.RequestError as e:
        # Handle connection errors to the microservice
        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to job recommender service: {str(e)}"
        )
    except Exception as e:
        # Handle any other unexpected errors during recommendation generation
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )

@router.post("/for-you", response_model=List[JobRecommendation])
async def get_for_you_feed(request: RecommendationRequest):
    """
    Get personalized 'For You' job feed for a user.
    
    This endpoint forwards the personalized feed request to a dedicated
    microservice that uses AI to generate a curated job feed based on
    user preferences and activity history.
    
    Args:
        request (RecommendationRequest): Contains user data for personalization
        
    Returns:
        List[JobRecommendation]: Personalized job feed recommendations
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> user_preferences = UserPreferences(
        ...     preferred_roles=["Software Engineer"],
        ...     preferred_industries=["Technology"],
        ...     preferred_locations=["Remote"],
        ...     job_types=["Full-time"]
        ... )
        >>> request = RecommendationRequest(
        ...     user_id="user123",
        ...     career_trajectory=CareerTrajectory(...),
        ...     preferences=user_preferences,
        ...     activity_history=[...],
        ...     job_pool=[...]
        ... )
        >>> feed = await get_for_you_feed(request)
        >>> print(f"Feed contains {len(feed)} jobs")
    """
    try:
        # ============================================================================
        # SERVICE DISCOVERY
        # Get the job recommender service URL from environment variables
        # ============================================================================
        
        # Get the job recommender service URL
        # In development, this would be http://localhost:8111
        # In production, this would be the deployed service URL
        recommender_service_url = os.getenv("JOB_RECOMMENDER_SERVICE_URL", "http://localhost:8111")
        
        # ============================================================================
        # SERVICE REQUEST
        # Forward the request to the job recommender microservice
        # ============================================================================
        
        # Forward the request to the job recommender microservice
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{recommender_service_url}/for-you",
                json=request.dict(),
                timeout=30.0
            )
            
            # Handle non-success responses from the microservice
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Job recommender service error: {response.text}"
                )
            
            # Return the personalized feed from the microservice
            return response.json()
    except httpx.RequestError as e:
        # Handle connection errors to the microservice
        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to job recommender service: {str(e)}"
        )
    except Exception as e:
        # Handle any other unexpected errors during feed generation
        raise HTTPException(
            status_code=500,
            detail=f"Error generating 'For You' feed: {str(e)}"
        )