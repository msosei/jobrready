"""
AI Resume Builder Service for MyBrand Job Application Platform
Version: v2
Purpose: Generates professional resumes from user data using AI-powered formatting
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for resume building functionality
# ============================================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from typing import List, Optional

# Local imports
from .config import app_settings

# ============================================================================
# ROUTER CONFIGURATION
# Create router for resume builder endpoints with appropriate prefix and tags
# ============================================================================

router = APIRouter(prefix="/ai/resume-builder", tags=["AI Resume Builder"])

# ============================================================================
# DATA MODELS
# Pydantic models for resume data structures and API requests/responses
# ============================================================================

class PersonalInfo(BaseModel):
    """
    Personal information section of a resume.
    
    Contains essential contact information for the resume owner.
    """
    name: str
    email: str
    phone: str
    address: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

class Experience(BaseModel):
    """
    Professional experience entry in a resume.
    
    Details about a specific position including company, role, dates, and description.
    """
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = "Present"
    description: List[str]
    location: Optional[str] = None

class Education(BaseModel):
    """
    Educational background entry in a resume.
    
    Details about academic qualifications including institution, degree, and dates.
    """
    institution: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: Optional[str] = None
    gpa: Optional[float] = None

class Skill(BaseModel):
    """
    Technical or professional skill with proficiency level.
    """
    name: str
    level: Optional[str] = "Intermediate"

class Project(BaseModel):
    """
    Personal or professional project showcase.
    
    Highlights relevant projects with technologies used and links.
    """
    name: str
    description: str
    technologies: List[str]
    url: Optional[str] = None

class ResumeData(BaseModel):
    """
    Complete resume data structure.
    
    Organizes all sections of a resume including personal info, experiences,
    education, skills, and optional sections.
    """
    personal_info: PersonalInfo
    summary: Optional[str] = None
    experiences: List[Experience]
    education: List[Education]
    skills: List[Skill]
    projects: Optional[List[Project]] = None
    certifications: Optional[List[str]] = None

class ResumeRequest(BaseModel):
    """
    Request model for resume generation.
    
    Contains the complete resume data and formatting preferences.
    """
    data: ResumeData
    template: Optional[str] = "professional"

class ResumeResponse(BaseModel):
    """
    Response model for generated resumes.
    
    Contains the formatted resume content and its format type.
    """
    resume_text: str
    format: str

class LinkedInData(BaseModel):
    """
    LinkedIn profile data structure.
    
    Standardized format for importing LinkedIn profile information.
    """
    name: str
    email: str
    phone: str
    headline: str
    location: str
    linkedin_url: str
    experiences: List[dict]
    education: List[dict]
    skills: List[str]

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for resume building functionality
# ============================================================================

@router.post("/generate", response_model=ResumeResponse)
async def generate_resume(request: ResumeRequest):
    """
    Generate a professional resume from provided data.
    
    This endpoint forwards the resume generation request to a dedicated
    microservice that uses AI to format the provided resume data into
    a professional document using the specified template.
    
    Args:
        request (ResumeRequest): Contains resume data and template preferences
        
    Returns:
        ResumeResponse: Generated resume content in the specified format
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> resume_data = ResumeData(
        ...     personal_info=PersonalInfo(name="John Doe", email="john@example.com", phone="123-456-7890"),
        ...     experiences=[...],
        ...     education=[...],
        ...     skills=[...]
        ... )
        >>> request = ResumeRequest(data=resume_data, template="modern")
        >>> response = await generate_resume(request)
        >>> print(response.resume_text)
    """
    try:
        # ============================================================================
        # SERVICE DISCOVERY
        # Get the resume builder service URL from environment variables
        # ============================================================================
        
        # Get the resume builder service URL
        # In development, this would be http://localhost:8106
        # In production, this would be the deployed service URL
        resume_service_url = os.getenv("RESUME_BUILDER_SERVICE_URL", "http://localhost:8106")
        
        # Get the resume builder service URL from configuration
        resume_service_url = app_settings.resume_builder_service_url
        
        # ============================================================================
        # SERVICE REQUEST
        # Forward the request to the resume builder microservice
        # ============================================================================
        
        # Forward the request to the resume builder microservice
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{resume_service_url}/generate",
                json=request.dict(),
                timeout=30.0
            )
            
            # Handle non-success responses from the microservice
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Resume builder service error: {response.text}"
                )
            
            # Return the generated resume from the microservice
            return response.json()
    except httpx.RequestError as e:
        # Handle connection errors to the microservice
        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to resume builder service: {str(e)}"
        )
    except Exception as e:
        # Handle any other unexpected errors during resume generation
        raise HTTPException(
            status_code=500,
            detail=f"Error generating resume: {str(e)}"
        )

@router.post("/from-linkedin", response_model=ResumeResponse)
async def generate_resume_from_linkedin(linkedin_data: LinkedInData):
    """
    Generate a resume from LinkedIn profile data.
    
    This endpoint forwards LinkedIn data to a dedicated microservice that
    converts the profile information into a professionally formatted resume.
    
    Args:
        linkedin_data (LinkedInData): Structured LinkedIn profile information
        
    Returns:
        ResumeResponse: Generated resume content in the specified format
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> linkedin_data = LinkedInData(
        ...     name="John Doe",
        ...     email="john@example.com",
        ...     headline="Software Engineer",
        ...     experiences=[...],
        ...     education=[...],
        ...     skills=[...]
        ... )
        >>> response = await generate_resume_from_linkedin(linkedin_data)
        >>> print(response.resume_text)
    """
    try:
        # ============================================================================
        # SERVICE DISCOVERY
        # Get the resume builder service URL from environment variables
        # ============================================================================
        
        # Get the resume builder service URL
        # In development, this would be http://localhost:8106
        # In production, this would be the deployed service URL
        resume_service_url = os.getenv("RESUME_BUILDER_SERVICE_URL", "http://localhost:8106")
        
        # Get the resume builder service URL from configuration
        resume_service_url = app_settings.resume_builder_service_url
        
        # ============================================================================
        # SERVICE REQUEST
        # Forward the LinkedIn data to the resume builder microservice
        # ============================================================================
        
        # Forward the LinkedIn data to the resume builder microservice
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{resume_service_url}/from-linkedin",
                json=linkedin_data.dict(),
                timeout=30.0
            )
            
            # Handle non-success responses from the microservice
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Resume builder service error: {response.text}"
                )
            
            # Return the generated resume from the microservice
            return response.json()
    except httpx.RequestError as e:
        # Handle connection errors to the microservice
        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to resume builder service: {str(e)}"
        )
    except Exception as e:
        # Handle any other unexpected errors during LinkedIn-based resume generation
        raise HTTPException(
            status_code=500,
            detail=f"Error generating resume from LinkedIn data: {str(e)}"
        )