"""
Course Recommender Service for MyBrand Job Application Platform
Version: v2
Purpose: Provides AI-powered course recommendations and learning path generation for career development
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for course recommendation functionality
# ============================================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os

# ============================================================================
# ROUTER CONFIGURATION
# Create router for course recommender endpoints with appropriate prefix and tags
# ============================================================================

router = APIRouter(prefix="/course-recommender", tags=["Course Recommender"])

# ============================================================================
# SERVICE CONFIGURATION
# Get the service URL from environment variables for microservice communication
# ============================================================================

# Get the course recommender service URL from environment variables
# In development, this would be http://localhost:8119
# In production, this would be the deployed service URL
COURSE_RECOMMENDER_SERVICE_URL = os.getenv("COURSE_RECOMMENDER_SERVICE_URL", "http://course_recommender:8119")

# ============================================================================
# DATA MODELS
# Pydantic models for course recommendation data structures and API requests
# ============================================================================

class SkillAssessmentRequest(BaseModel):
    """
    Request model for skill gap assessment.
    
    Contains current skills, target role, and experience level to assess
    learning needs and recommend priorities.
    """
    current_skills: List[str]
    target_role: str
    experience_level: str
    learning_preferences: Optional[List[str]] = None

class CourseRecommendationRequest(BaseModel):
    """
    Request model for course recommendations.
    
    Contains user information, skills to learn, and career goals to generate
    personalized course recommendations.
    """
    user_id: str
    skills_to_learn: List[str]
    career_goal: str
    budget: Optional[float] = None
    time_commitment: Optional[str] = None

class LearningPathRequest(BaseModel):
    """
    Request model for learning path generation.
    
    Contains target role, current skills, experience level, and timeline
    to create a personalized learning path.
    """
    target_role: str
    current_skills: List[str]
    experience_level: str
    timeline: str

class CourseProgressRequest(BaseModel):
    """
    Request model for tracking course progress.
    
    Contains user and course information along with progress percentage
    to track learning and provide next steps.
    """
    user_id: str
    course_id: str
    progress: float

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for course recommendation functionality
# ============================================================================

@router.post("/assess-skills")
async def assess_skills(request: SkillAssessmentRequest):
    """
    Assess skill gaps and recommend learning priorities.
    
    This endpoint forwards the skill assessment request to a dedicated
    microservice that analyzes current skills against target role requirements
    to identify gaps and recommend learning priorities.
    
    Args:
        request (SkillAssessmentRequest): Contains current skills, target role, and experience level
        
    Returns:
        dict: Skill gap analysis with learning priorities and recommendations
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = SkillAssessmentRequest(
        ...     current_skills=["Python", "SQL"],
        ...     target_role="Data Scientist",
        ...     experience_level="Mid-level"
        ... )
        >>> assessment = await assess_skills(request)
        >>> print(f"Recommended skills: {assessment['recommended_skills']}")
    """
    # Forward the request to the course recommender microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{COURSE_RECOMMENDER_SERVICE_URL}/assess-skills",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Course recommender service unavailable: {str(e)}"
            )

@router.post("/recommend-courses")
async def recommend_courses(request: CourseRecommendationRequest):
    """
    Recommend courses based on skills to learn and career goals.
    
    This endpoint forwards the course recommendation request to a dedicated
    microservice that generates personalized course recommendations based
    on user goals, budget, and time constraints.
    
    Args:
        request (CourseRecommendationRequest): Contains user goals and constraints
        
    Returns:
        dict: Personalized course recommendations with details and metadata
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = CourseRecommendationRequest(
        ...     user_id="user123",
        ...     skills_to_learn=["Machine Learning", "Deep Learning"],
        ...     career_goal="AI Engineer",
        ...     budget=500.0,
        ...     time_commitment="Part-time"
        ... )
        >>> recommendations = await recommend_courses(request)
        >>> print(f"Found {len(recommendations['courses'])} courses")
    """
    # Forward the request to the course recommender microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{COURSE_RECOMMENDER_SERVICE_URL}/recommend-courses",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Course recommender service unavailable: {str(e)}"
            )

@router.post("/generate-learning-path")
async def generate_learning_path(request: LearningPathRequest):
    """
    Generate a personalized learning path to reach career goals.
    
    This endpoint forwards the learning path generation request to a dedicated
    microservice that creates a structured learning path with milestones,
    timelines, and course sequences to achieve career objectives.
    
    Args:
        request (LearningPathRequest): Contains career goals and current status
        
    Returns:
        dict: Personalized learning path with milestones and timeline
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = LearningPathRequest(
        ...     target_role="Senior Software Engineer",
        ...     current_skills=["Python", "JavaScript"],
        ...     experience_level="Junior",
        ...     timeline="12 months"
        ... )
        >>> learning_path = await generate_learning_path(request)
        >>> print(f"Path duration: {learning_path['duration']}")
    """
    # Forward the request to the course recommender microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{COURSE_RECOMMENDER_SERVICE_URL}/generate-learning-path",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Course recommender service unavailable: {str(e)}"
            )

@router.post("/track-progress")
async def track_progress(request: CourseProgressRequest):
    """
    Track course progress and provide next steps.
    
    This endpoint forwards the progress tracking request to a dedicated
    microservice that monitors learning progress and suggests next steps
    or additional resources based on completion status.
    
    Args:
        request (CourseProgressRequest): Contains progress information
        
    Returns:
        dict: Progress update with next steps and recommendations
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = CourseProgressRequest(
        ...     user_id="user123",
        ...     course_id="course456",
        ...     progress=0.75
        ... )
        >>> progress_update = await track_progress(request)
        >>> print(f"Next steps: {progress_update['next_steps']}")
    """
    # Forward the request to the course recommender microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{COURSE_RECOMMENDER_SERVICE_URL}/track-progress",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Course recommender service unavailable: {str(e)}"
            )

@router.get("/course-catalog")
async def get_course_catalog(skills: Optional[str] = None, level: Optional[str] = None):
    """
    Get the course catalog with optional filtering.
    
    This endpoint retrieves the course catalog from the dedicated microservice
    with optional filtering by skills and experience level.
    
    Args:
        skills (str, optional): Skills to filter courses by
        level (str, optional): Experience level to filter courses by
        
    Returns:
        dict: Course catalog with filtering options applied
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> catalog = await get_course_catalog(skills="Python", level="Beginner")
        >>> print(f"Found {len(catalog['courses'])} courses")
    """
    # Forward the request to the course recommender microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{COURSE_RECOMMENDER_SERVICE_URL}/course-catalog",
                params={"skills": skills, "level": level},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Course recommender service unavailable: {str(e)}"
            )