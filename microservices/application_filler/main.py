"""
Job Application Auto-Fill Service
Version: 1.0
Purpose: Extract data from resume/profile and auto-fill application forms

This microservice provides functionality to:
1. Parse resume text and extract structured data
2. Auto-fill job application forms based on extracted data
3. Provide confidence scores for filled fields
4. Identify missing required fields
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for the application
# ============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import re

# ============================================================================
# APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata
# ============================================================================

app = FastAPI(
    title="Job Application Auto-Fill",
    description="Extract data from resume/profile and auto-fill application forms",
    version="1.0.0"
)

# ============================================================================
# DATA MODELS
# Pydantic models for data validation and serialization
# ============================================================================

# ----------------------------------------------------------------------------
# PERSONAL INFORMATION MODEL
# Represents personal contact and profile information
# ----------------------------------------------------------------------------

class PersonalInfo(BaseModel):
    """Model for personal contact information"""
    name: str
    email: str
    phone: str
    address: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None

# ----------------------------------------------------------------------------
# WORK EXPERIENCE MODEL
# Represents professional work history
# ----------------------------------------------------------------------------

class WorkExperience(BaseModel):
    """Model for work experience entries"""
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    description: str

# ----------------------------------------------------------------------------
# EDUCATION MODEL
# Represents educational background
# ----------------------------------------------------------------------------

class Education(BaseModel):
    """Model for educational qualifications"""
    institution: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: Optional[str] = None
    gpa: Optional[float] = None

# ----------------------------------------------------------------------------
# APPLICATION DATA MODEL
# Comprehensive model for all extracted application data
# ----------------------------------------------------------------------------

class ApplicationData(BaseModel):
    """Model for complete application data extracted from resume"""
    personal_info: PersonalInfo
    work_experience: List[WorkExperience]
    education: List[Education]
    skills: List[str]
    certifications: List[str] = []
    portfolio_url: Optional[str] = None

# ----------------------------------------------------------------------------
# FORM FIELD MODEL
# Represents a field in a job application form
# ----------------------------------------------------------------------------

class FormField(BaseModel):
    """Model for job application form fields"""
    name: str
    label: str
    type: str  # "text", "email", "phone", "textarea", "select", "checkbox", "radio"
    required: bool
    options: Optional[List[str]] = None  # For select, checkbox, radio

# ----------------------------------------------------------------------------
# REQUEST/RESPONSE MODELS
# Models for API request and response data
# ----------------------------------------------------------------------------

class AutoFillRequest(BaseModel):
    """Model for auto-fill request parameters"""
    resume_text: str
    form_fields: List[FormField]
    target_company: Optional[str] = None

class AutoFillResponse(BaseModel):
    """Model for auto-fill response data"""
    filled_data: Dict[str, Any]
    confidence_scores: Dict[str, float]
    missing_fields: List[str]

# ============================================================================
# DATA EXTRACTION FUNCTIONS
# Functions to extract specific data types from resume text
# ============================================================================

# ----------------------------------------------------------------------------
# PERSONAL INFO EXTRACTION
# Extract contact information from resume text
# ----------------------------------------------------------------------------

def extract_personal_info(resume_text: str) -> PersonalInfo:
    """
    Extract personal information from resume text
    
    Args:
        resume_text (str): The full text content of the resume
        
    Returns:
        PersonalInfo: Structured personal information object
    """
    lines = resume_text.split('\n')
    
    # Extract name (first non-empty line)
    name = ""
    for line in lines:
        if line.strip() and not name:
            name = line.strip()
            break
    
    # Extract email using regex pattern
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text)
    email = email_match.group() if email_match else ""
    
    # Extract phone number using regex pattern
    phone_match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', resume_text)
    phone = phone_match.group() if phone_match else ""
    
    # Extract LinkedIn profile URL
    linkedin_match = re.search(r'(linkedin\.com/in/[\w-]+)', resume_text, re.IGNORECASE)
    linkedin = linkedin_match.group() if linkedin_match else ""
    if linkedin and not linkedin.startswith("http"):
        linkedin = "https://www." + linkedin
    
    # Extract GitHub profile URL
    github_match = re.search(r'(github\.com/[\w-]+)', resume_text, re.IGNORECASE)
    github = github_match.group() if github_match else ""
    if github and not github.startswith("http"):
        github = "https://www." + github
    
    # Return structured personal information
    return PersonalInfo(
        name=name,
        email=email,
        phone=phone,
        linkedin=linkedin,
        github=github
    )

# ----------------------------------------------------------------------------
# WORK EXPERIENCE EXTRACTION
# Extract professional experience from resume text
# ----------------------------------------------------------------------------

def extract_work_experience(resume_text: str) -> List[WorkExperience]:
    """
    Extract work experience from resume text
    
    Args:
        resume_text (str): The full text content of the resume
        
    Returns:
        List[WorkExperience]: List of work experience objects
    """
    experiences = []
    
    # Look for experience section in the resume
    experience_section = ""
    lines = resume_text.split('\n')
    in_experience = False
    
    # Parse resume to find experience section
    for line in lines:
        if any(keyword in line.upper() for keyword in ["EXPERIENCE", "WORK", "EMPLOYMENT"]):
            in_experience = True
            continue
        elif in_experience and any(keyword in line.upper() for keyword in ["EDUCATION", "SKILLS", "PROJECTS"]):
            break
        elif in_experience:
            experience_section += line + "\n"
    
    # Simple parsing of experience entries (this would be more sophisticated in practice)
    # Look for patterns like "Company | Position | Date"
    experience_pattern = r'(.+?)\s*[|]\s*(.+?)\s*[|]\s*(.+?)(?:\s*[|]\s*(.+?))?$'
    matches = re.findall(experience_pattern, experience_section, re.MULTILINE)
    
    # Create work experience objects from matches
    for match in matches[:3]:  # Limit to 3 experiences
        company, position, date_range = match[0], match[1], match[2]
        experiences.append(WorkExperience(
            company=company.strip(),
            position=position.strip(),
            start_date=date_range.split('-')[0].strip() if '-' in date_range else date_range.strip(),
            end_date=date_range.split('-')[1].strip() if '-' in date_range else None,
            description=f"Worked as {position} at {company}"
        ))
    
    return experiences

# ----------------------------------------------------------------------------
# EDUCATION EXTRACTION
# Extract educational background from resume text
# ----------------------------------------------------------------------------

def extract_education(resume_text: str) -> List[Education]:
    """
    Extract education from resume text
    
    Args:
        resume_text (str): The full text content of the resume
        
    Returns:
        List[Education]: List of education objects
    """
    education = []
    
    # Look for education section in the resume
    education_section = ""
    lines = resume_text.split('\n')
    in_education = False
    
    # Parse resume to find education section
    for line in lines:
        if "EDUCATION" in line.upper():
            in_education = True
            continue
        elif in_education and any(keyword in line.upper() for keyword in ["EXPERIENCE", "SKILLS", "WORK"]):
            break
        elif in_education:
            education_section += line + "\n"
    
    # Simple parsing of education entries
    # Look for patterns like "Degree, Institution, Date"
    education_pattern = r'(.+?),\s*(.+?)(?:,\s*(.+?))?$'
    matches = re.findall(education_pattern, education_section, re.MULTILINE)
    
    # Create education objects from matches
    for match in matches[:2]:  # Limit to 2 education entries
        degree, institution = match[0], match[1]
        education.append(Education(
            institution=institution.strip(),
            degree=degree.strip(),
            field_of_study="",  # Would need more sophisticated parsing
            start_date="",  # Would need more sophisticated parsing
            end_date=None
        ))
    
    return education

# ----------------------------------------------------------------------------
# SKILLS EXTRACTION
# Extract technical and professional skills from resume text
# ----------------------------------------------------------------------------

def extract_skills(resume_text: str) -> List[str]:
    """
    Extract skills from resume text
    
    Args:
        resume_text (str): The full text content of the resume
        
    Returns:
        List[str]: List of extracted skills
    """
    skills = []
    
    # Look for skills section in the resume
    skills_section = ""
    lines = resume_text.split('\n')
    in_skills = False
    
    # Parse resume to find skills section
    for line in lines:
        if "SKILLS" in line.upper():
            in_skills = True
            continue
        elif in_skills and any(keyword in line.upper() for keyword in ["EDUCATION", "EXPERIENCE", "WORK"]):
            break
        elif in_skills:
            skills_section += line + "\n"
    
    # Simple skill extraction (this would be more sophisticated in practice)
    common_skills = [
        "python", "java", "javascript", "react", "node.js", "sql", "docker", "kubernetes",
        "aws", "azure", "gcp", "tensorflow", "pytorch", "machine learning", "data analysis",
        "api", "rest", "graphql", "ci/cd", "git", "agile", "scrum", "project management"
    ]
    
    # Match common skills in the skills section
    skills_text = skills_section.lower()
    for skill in common_skills:
        if skill in skills_text:
            skills.append(skill.title())
    
    return skills

# ============================================================================
# FORM AUTO-FILL FUNCTION
# Main function to auto-fill application forms
# ============================================================================

def auto_fill_form(resume_text: str, form_fields: List[FormField]) -> tuple[Dict[str, Any], Dict[str, float], List[str]]:
    """
    Auto-fill form fields based on resume data
    
    Args:
        resume_text (str): The full text content of the resume
        form_fields (List[FormField]): List of form fields to fill
        
    Returns:
        tuple[Dict[str, Any], Dict[str, float], List[str]]: 
            - Filled data dictionary
            - Confidence scores for each field
            - List of missing required fields
    """
    # Extract data from resume using helper functions
    personal_info = extract_personal_info(resume_text)
    work_experience = extract_work_experience(resume_text)
    education = extract_education(resume_text)
    skills = extract_skills(resume_text)
    
    # Prepare data structures for results
    filled_data = {}
    confidence_scores = {}
    missing_fields = []
    
    # Create mappings between form fields and extracted data
    field_mappings = {
        "name": personal_info.name,
        "full_name": personal_info.name,
        "email": personal_info.email,
        "phone": personal_info.phone,
        "address": personal_info.address or "",
        "linkedin": personal_info.linkedin or "",
        "github": personal_info.github or "",
        "website": personal_info.website or "",
        "current_company": work_experience[0].company if work_experience else "",
        "current_position": work_experience[0].position if work_experience else "",
        "experience": work_experience[0].description if work_experience else "",
        "education": education[0].degree + " from " + education[0].institution if education else "",
        "skills": ", ".join(skills[:10]) if skills else ""  # Limit to 10 skills
    }
    
    # Fill form fields based on mappings
    for field in form_fields:
        field_key = field.name.lower()
        value_found = False
        
        # Direct mapping for exact field name matches
        if field_key in field_mappings and field_mappings[field_key]:
            filled_data[field.name] = field_mappings[field_key]
            confidence_scores[field.name] = 0.9
            value_found = True
        
        # Fuzzy matching for similar field names
        if not value_found:
            for key, value in field_mappings.items():
                if value and (key in field_key or field_key in key) and value:
                    filled_data[field.name] = value
                    confidence_scores[field.name] = 0.7
                    value_found = True
                    break
        
        # Handle missing values for required fields
        if not value_found:
            if field.required:
                missing_fields.append(field.name)
            # For non-required fields, leave them empty
            filled_data[field.name] = ""
            confidence_scores[field.name] = 0.0
    
    # Return the filled form data, confidence scores, and missing fields
    return filled_data, confidence_scores, missing_fields

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the application auto-fill service
# ============================================================================

# ----------------------------------------------------------------------------
# AUTO-FILL ENDPOINT
# Main endpoint for auto-filling job application forms
# ----------------------------------------------------------------------------

@app.post("/auto-fill", response_model=AutoFillResponse)
async def auto_fill_application(request: AutoFillRequest):
    """
    Auto-fill job application form based on resume
    
    Args:
        request (AutoFillRequest): Request containing resume text and form fields
        
    Returns:
        AutoFillResponse: Response with filled data, confidence scores, and missing fields
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        # Process the auto-fill request
        filled_data, confidence_scores, missing_fields = auto_fill_form(
            request.resume_text, request.form_fields
        )
        
        # Return the response with filled data
        return AutoFillResponse(
            filled_data=filled_data,
            confidence_scores=confidence_scores,
            missing_fields=missing_fields
        )
    except Exception as e:
        # Handle any errors during processing
        raise HTTPException(status_code=500, detail=f"Error auto-filling application: {str(e)}")

