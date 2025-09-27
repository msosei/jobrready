"""
Resume Enhancer Service
Version: 1.0
Purpose: Parse and enhance resumes for ATS optimization

This microservice provides functionality to:
1. Parse resumes and extract key sections
2. Analyze resumes for ATS compatibility
3. Provide enhancement suggestions for optimization
4. Generate enhanced resume versions with improved formatting
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for the application
# ============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import re

# ============================================================================
# APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata
# ============================================================================

app = FastAPI(
    title="Resume Enhancer",
    description="Parse and enhance resumes for ATS optimization",
    version="1.0.0"
)

# ============================================================================
# DATA MODELS
# Pydantic models for data validation and serialization
# ============================================================================

# ----------------------------------------------------------------------------
# REQUEST MODELS
# Models for API request data
# ----------------------------------------------------------------------------

class ResumeEnhancementRequest(BaseModel):
    """Request model for resume enhancement"""
    resume_text: str

# ----------------------------------------------------------------------------
# RESPONSE MODELS
# Models for API response data
# ----------------------------------------------------------------------------

class EnhancementSuggestion(BaseModel):
    """Model for individual enhancement suggestions"""
    type: str  # "formatting", "keywords", "phrasing", "structure"
    issue: str
    suggestion: str
    priority: str  # "high", "medium", "low"

class ResumeEnhancementResponse(BaseModel):
    """Response model for enhanced resume results"""
    enhanced_resume: str
    suggestions: List[EnhancementSuggestion]
    ats_score: float  # 0-1 scale

class ResumeParseResponse(BaseModel):
    """Response model for parsed resume data"""
    parsed_data: Dict[str, Any]
    suggestions: List[EnhancementSuggestion]

# ============================================================================
# RESUME PROCESSING FUNCTIONS
# Core functions for parsing, analyzing, and enhancing resumes
# ============================================================================

# ----------------------------------------------------------------------------
# RESUME PARSING
# Function to parse resumes and extract key sections
# ----------------------------------------------------------------------------

def parse_resume(resume_text: str) -> Dict[str, Any]:
    """
    Simple resume parser to extract key sections
    
    Args:
        resume_text (str): Raw resume text to parse
        
    Returns:
        Dict[str, Any]: Dictionary mapping section names to content
    """
    sections = {}
    
    # Define section headers we're looking for
    section_headers = [
        "PROFESSIONAL SUMMARY", "SUMMARY", "PROFESSIONAL EXPERIENCE", "EXPERIENCE", 
        "WORK EXPERIENCE", "EDUCATION", "SKILLS", "PROJECTS", "CERTIFICATIONS"
    ]
    
    # Split text into lines for processing
    lines = resume_text.split('\n')
    
    # Initialize variables for tracking current section
    current_section = None
    section_content = []
    
    # Process each line to identify sections
    for line in lines:
        # Check if this line is a section header
        is_header = False
        for header in section_headers:
            if header.upper() in line.upper():
                # Save previous section if exists
                if current_section:
                    sections[current_section] = '\n'.join(section_content).strip()
                
                # Start new section
                current_section = header.upper()
                section_content = []
                is_header = True
                break
        
        # If not a header, add to current section
        if not is_header and current_section:
            section_content.append(line)
    
    # Don't forget the last section
    if current_section:
        sections[current_section] = '\n'.join(section_content).strip()
    
    return sections

# ----------------------------------------------------------------------------
# ATS COMPATIBILITY ANALYSIS
# Function to analyze resume compatibility with Applicant Tracking Systems
# ----------------------------------------------------------------------------

def analyze_ats_compatibility(resume_text: str) -> float:
    """
    Simple ATS compatibility score (0-1)
    
    Args:
        resume_text (str): Resume text to analyze
        
    Returns:
        float: ATS compatibility score between 0.0 and 1.0
    """
    score = 0.5  # Base score
    
    # Check for common ATS-friendly elements
    if re.search(r'\b\d{4}\b', resume_text):  # Has years
        score += 0.1
    if 'PROFESSIONAL' in resume_text.upper() or 'EXPERIENCE' in resume_text.upper():
        score += 0.1
    if 'SKILLS' in resume_text.upper():
        score += 0.1
    if 'EDUCATION' in resume_text.upper():
        score += 0.1
    if re.search(r'\b\d+\s*(years|months)\b', resume_text, re.IGNORECASE):
        score += 0.1
    
    # Ensure score doesn't exceed 1.0
    return min(score, 1.0)

# ----------------------------------------------------------------------------
# ENHANCEMENT SUGGESTIONS
# Function to generate enhancement suggestions for resumes
# ----------------------------------------------------------------------------

def suggest_enhancements(resume_text: str, parsed_sections: Dict[str, str]) -> List[EnhancementSuggestion]:
    """
    Generate enhancement suggestions for the resume
    
    Args:
        resume_text (str): Raw resume text
        parsed_sections (Dict[str, str]): Parsed resume sections
        
    Returns:
        List[EnhancementSuggestion]: List of enhancement suggestions
    """
    suggestions = []
    
    # Check for missing required sections
    required_sections = ["PROFESSIONAL EXPERIENCE", "EDUCATION", "SKILLS"]
    for section in required_sections:
        if section not in parsed_sections:
            suggestions.append(EnhancementSuggestion(
                type="structure",
                issue=f"Missing {section} section",
                suggestion=f"Add a {section} section to your resume",
                priority="high"
            ))
    
    # Check for action verbs in experience section
    weak_verbs = ["was", "were", "did", "does", "do"]
    strong_verbs = ["managed", "developed", "created", "implemented", "led", "optimized", "designed"]
    
    experience_section = parsed_sections.get("PROFESSIONAL EXPERIENCE", "")
    if experience_section:
        # Count weak and strong verbs
        weak_count = sum(1 for verb in weak_verbs if verb in experience_section.lower())
        strong_count = sum(1 for verb in strong_verbs if verb in experience_section.lower())
        
        # Suggest improvement if weak verbs outnumber strong verbs
        if weak_count > strong_count:
            suggestions.append(EnhancementSuggestion(
                type="phrasing",
                issue="Overuse of weak action verbs",
                suggestion="Replace passive verbs like 'was', 'did' with strong action verbs like 'managed', 'developed', 'created'",
                priority="medium"
            ))
    
    # Check for keyword density in resume
    tech_keywords = ["python", "java", "javascript", "react", "node", "sql", "docker", "aws", "api"]
    keyword_count = sum(1 for keyword in tech_keywords if keyword in resume_text.lower())
    
    # Suggest adding more keywords if density is low
    if keyword_count < 5:
        suggestions.append(EnhancementSuggestion(
            type="keywords",
            issue="Low keyword density",
            suggestion="Include more industry-specific keywords relevant to your target roles",
            priority="medium"
        ))
    
    # Check formatting consistency
    if resume_text.count('\t') > 10:  # Too many tabs
        suggestions.append(EnhancementSuggestion(
            type="formatting",
            issue="Inconsistent formatting",
            suggestion="Use consistent spacing and avoid excessive tab characters",
            priority="low"
        ))
    
    # Check for date information
    date_pattern = r'(19|20)\d{2}'
    dates = re.findall(date_pattern, resume_text)
    if len(dates) < 2:
        suggestions.append(EnhancementSuggestion(
            type="structure",
            issue="Missing dates",
            suggestion="Include start and end dates for all positions and education",
            priority="high"
        ))
    
    return suggestions

# ----------------------------------------------------------------------------
# RESUME ENHANCEMENT
# Function to apply basic enhancements to resumes
# ----------------------------------------------------------------------------

def enhance_resume(resume_text: str, suggestions: List[EnhancementSuggestion]) -> str:
    """
    Apply basic enhancements to the resume
    
    Args:
        resume_text (str): Raw resume text to enhance
        suggestions (List[EnhancementSuggestion]): Enhancement suggestions to apply
        
    Returns:
        str: Enhanced resume text
    """
    enhanced_text = resume_text
    
    # This is a simplified enhancement - in a real implementation,
    # you would apply more sophisticated transformations
    
    # Ensure standard section headers for better ATS compatibility
    enhanced_text = re.sub(r'(?i)work experience|job history', 'PROFESSIONAL EXPERIENCE', enhanced_text)
    enhanced_text = re.sub(r'(?i)profile|summary', 'PROFESSIONAL SUMMARY', enhanced_text)
    
    return enhanced_text

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the resume enhancer service
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
# RESUME PARSING ENDPOINT
# Endpoint for parsing resumes and providing suggestions
# ----------------------------------------------------------------------------

@app.post("/parse", response_model=ResumeParseResponse)
async def parse_resume_endpoint(request: ResumeEnhancementRequest):
    """
    Parse a resume and provide suggestions
    
    Args:
        request (ResumeEnhancementRequest): Request containing resume text
        
    Returns:
        ResumeParseResponse: Parsed resume data and enhancement suggestions
        
    Example:
        POST /parse
        {
            "resume_text": "John Doe\nEmail: john@example.com\nPROFESSIONAL EXPERIENCE\n..."
        }
    """
    try:
        # Parse the resume into sections
        parsed_data = parse_resume(request.resume_text)
        
        # Generate enhancement suggestions based on parsed data
        suggestions = suggest_enhancements(request.resume_text, parsed_data)
        
        # Return parsed data and suggestions
        return ResumeParseResponse(
            parsed_data=parsed_data,
            suggestions=suggestions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")

# ----------------------------------------------------------------------------
# RESUME ENHANCEMENT ENDPOINT
# Endpoint for enhancing resumes with ATS optimization
# ----------------------------------------------------------------------------

@app.post("/enhance", response_model=ResumeEnhancementResponse)
async def enhance_resume_endpoint(request: ResumeEnhancementRequest):
    """
    Enhance a resume for better ATS compatibility
    
    Args:
        request (ResumeEnhancementRequest): Request containing resume text
        
    Returns:
        ResumeEnhancementResponse: Enhanced resume and improvement suggestions
        
    Example:
        POST /enhance
        {
            "resume_text": "John Doe\nEmail: john@example.com\nPROFESSIONAL EXPERIENCE\n..."
        }
    """
    try:
        # Parse the resume into sections
        parsed_data = parse_resume(request.resume_text)
        
        # Generate enhancement suggestions
        suggestions = suggest_enhancements(request.resume_text, parsed_data)
        
        # Apply enhancements to the resume
        enhanced_resume = enhance_resume(request.resume_text, suggestions)
        
        # Calculate ATS compatibility score
        ats_score = analyze_ats_compatibility(enhanced_resume)
        
        # Return enhanced resume, suggestions, and ATS score
        return ResumeEnhancementResponse(
            enhanced_resume=enhanced_resume,
            suggestions=suggestions,
            ats_score=ats_score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enhancing resume: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
