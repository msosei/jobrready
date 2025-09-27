"""
AI Resume Builder Service
Version: 1.0
Purpose: Generate professional resumes from user data

This microservice provides functionality to:
1. Generate professional resumes from structured user data
2. Create resumes from LinkedIn profile data
3. Support multiple resume templates and formats
4. Provide clean, well-formatted resume output
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for the application
# ============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json

# ============================================================================
# APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata
# ============================================================================

app = FastAPI(
    title="AI Resume Builder",
    description="Generate professional resumes from user data",
    version="1.0.0"
)

# ============================================================================
# DATA MODELS
# Pydantic models for data validation and serialization
# ============================================================================

# ----------------------------------------------------------------------------
# PERSONAL INFORMATION MODEL
# Model for personal contact information
# ----------------------------------------------------------------------------

class PersonalInfo(BaseModel):
    """Model for personal contact information"""
    name: str
    email: str
    phone: str
    address: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

# ----------------------------------------------------------------------------
# EXPERIENCE MODEL
# Model for professional work experience
# ----------------------------------------------------------------------------

class Experience(BaseModel):
    """Model for professional work experience"""
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = "Present"
    description: List[str]
    location: Optional[str] = None

# ----------------------------------------------------------------------------
# EDUCATION MODEL
# Model for educational background
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
# SKILL MODEL
# Model for professional skills
# ----------------------------------------------------------------------------

class Skill(BaseModel):
    """Model for professional skills"""
    name: str
    level: Optional[str] = "Intermediate"  # Beginner, Intermediate, Advanced, Expert

# ----------------------------------------------------------------------------
# PROJECT MODEL
# Model for personal and professional projects
# ----------------------------------------------------------------------------

class Project(BaseModel):
    """Model for personal and professional projects"""
    name: str
    description: str
    technologies: List[str]
    url: Optional[str] = None

# ----------------------------------------------------------------------------
# RESUME DATA MODEL
# Comprehensive model for all resume information
# ----------------------------------------------------------------------------

class ResumeData(BaseModel):
    """Model for complete resume data"""
    personal_info: PersonalInfo
    summary: Optional[str] = None
    experiences: List[Experience]
    education: List[Education]
    skills: List[Skill]
    projects: Optional[List[Project]] = None
    certifications: Optional[List[str]] = None

# ----------------------------------------------------------------------------
# REQUEST/RESPONSE MODELS
# Models for API request and response data
# ----------------------------------------------------------------------------

class ResumeRequest(BaseModel):
    """Request model for resume generation"""
    data: ResumeData
    template: Optional[str] = "professional"  # professional, creative, minimal

class ResumeResponse(BaseModel):
    """Response model for generated resumes"""
    resume_text: str
    format: str  # "txt", "md", "pdf" (we'll generate text-based for now)

# ============================================================================
# RESUME GENERATION FUNCTIONS
# Functions for creating formatted resume output
# ============================================================================

# ----------------------------------------------------------------------------
# TEXT RESUME GENERATION
# Function to generate a formatted resume as text
# ----------------------------------------------------------------------------

def generate_resume_text(data: ResumeData) -> str:
    """
    Generate a formatted resume as text
    
    Args:
        data (ResumeData): Structured resume data to format
        
    Returns:
        str: Formatted resume as text
    """
    # Initialize list for storing resume lines
    resume_lines = []
    
    # ----------------------------------------------------------------------------
    # PERSONAL INFORMATION SECTION
    # Add personal contact information to resume
    # ----------------------------------------------------------------------------
    
    # Add name as the first line
    resume_lines.append(f"{data.personal_info.name}")
    
    # Add contact information
    resume_lines.append(f"Email: {data.personal_info.email} | Phone: {data.personal_info.phone}")
    
    # Add optional address if provided
    if data.personal_info.address:
        resume_lines.append(f"Address: {data.personal_info.address}")
    
    # Add LinkedIn profile if provided
    if data.personal_info.linkedin:
        resume_lines.append(f"LinkedIn: {data.personal_info.linkedin}")
    
    # Add GitHub profile if provided
    if data.personal_info.github:
        resume_lines.append(f"GitHub: {data.personal_info.github}")
    
    # Add blank line for spacing
    resume_lines.append("")
    
    # ----------------------------------------------------------------------------
    # PROFESSIONAL SUMMARY SECTION
    # Add professional summary if provided
    # ----------------------------------------------------------------------------
    
    if data.summary:
        resume_lines.append("PROFESSIONAL SUMMARY")
        resume_lines.append(data.summary)
        resume_lines.append("")
    
    # ----------------------------------------------------------------------------
    # PROFESSIONAL EXPERIENCE SECTION
    # Add work experience details
    # ----------------------------------------------------------------------------
    
    if data.experiences:
        resume_lines.append("PROFESSIONAL EXPERIENCE")
        for exp in data.experiences:
            # Add position, company, and dates
            resume_lines.append(f"{exp.position} | {exp.company} | {exp.start_date} - {exp.end_date}")
            
            # Add location if provided
            if exp.location:
                resume_lines.append(f"Location: {exp.location}")
            
            # Add job description bullet points
            for desc in exp.description:
                resume_lines.append(f"  • {desc}")
            
            # Add blank line for spacing between experiences
            resume_lines.append("")
    
    # ----------------------------------------------------------------------------
    # EDUCATION SECTION
    # Add educational background details
    # ----------------------------------------------------------------------------
    
    if data.education:
        resume_lines.append("EDUCATION")
        for edu in data.education:
            # Format GPA information if provided
            gpa_str = f" | GPA: {edu.gpa}" if edu.gpa else ""
            
            # Format end date information
            end_date_str = f" - {edu.end_date}" if edu.end_date else ""
            
            # Add degree and institution information
            resume_lines.append(f"{edu.degree} in {edu.field_of_study} | {edu.institution}")
            resume_lines.append(f"{edu.start_date}{end_date_str}{gpa_str}")
            
            # Add blank line for spacing between education entries
            resume_lines.append("")
    
    # ----------------------------------------------------------------------------
    # SKILLS SECTION
    # Add professional skills organized by proficiency level
    # ----------------------------------------------------------------------------
    
    if data.skills:
        resume_lines.append("SKILLS")
        
        # Group skills by proficiency level
        skill_groups = {}
        for skill in data.skills:
            if skill.level not in skill_groups:
                skill_groups[skill.level] = []
            skill_groups[skill.level].append(skill.name)
        
        # Add skills organized by level
        for level, skills in skill_groups.items():
            resume_lines.append(f"  {level}: {', '.join(skills)}")
        
        # Add blank line for spacing
        resume_lines.append("")
    
    # ----------------------------------------------------------------------------
    # PROJECTS SECTION
    # Add personal and professional projects
    # ----------------------------------------------------------------------------
    
    if data.projects:
        resume_lines.append("PROJECTS")
        for project in data.projects:
            # Add project name
            resume_lines.append(f"{project.name}")
            
            # Add project description
            resume_lines.append(f"  {project.description}")
            
            # Add technologies used
            resume_lines.append(f"  Technologies: {', '.join(project.technologies)}")
            
            # Add project URL if provided
            if project.url:
                resume_lines.append(f"  URL: {project.url}")
            
            # Add blank line for spacing between projects
            resume_lines.append("")
    
    # ----------------------------------------------------------------------------
    # CERTIFICATIONS SECTION
    # Add professional certifications
    # ----------------------------------------------------------------------------
    
    if data.certifications:
        resume_lines.append("CERTIFICATIONS")
        for cert in data.certifications:
            resume_lines.append(f"  • {cert}")
        resume_lines.append("")
    
    # Join all resume lines with newlines
    return "\n".join(resume_lines)

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the resume builder service
# ============================================================================

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

# ----------------------------------------------------------------------------
# RESUME GENERATION ENDPOINT
# Main endpoint for generating resumes from structured data
# ----------------------------------------------------------------------------

@app.post("/generate", response_model=ResumeResponse)
async def generate_resume(request: ResumeRequest):
    """
    Generate a resume from provided data
    
    Args:
        request (ResumeRequest): Request containing resume data and template preference
        
    Returns:
        ResumeResponse: Generated resume in text format
        
    Example:
        POST /generate
        {
            "data": {
                "personal_info": {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "phone": "(555) 123-4567"
                },
                "experiences": [
                    {
                        "company": "TechCorp",
                        "position": "Software Engineer",
                        "start_date": "2020-01",
                        "end_date": "2023-01",
                        "description": [
                            "Developed web applications using React and Node.js",
                            "Improved application performance by 30%"
                        ]
                    }
                ],
                "education": [
                    {
                        "institution": "University of Technology",
                        "degree": "BS",
                        "field_of_study": "Computer Science",
                        "start_date": "2016-09",
                        "end_date": "2020-05"
                    }
                ],
                "skills": [
                    {"name": "Python", "level": "Advanced"},
                    {"name": "JavaScript", "level": "Intermediate"}
                ]
            },
            "template": "professional"
        }
    """
    try:
        # Generate formatted resume text from provided data
        resume_text = generate_resume_text(request.data)
        
        # Return the generated resume with format information
        return ResumeResponse(resume_text=resume_text, format="txt")
    except Exception as e:
        # Handle any errors during resume generation
        raise HTTPException(status_code=500, detail=f"Error generating resume: {str(e)}")

# ----------------------------------------------------------------------------
# LINKEDIN DATA RESUME GENERATION ENDPOINT
# Endpoint for generating resumes from LinkedIn profile data
# ----------------------------------------------------------------------------

@app.post("/from-linkedin", response_model=ResumeResponse)
async def generate_resume_from_linkedin(linkedin_data: dict):
    """
    Generate a resume from LinkedIn data (simplified implementation)
    
    Args:
        linkedin_data (dict): LinkedIn profile data to convert to resume format
        
    Returns:
        ResumeResponse: Generated resume in text format
        
    Example:
        POST /from-linkedin
        {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "headline": "Software Engineer with 5 years experience",
            "experiences": [
                {
                    "company": "TechCorp",
                    "title": "Software Engineer",
                    "start_date": "2020-01",
                    "end_date": "2023-01",
                    "description": "Developed web applications"
                }
            ],
            "education": [
                {
                    "school": "University of Technology",
                    "degree": "BS",
                    "field_of_study": "Computer Science",
                    "start_date": "2016-09",
                    "end_date": "2020-05"
                }
            ],
            "skills": ["Python", "JavaScript", "React"]
        }
    """
    try:
        # Convert LinkedIn data to our resume format
        resume_data = ResumeData(
            personal_info=PersonalInfo(
                name=linkedin_data.get("name", "John Doe"),
                email=linkedin_data.get("email", "john.doe@example.com"),
                phone=linkedin_data.get("phone", "(555) 123-4567"),
                linkedin=linkedin_data.get("linkedin_url", ""),
                address=linkedin_data.get("location", "")
            ),
            summary=linkedin_data.get("headline", ""),
            experiences=[],
            education=[],
            skills=[],
            projects=[],
            certifications=[]
        )
        
        # Process experiences from LinkedIn data
        if "experiences" in linkedin_data:
            for exp in linkedin_data["experiences"]:
                resume_data.experiences.append(Experience(
                    company=exp.get("company", ""),
                    position=exp.get("title", ""),
                    start_date=exp.get("start_date", ""),
                    end_date=exp.get("end_date", "Present"),
                    description=[exp.get("description", "")],
                    location=exp.get("location", "")
                ))
        
        # Process education from LinkedIn data
        if "education" in linkedin_data:
            for edu in linkedin_data["education"]:
                resume_data.education.append(Education(
                    institution=edu.get("school", ""),
                    degree=edu.get("degree", ""),
                    field_of_study=edu.get("field_of_study", ""),
                    start_date=edu.get("start_date", ""),
                    end_date=edu.get("end_date", "")
                ))
        
        # Process skills from LinkedIn data
        if "skills" in linkedin_data:
            for skill in linkedin_data["skills"]:
                resume_data.skills.append(Skill(
                    name=skill,
                    level="Intermediate"
                ))
        
        # Generate formatted resume text
        resume_text = generate_resume_text(resume_data)
        
        # Return the generated resume with format information
        return ResumeResponse(resume_text=resume_text, format="txt")
    except Exception as e:
        # Handle any errors during LinkedIn data processing
        raise HTTPException(status_code=500, detail=f"Error generating resume from LinkedIn data: {str(e)}")

# ============================================================================
# APPLICATION ENTRY POINT
# Main execution block for running the service
# ============================================================================

if __name__ == "__main__":
    # Import uvicorn for running the ASGI application
    import uvicorn
    
    # Run the FastAPI application with uvicorn
    # Host 0.0.0.0 makes it accessible from outside the container
    # Port 8106 is the designated port for this microservice
    uvicorn.run(app, host="0.0.0.0", port=8106)