# ----------------------------------------------------------------------------
# DATA EXTRACTION ENDPOINT
# Endpoint for extracting structured data from resume text
# ----------------------------------------------------------------------------

@app.post("/extract-data", response_model=ApplicationData)
async def extract_application_data(resume_text: str):
    """
    Extract structured data from resume text
    
    Args:
        resume_text (str): The full text content of the resume
        
    Returns:
        ApplicationData: Structured application data extracted from resume
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        # Extract all data types from the resume
        personal_info = extract_personal_info(resume_text)
        work_experience = extract_work_experience(resume_text)
        education = extract_education(resume_text)
        skills = extract_skills(resume_text)
        
        # Return structured application data
        return ApplicationData(
            personal_info=personal_info,
            work_experience=work_experience,
            education=education,
            skills=skills
        )
    except Exception as e:
        # Handle any errors during processing
        raise HTTPException(status_code=500, detail=f"Error extracting application data: {str(e)}")

# ----------------------------------------------------------------------------
# HEALTH CHECK ENDPOINT
# Endpoint for checking service health status
# ----------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring service status
    
    Returns:
        dict: Health status information
    """
    return {"status": "healthy"}

# ============================================================================
# APPLICATION ENTRY POINT
# Main execution block for running the service
# ============================================================================

if __name__ == "__main__":
    # Import uvicorn for running the ASGI application
    import uvicorn
    
    # Run the FastAPI application with uvicorn
    # Host 0.0.0.0 makes it accessible from outside the container
    # Port 8109 is the designated port for this microservice
    uvicorn.run(app, host="0.0.0.0", port=8109)