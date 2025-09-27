"""
Cover Letter Generator Service
Version: 1.0
Purpose: Generate personalized cover letters for job applications

This microservice provides functionality to:
1. Generate customized cover letters based on user profile and job description
2. Create professional cover letters that align with job requirements
3. Provide personalized content based on user experience and skills
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for the application
# ============================================================================

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Optional

# ============================================================================
# APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata and CORS middleware
# ============================================================================

app = FastAPI(
    title="Cover Letter Generator",
    description="Generate personalized cover letters for job applications",
    version="1.0.0"
)

# Configure CORS middleware to allow cross-origin requests
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

class GenerateRequest(BaseModel):
    """Request model for cover letter generation"""
    user_id: str
    job_id: str
    resume_json: Optional[Dict] = None
    job_description: Optional[str] = None

# ============================================================================
# CORE FUNCTIONS
# Main functions for generating cover letters
# ============================================================================

# ----------------------------------------------------------------------------
# COVER LETTER GENERATION
# Function to generate personalized cover letters
# ----------------------------------------------------------------------------

def generate_cover_letter(user_id: str, job_id: str, resume_data: Optional[Dict], job_description: Optional[str]) -> str:
    """
    Generate a personalized cover letter based on user data and job information
    
    Args:
        user_id (str): Unique identifier for the user
        job_id (str): Unique identifier for the job
        resume_data (Optional[Dict]): User's resume data in JSON format
        job_description (Optional[str]): Job description text
        
    Returns:
        str: Generated cover letter text
    """
    # In a real implementation, this would use AI to generate a personalized cover letter
    # based on the user's resume and the job description
    
    # For now, we'll generate a placeholder that can be expanded later
    cover_letter = f"""Dear Hiring Manager,

I am excited to apply for the position (Job ID: {job_id}) at your company. With my background and skills, I believe I would be a valuable addition to your team.

"""
    
    # Add content based on available information
    if resume_data:
        cover_letter += "Based on my experience and qualifications, I am confident in my ability to contribute to your organization.\n\n"
    else:
        cover_letter += "I am eager to bring my skills and enthusiasm to this role and contribute to your team's success.\n\n"
    
    if job_description:
        cover_letter += "I am particularly drawn to this opportunity because of [specific aspect of the role/company that matches your interests].\n\n"
    
    cover_letter += """I would welcome the opportunity to discuss how my background, skills, and enthusiasms align with your needs. 
Thank you for your consideration, and I look forward to hearing from you.

Sincerely,
[Your Name]"""
    
    return cover_letter

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the cover letter generator service
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
# COVER LETTER GENERATION ENDPOINT
# Endpoint for generating personalized cover letters
# ----------------------------------------------------------------------------

@app.post('/generate')
async def generate(req: GenerateRequest):
    """
    Generate a personalized cover letter for a job application
    
    Args:
        req (GenerateRequest): Request containing user and job information
        
    Returns:
        dict: Generated cover letter text
        
    Example:
        POST /generate
        {
            "user_id": "user123",
            "job_id": "job456",
            "resume_json": {"experience": "...", "skills": "..."},
            "job_description": "We are looking for a software engineer..."
        }
    """
    # Generate the cover letter using the provided information
    cover_letter_text = generate_cover_letter(
        req.user_id, 
        req.job_id, 
        req.resume_json, 
        req.job_description
    )
    
    # Return the generated cover letter
    return {"cover_letter": cover_letter_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)