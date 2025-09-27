"""
Semantic Job Matcher Service
Version: 1.0
Purpose: Rank jobs by semantic similarity to candidate's skills and career goals

This microservice provides functionality to:
1. Match job postings to candidate profiles based on semantic similarity
2. Calculate similarity scores using skills, experience, location, and job type
3. Rank jobs by compatibility with candidate preferences
4. Provide detailed explanations of matching results
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for the application
# ============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import re
from collections import Counter

# ============================================================================
# APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata
# ============================================================================

app = FastAPI(
    title="Semantic Job Matcher",
    description="Rank jobs by semantic similarity to candidate's skills and career goals",
    version="1.0.0"
)

# ============================================================================
# DATA MODELS
# Pydantic models for data validation and serialization
# ============================================================================

# ----------------------------------------------------------------------------
# CANDIDATE PROFILE MODELS
# Models for representing candidate information and preferences
# ----------------------------------------------------------------------------

class CandidateProfile(BaseModel):
    """Model for candidate profile information"""
    skills: List[str]
    experience: List[str]
    education: List[str]
    career_goals: List[str]
    preferred_locations: List[str] = []
    job_types: List[str] = []

# ----------------------------------------------------------------------------
# JOB POSTING MODELS
# Models for representing job postings and their attributes
# ----------------------------------------------------------------------------

class JobPosting(BaseModel):
    """Model for job posting information"""
    id: str
    title: str
    company: str
    description: str
    requirements: List[str]
    location: str
    type: str  # "Full-time", "Part-time", "Contract", etc.
    salary: Optional[str] = None
    benefits: List[str] = []

# ----------------------------------------------------------------------------
# MATCHING REQUEST AND RESPONSE MODELS
# Models for job matching requests and responses
# ----------------------------------------------------------------------------

class MatchRequest(BaseModel):
    """Request model for job matching"""
    candidate: CandidateProfile
    jobs: List[JobPosting]

class JobMatch(BaseModel):
    """Model for individual job match results"""
    job_id: str
    similarity_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    explanation: str

class MatchResponse(BaseModel):
    """Response model for job matching results"""
    matches: List[JobMatch]
    recommended_jobs: List[str]  # Job IDs

# ============================================================================
# SKILL VARIATIONS
# Common skills and their variations for better matching
# ============================================================================

# Common skills and their variations
skill_variations = {
    "python": ["python", "python programming", "python development"],
    "javascript": ["javascript", "js", "javascript development"],
    "react": ["react", "react.js", "reactjs"],
    "node.js": ["node.js", "nodejs", "node"],
    "sql": ["sql", "structured query language"],
    "docker": ["docker", "docker containers", "containerization"],
    "aws": ["aws", "amazon web services", "amazon cloud"],
    "machine learning": ["machine learning", "ml", "ai", "artificial intelligence"],
    "data analysis": ["data analysis", "data analytics", "data science"],
    "project management": ["project management", "pm", "agile", "scrum"]
}

# ============================================================================
# TEXT PROCESSING FUNCTIONS
# Functions for normalizing and extracting information from text
# ============================================================================

# ----------------------------------------------------------------------------
# TEXT NORMALIZATION
# Function to normalize text for consistent comparison
# ----------------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """
    Normalize text for comparison by removing punctuation and converting to lowercase
    
    Args:
        text (str): Text to normalize
        
    Returns:
        str: Normalized text
    """
    return re.sub(r'[^\w\s]', '', text.lower())

# ----------------------------------------------------------------------------
# KEYWORD EXTRACTION
# Function to extract keywords from text for similarity calculations
# ----------------------------------------------------------------------------

def extract_keywords(text: str) -> List[str]:
    """
    Extract keywords from text for similarity calculations
    
    Args:
        text (str): Text to extract keywords from
        
    Returns:
        List[str]: List of extracted keywords
    """
    # Simple keyword extraction - in practice, you'd use NLP techniques
    words = normalize_text(text).split()
    # Filter out common stop words
    stop_words = {"the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were"}
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return keywords

# ============================================================================
# SIMILARITY CALCULATION FUNCTIONS
# Functions for calculating similarity between different aspects of profiles
# ============================================================================

# ----------------------------------------------------------------------------
# SKILL SIMILARITY CALCULATION
# Function to calculate similarity between candidate skills and job requirements
# ----------------------------------------------------------------------------

def calculate_skill_similarity(candidate_skills: List[str], job_requirements: List[str]) -> tuple[float, List[str], List[str]]:
    """
    Calculate similarity between candidate skills and job requirements
    
    Args:
        candidate_skills (List[str]): List of candidate's skills
        job_requirements (List[str]): List of job requirements
        
    Returns:
        tuple[float, List[str], List[str]]: Similarity score, matching skills, missing skills
    """
    # Normalize skills for consistent comparison
    candidate_skills_normalized = [normalize_text(skill) for skill in candidate_skills]
    job_requirements_normalized = [normalize_text(req) for req in job_requirements]
    
    # Find matching skills and identify missing ones
    matching_skills = []
    missing_skills = []
    
    for req in job_requirements_normalized:
        matched = False
        # Check for exact matches
        if req in candidate_skills_normalized:
            matching_skills.append(req)
            matched = True
        else:
            # Check for partial matches and variations
            for skill in candidate_skills_normalized:
                if req in skill or skill in req:
                    matching_skills.append(req)
                    matched = True
                    break
                # Check variations
                for base_skill, variations in skill_variations.items():
                    if req in variations and skill in variations:
                        matching_skills.append(req)
                        matched = True
                        break
                if matched:
                    break
        
        if not matched:
            missing_skills.append(req)
    
    # Calculate similarity score as ratio of matching to total requirements
    if not job_requirements_normalized:
        similarity_score = 1.0
    else:
        similarity_score = len(matching_skills) / len(job_requirements_normalized)
    
    return similarity_score, matching_skills, missing_skills

# ----------------------------------------------------------------------------
# EXPERIENCE SIMILARITY CALCULATION
# Function to calculate similarity between candidate experience and job description
# ----------------------------------------------------------------------------

def calculate_experience_similarity(candidate_experience: List[str], job_description: str) -> float:
    """
    Calculate similarity between candidate experience and job description
    
    Args:
        candidate_experience (List[str]): List of candidate's experience entries
        job_description (str): Job description text
        
    Returns:
        float: Similarity score between 0.0 and 1.0
    """
    # Extract keywords from both candidate experience and job description
    candidate_keywords = []
    for exp in candidate_experience:
        candidate_keywords.extend(extract_keywords(exp))
    
    job_keywords = extract_keywords(job_description)
    
    # Count keyword frequencies for both
    candidate_counter = Counter(candidate_keywords)
    job_counter = Counter(job_keywords)
    
    # Calculate similarity using Jaccard similarity coefficient
    intersection = sum((candidate_counter & job_counter).values())
    union = sum((candidate_counter | job_counter).values())
    
    if union == 0:
        return 0.0
    
    return intersection / union

# ----------------------------------------------------------------------------
# LOCATION MATCH CALCULATION
# Function to calculate location match score
# ----------------------------------------------------------------------------

def calculate_location_match(candidate_locations: List[str], job_location: str) -> float:
    """
    Calculate location match score between candidate preferences and job location
    
    Args:
        candidate_locations (List[str]): List of candidate's preferred locations
        job_location (str): Job location
        
    Returns:
        float: Location match score (0.0 = no match, 1.0 = perfect match)
    """
    # If candidate has no location preferences, return full match
    if not candidate_locations:
        return 1.0  # No preference
    
    # Normalize job location for comparison
    job_location_normalized = normalize_text(job_location)
    
    # Check for matches in candidate's preferred locations
    for location in candidate_locations:
        location_normalized = normalize_text(location)
        if location_normalized in job_location_normalized or job_location_normalized in location_normalized:
            return 1.0
    
    return 0.0

# ----------------------------------------------------------------------------
# JOB TYPE MATCH CALCULATION
# Function to calculate job type match score
# ----------------------------------------------------------------------------

def calculate_job_type_match(candidate_job_types: List[str], job_type: str) -> float:
    """
    Calculate job type match score between candidate preferences and job type
    
    Args:
        candidate_job_types (List[str]): List of candidate's preferred job types
        job_type (str): Job type (Full-time, Part-time, Contract, etc.)
        
    Returns:
        float: Job type match score (0.0 = no match, 1.0 = perfect match)
    """
    # If candidate has no job type preferences, return full match
    if not candidate_job_types:
        return 1.0  # No preference
    
    # Normalize job type for comparison
    job_type_normalized = normalize_text(job_type)
    
    # Check for matches in candidate's preferred job types
    for job_type_pref in candidate_job_types:
        job_type_pref_normalized = normalize_text(job_type_pref)
        if job_type_pref_normalized in job_type_normalized or job_type_normalized in job_type_pref_normalized:
            return 1.0
    
    return 0.0

# ============================================================================
# JOB MATCHING FUNCTIONS
# Main functions for matching jobs to candidate profiles
# ============================================================================

# ----------------------------------------------------------------------------
# JOB MATCHING
# Function to match jobs to candidate profile using multiple similarity metrics
# ----------------------------------------------------------------------------

def match_jobs(candidate: CandidateProfile, jobs: List[JobPosting]) -> List[JobMatch]:
    """
    Match jobs to candidate profile using multiple similarity metrics
    
    Args:
        candidate (CandidateProfile): Candidate's profile information
        jobs (List[JobPosting]): List of job postings to match against
        
    Returns:
        List[JobMatch]: List of job matches sorted by similarity score
    """
    matches = []
    
    # Process each job posting for matching
    for job in jobs:
        # Calculate different similarity scores for comprehensive matching
        skill_similarity, matching_skills, missing_skills = calculate_skill_similarity(
            candidate.skills, job.requirements
        )
        
        experience_similarity = calculate_experience_similarity(
            candidate.experience, job.description
        )
        
        location_similarity = calculate_location_match(
            candidate.preferred_locations, job.location
        )
        
        job_type_similarity = calculate_job_type_match(
            candidate.job_types, job.type
        )
        
        # Calculate weighted overall similarity score
        # Skills: 40%, Experience: 30%, Location: 15%, Job Type: 15%
        overall_similarity = (
            skill_similarity * 0.4 +
            experience_similarity * 0.3 +
            location_similarity * 0.15 +
            job_type_similarity * 0.15
        )
        
        # Generate explanation of the match based on similarity scores
        explanation_parts = []
        if skill_similarity > 0.5:
            explanation_parts.append(f"Strong skill match ({int(skill_similarity*100)}%)")
        elif skill_similarity > 0.2:
            explanation_parts.append(f"Moderate skill match ({int(skill_similarity*100)}%)")
        else:
            explanation_parts.append(f"Low skill match ({int(skill_similarity*100)}%)")
        
        if experience_similarity > 0.3:
            explanation_parts.append("Relevant experience")
        
        if location_similarity > 0.5:
            explanation_parts.append("Preferred location")
        
        if job_type_similarity > 0.5:
            explanation_parts.append("Preferred job type")
        
        explanation = ", ".join(explanation_parts)
        
        # Create job match object with all calculated information
        matches.append(JobMatch(
            job_id=job.id,
            similarity_score=overall_similarity,
            matching_skills=matching_skills,
            missing_skills=missing_skills,
            explanation=explanation
        ))
    
    # Sort matches by similarity score in descending order (best matches first)
    matches.sort(key=lambda x: x.similarity_score, reverse=True)
    
    return matches

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the semantic matcher service
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
# SEMANTIC JOB MATCHING ENDPOINT
# Endpoint for performing comprehensive job matching for a candidate
# ----------------------------------------------------------------------------

@app.post("/match", response_model=MatchResponse)
async def semantic_job_matching(request: MatchRequest):
    """
    Perform semantic job matching for a candidate
    
    Args:
        request (MatchRequest): Request containing candidate profile and job postings
        
    Returns:
        MatchResponse: Job matches and recommended job IDs
        
    Example:
        POST /match
        {
            "candidate": {
                "skills": ["Python", "JavaScript", "React"],
                "experience": ["Software Engineer at Tech Corp"],
                "education": ["BS Computer Science"],
                "career_goals": ["Senior Developer"],
                "preferred_locations": ["San Francisco", "Remote"],
                "job_types": ["Full-time"]
            },
            "jobs": [
                {
                    "id": "job123",
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "description": "We are looking for a senior software engineer...",
                    "requirements": ["Python", "JavaScript"],
                    "location": "San Francisco",
                    "type": "Full-time"
                }
            ]
        }
    """
    try:
        # Perform job matching for the candidate
        matches = match_jobs(request.candidate, request.jobs)
        
        # Recommend top 10 jobs based on similarity scores
        recommended_jobs = [match.job_id for match in matches[:10]]
        
        # Return matching results and recommendations
        return MatchResponse(
            matches=matches,
            recommended_jobs=recommended_jobs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing job matching: {str(e)}")

# ----------------------------------------------------------------------------
# JOB RANKING ENDPOINT
# Endpoint for ranking jobs by similarity to candidate profile
# ----------------------------------------------------------------------------

@app.post("/rank", response_model=List[JobMatch])
async def rank_jobs(request: MatchRequest):
    """
    Rank jobs by similarity to candidate profile
    
    Args:
        request (MatchRequest): Request containing candidate profile and job postings
        
    Returns:
        List[JobMatch]: List of job matches sorted by similarity score
        
    Example:
        POST /rank
        {
            "candidate": {
                "skills": ["Python", "JavaScript", "React"],
                "experience": ["Software Engineer at Tech Corp"],
                "education": ["BS Computer Science"],
                "career_goals": ["Senior Developer"]
            },
            "jobs": [
                {
                    "id": "job123",
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "description": "We are looking for a senior software engineer...",
                    "requirements": ["Python", "JavaScript"],
                    "location": "San Francisco",
                    "type": "Full-time"
                }
            ]
        }
    """
    try:
        # Perform job matching and ranking
        matches = match_jobs(request.candidate, request.jobs)
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ranking jobs: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8110)