"""
AI Application Filler Service for MyBrand Job Application Platform
Version: v2
Purpose: Provides AI-powered auto-filling of job application forms using resume data
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for application filling functionality
# ============================================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from typing import Dict, List, Optional, Any

# ============================================================================
# ROUTER CONFIGURATION
# Create router for application filler endpoints with appropriate prefix and tags
# ============================================================================

router = APIRouter(prefix="/ai/application-filler", tags=["AI Application Filler"])

# ============================================================================
# DATA MODELS
# Pydantic models for application filling data structures and API requests/responses
# ============================================================================

class PersonalInfo(BaseModel):
    """
    Personal information for job application.
    
    Contains essential contact information for the job applicant.
    """
    name: str
    email: str
    phone: str
    address: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None

class WorkExperience(BaseModel):
    """
    Work experience entry for job application.
    
    Details about a specific position including company, role, dates, and description.
    """
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    description: str

class Education(BaseModel):
    """
    Education entry for job application.
    
    Details about academic qualifications including institution, degree, and dates.
    """
    institution: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: Optional[str] = None
    gpa: Optional[float] = None

class ApplicationData(BaseModel):
    """
    Complete structured application data.
    
    Organizes all sections of a job application including personal info,
    work experience, education, and skills.
    """
    personal_info: PersonalInfo
    work_experience: List[WorkExperience]
    education: List[Education]
    skills: List[str]
    certifications: List[str] = []
    portfolio_url: Optional[str] = None

class FormField(BaseModel):
    """
    Job application form field definition.
    
    Represents a single field in a job application form with metadata
    for proper data mapping and validation.
    """
    name: str
    label: str
    type: str
    required: bool
    options: Optional[List[str]] = None

class AutoFillRequest(BaseModel):
    """
    Request model for auto-filling job application forms.
    
    Contains resume text and form field definitions to map resume data
    to application form fields.
    """
    resume_text: str
    form_fields: List[FormField]
    target_company: Optional[str] = None

class AutoFillResponse(BaseModel):
    """
    Response model for auto-filled application forms.
    
    Contains the filled form data, confidence scores for each field,
    and a list of any fields that could not be filled.
    """
    filled_data: Dict[str, Any]
    confidence_scores: Dict[str, float]
    missing_fields: List[str]

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for application filling functionality
# ============================================================================

@router.post("/auto-fill", response_model=AutoFillResponse)
async def auto_fill_application(request: AutoFillRequest):
    """
    Auto-fill job application form based on resume.
    
    This endpoint forwards the auto-fill request to a dedicated microservice
    that uses AI to extract information from the resume and map it to the
    provided form fields, generating a completed application form.
    
    Args:
        request (AutoFillRequest): Contains resume text and form field definitions
        
    Returns:
        AutoFillResponse: Filled form data with confidence scores and missing fields
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> form_fields = [
        ...     FormField(name="full_name", label="Full Name", type="text", required=True),
        ...     FormField(name="email", label="Email", type="email", required=True)
        ... ]
        >>> request = AutoFillRequest(
        ...     resume_text="John Doe\\nSoftware Engineer\\nExperience...",
        ...     form_fields=form_fields
        ... )
        >>> response = await auto_fill_application(request)
        >>> print(f"Filled {len(response.filled_data)} fields")
    """
    try:
        # ============================================================================
        # SERVICE DISCOVERY
        # Get the application filler service URL from environment variables
        # ============================================================================
        
        # Get the application filler service URL
        # In development, this would be http://localhost:8109
        # In production, this would be the deployed service URL
        filler_service_url = os.getenv("APPLICATION_FILLER_SERVICE_URL", "http://localhost:8109")
        
        # ============================================================================
        # SERVICE REQUEST
        # Forward the request to the application filler microservice
        # ============================================================================
        
        # Forward the request to the application filler microservice
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{filler_service_url}/auto-fill",
                json=request.dict(),
                timeout=30.0
            )
            
            # Handle non-success responses from the microservice
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Application filler service error: {response.text}"
                )
            
            # Return the auto-filled form data from the microservice
            return response.json()
    except httpx.RequestError as e:
        # Handle connection errors to the microservice
        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to application filler service: {str(e)}"
        )
    except Exception as e:
        # Handle any other unexpected errors during auto-filling
        raise HTTPException(
            status_code=500,
            detail=f"Error auto-filling application: {str(e)}"
        )

@router.post("/extract-data", response_model=ApplicationData)
async def extract_application_data(resume_text: str):
    """
    Extract structured data from resume text.
    
    This endpoint forwards the data extraction request to a dedicated
    microservice that parses resume text and extracts structured
    information organized by application sections.
    
    Args:
        resume_text (str): The raw text content of the resume to parse
        
    Returns:
        ApplicationData: Structured application data extracted from the resume
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> resume_text = "John Doe\\nSoftware Engineer\\nExperience: 5 years..."
        >>> data = await extract_application_data(resume_text)
        >>> print(f"Extracted {len(data.work_experience)} work experiences")
    """
    try:
        # ============================================================================
        # SERVICE DISCOVERY
        # Get the application filler service URL from environment variables
        # ============================================================================
        
        # Get the application filler service URL
        # In development, this would be http://localhost:8109
        # In production, this would be the deployed service URL
        filler_service_url = os.getenv("APPLICATION_FILLER_SERVICE_URL", "http://localhost:8109")
        
        # ============================================================================
        # SERVICE REQUEST
        # Forward the request to the application filler microservice
        # ============================================================================
        
        # Forward the request to the application filler microservice
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{filler_service_url}/extract-data",
                json={"resume_text": resume_text},
                timeout=30.0
            )
            
            # Handle non-success responses from the microservice
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Application filler service error: {response.text}"
                )
            
            # Return the extracted application data from the microservice
            return response.json()
    except httpx.RequestError as e:
        # Handle connection errors to the microservice
        raise HTTPException(
            status_code=503,
            detail=f"Unable to connect to application filler service: {str(e)}"
        )
    except Exception as e:
        # Handle any other unexpected errors during data extraction
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting application data: {str(e)}"
        )