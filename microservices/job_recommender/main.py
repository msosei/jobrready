"""
Personalized Job Recommender Service
Version: 1.0
Purpose: Generate personalized job recommendations based on career trajectory and preferences

This microservice provides functionality to:
1. Generate personalized job recommendations using advanced matching algorithms
2. Categorize recommendations by type (career growth, skill match, etc.)
3. Adjust recommendations based on user activity history
4. Provide personalized job feeds for different user needs
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for the application
# ============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import random
from datetime import datetime, timedelta

# ============================================================================
# APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata
# ============================================================================

app = FastAPI(
    title="Personalized Job Recommender",
    description="Generate personalized job recommendations based on career trajectory and preferences",
    version="1.0.0"
)

# ============================================================================
# DATA MODELS
# Pydantic models for data validation and serialization
# ============================================================================

# ----------------------------------------------------------------------------
# USER ACTIVITY MODEL
# Model for tracking user interactions with job postings
# ----------------------------------------------------------------------------

class UserActivity(BaseModel):
    """Model for user activity with job postings"""
    job_id: str
    action: str  # "viewed", "applied", "saved", "dismissed"
    timestamp: str

# ----------------------------------------------------------------------------
# USER PREFERENCES MODEL
# Model for user job search preferences
# ----------------------------------------------------------------------------

class UserPreferences(BaseModel):
    """Model for user job search preferences"""
    preferred_roles: List[str]
    preferred_industries: List[str]
    preferred_locations: List[str]
    job_types: List[str]
    salary_range: Optional[Dict[str, int]] = None  # {"min": 50000, "max": 100000}
    experience_level: str  # "entry", "mid", "senior", "executive"

# ----------------------------------------------------------------------------
# JOB POSTING MODEL
# Model for job posting information
# ----------------------------------------------------------------------------

class JobPosting(BaseModel):
    """Model for job posting information"""
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

# ----------------------------------------------------------------------------
# CAREER TRAJECTORY MODEL
# Model for user's career history and goals
# ----------------------------------------------------------------------------

class CareerTrajectory(BaseModel):
    """Model for user's career trajectory"""
    current_role: str
    years_experience: int
    skills: List[str]
    career_goals: List[str]
    past_roles: List[Dict[str, Any]]  # [{"role": "string", "duration": "string", "achievements": ["string"]}]

# ----------------------------------------------------------------------------
# REQUEST/RESPONSE MODELS
# Models for API request and response data
# ----------------------------------------------------------------------------

class RecommendationRequest(BaseModel):
    """Request model for job recommendations"""
    user_id: str
    career_trajectory: CareerTrajectory
    preferences: UserPreferences
    activity_history: List[UserActivity]
    job_pool: List[JobPosting]

class JobRecommendation(BaseModel):
    """Model for individual job recommendations"""
    job_id: str
    title: str
    company: str
    location: str
    match_score: float
    reasons: List[str]
    recommendation_type: str  # "for_you", "career_growth", "skill_match", "new_opportunity"
    apply_probability: float  # 0-1 scale

class RecommendationResponse(BaseModel):
    """Response model for job recommendations"""
    recommendations: List[JobRecommendation]
    personalized_feed: List[JobRecommendation]  # Top recommendations for "For You" feed
    career_growth_opportunities: List[JobRecommendation]
    skill_based_matches: List[JobRecommendation]
    new_opportunities: List[JobRecommendation]

# ============================================================================
# RECOMMENDATION ALGORITHMS
# Core functions for generating personalized job recommendations
# ============================================================================

# ----------------------------------------------------------------------------
# BASE MATCH SCORE CALCULATION
# Function to calculate initial match score between user and job
# ----------------------------------------------------------------------------

def calculate_base_match_score(user_preferences: UserPreferences, job: JobPosting, career_trajectory: CareerTrajectory) -> float:
    """
    Calculate base match score between user and job
    
    Args:
        user_preferences (UserPreferences): User's job search preferences
        job (JobPosting): Job posting to match against
        career_trajectory (CareerTrajectory): User's career history and goals
        
    Returns:
        float: Match score between 0.0 and 1.0
    """
    score = 0.0
    
    # Location match (20% weight)
    if job.location in user_preferences.preferred_locations or job.is_remote:
        score += 0.2
    
    # Job type match (15% weight)
    if job.type in user_preferences.job_types:
        score += 0.15
    
    # Industry match (15% weight)
    if job.industry in user_preferences.preferred_industries:
        score += 0.15
    
    # Role match (20% weight)
    for role in user_preferences.preferred_roles:
        if role.lower() in job.title.lower() or role.lower() in job.description.lower():
            score += 0.2
            break
    
    # Experience level match (10% weight)
    if job.experience_level == user_preferences.experience_level:
        score += 0.1
    
    # Salary match (10% weight)
    if user_preferences.salary_range:
        # Simplified salary matching - in practice, you'd parse salary strings
        score += 0.1 * random.random()  # Random for demo purposes
    
    # Skills match (10% weight)
    skill_matches = 0
    for skill in career_trajectory.skills:
        for requirement in job.requirements:
            if skill.lower() in requirement.lower():
                skill_matches += 1
                break
    
    if job.requirements:
        score += 0.1 * (skill_matches / len(job.requirements))
    
    # Ensure score is between 0.0 and 1.0
    return min(score, 1.0)

# ----------------------------------------------------------------------------
# ACTIVITY HISTORY ADJUSTMENT
# Function to adjust scores based on user's activity history
# ----------------------------------------------------------------------------

def adjust_for_activity_history(score: float, job_id: str, activity_history: List[UserActivity]) -> float:
    """
    Adjust score based on user's activity history with similar jobs
    
    Args:
        score (float): Initial match score
        job_id (str): ID of the job being scored
        activity_history (List[UserActivity]): User's history of job interactions
        
    Returns:
        float: Adjusted match score between 0.0 and 1.0
    """
    # Find recent activities with this job or similar jobs (within last 30 days)
    recent_activities = [
        activity for activity in activity_history 
        if datetime.fromisoformat(activity.timestamp) > datetime.now() - timedelta(days=30)
    ]
    
    # Adjust score based on user's past interactions
    for activity in recent_activities:
        if activity.job_id == job_id:
            if activity.action == "applied":
                # Boost score for jobs in the same category (user showed interest)
                score += 0.1
            elif activity.action == "dismissed":
                # Reduce score for jobs user has dismissed (user showed disinterest)
                score -= 0.2
            elif activity.action == "saved":
                # Slight boost for saved jobs (user showed moderate interest)
                score += 0.05
    
    # Ensure score is between 0.0 and 1.0
    return max(0.0, min(score, 1.0))

# ----------------------------------------------------------------------------
# CAREER GROWTH OPPORTUNITIES IDENTIFICATION
# Function to identify jobs representing career growth opportunities
# ----------------------------------------------------------------------------

def identify_career_growth_opportunities(career_trajectory: CareerTrajectory, jobs: List[JobPosting]) -> List[JobPosting]:
    """
    Identify jobs that represent career growth opportunities
    
    Args:
        career_trajectory (CareerTrajectory): User's career history and goals
        jobs (List[JobPosting]): List of job postings to analyze
        
    Returns:
        List[JobPosting]: List of jobs representing career growth opportunities
    """
    growth_opportunities = []
    
    # Simple heuristic: jobs that require more experience or are in adjacent roles
    current_experience = career_trajectory.years_experience
    
    # Identify growth opportunities based on job titles
    for job in jobs:
        # Jobs requiring more seniority level
        if "senior" in job.title.lower() and "senior" not in career_trajectory.current_role.lower():
            growth_opportunities.append(job)
        elif "lead" in job.title.lower() and "lead" not in career_trajectory.current_role.lower():
            growth_opportunities.append(job)
        elif "manager" in job.title.lower() and "manager" not in career_trajectory.current_role.lower():
            growth_opportunities.append(job)
    
    return growth_opportunities

# ----------------------------------------------------------------------------
# RECOMMENDATION GENERATION
# Main function to generate personalized job recommendations
# ----------------------------------------------------------------------------

def generate_recommendations(request: RecommendationRequest) -> RecommendationResponse:
    """
    Generate personalized job recommendations
    
    Args:
        request (RecommendationRequest): Request containing user data and job pool
        
    Returns:
        RecommendationResponse: Personalized job recommendations categorized by type
    """
    recommendations = []
    
    # Calculate match scores for all jobs in the pool
    for job in request.job_pool:
        base_score = calculate_base_match_score(request.preferences, job, request.career_trajectory)
        adjusted_score = adjust_for_activity_history(base_score, job.id, request.activity_history)
        
        # Generate reasons for recommendation
        reasons = []
        if job.location in request.preferences.preferred_locations or job.is_remote:
            reasons.append("Matches your preferred location")
        if job.type in request.preferences.job_types:
            reasons.append("Matches your preferred job type")
        if any(role.lower() in job.title.lower() for role in request.preferences.preferred_roles):
            reasons.append("Matches your preferred role")
        if job.industry in request.preferences.preferred_industries:
            reasons.append("In your preferred industry")
        
        # Determine recommendation type
        recommendation_type = "for_you"  # Default
        
        # Check if it's a career growth opportunity
        growth_jobs = identify_career_growth_opportunities(request.career_trajectory, [job])
        if growth_jobs:
            recommendation_type = "career_growth"
        
        # Check if it's a skill-based match
        skill_matches = sum(1 for skill in request.career_trajectory.skills 
                           if any(skill.lower() in req.lower() for req in job.requirements))
        if skill_matches > len(job.requirements) * 0.5:
            recommendation_type = "skill_match"
        
        # Apply probability (simplified)
        apply_probability = min(adjusted_score + 0.2 * random.random(), 1.0)
        
        recommendations.append(JobRecommendation(
            job_id=job.id,
            title=job.title,
            company=job.company,
            location=job.location,
            match_score=adjusted_score,
            reasons=reasons,
            recommendation_type=recommendation_type,
            apply_probability=apply_probability
        ))
    
    # Sort by match score in descending order (highest scores first)
    recommendations.sort(key=lambda x: x.match_score, reverse=True)
    
    # Categorize recommendations
    personalized_feed = [rec for rec in recommendations if rec.recommendation_type == "for_you"][:10]
    career_growth_opportunities = [rec for rec in recommendations if rec.recommendation_type == "career_growth"][:5]
    skill_based_matches = [rec for rec in recommendations if rec.recommendation_type == "skill_match"][:5]
    new_opportunities = [rec for rec in recommendations if rec.recommendation_type == "new_opportunity"][:5]
    
    # If we don't have enough in each category, fill from the general recommendations
    while len(personalized_feed) < 10 and recommendations:
        personalized_feed.append(recommendations.pop(0))
    
    # Return the recommendation response with all categorized recommendations
    return RecommendationResponse(
        recommendations=recommendations[:20],  # Top 20 overall
        personalized_feed=personalized_feed,
        career_growth_opportunities=career_growth_opportunities,
        skill_based_matches=skill_based_matches,
        new_opportunities=new_opportunities
    )

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the job recommender service
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
# JOB RECOMMENDATIONS ENDPOINT
# Main endpoint for getting personalized job recommendations
# ----------------------------------------------------------------------------

@app.post("/recommend", response_model=RecommendationResponse)
async def get_job_recommendations(request: RecommendationRequest):
    """
    Get personalized job recommendations for a user
    
    Args:
        request (RecommendationRequest): Request containing user data and job pool
        
    Returns:
        RecommendationResponse: Personalized job recommendations categorized by type
        
    Example:
        POST /recommend
        {
            "user_id": "user123",
            "career_trajectory": {
                "current_role": "Software Engineer",
                "years_experience": 3,
                "skills": ["Python", "JavaScript", "React"],
                "career_goals": ["Become a senior developer"],
                "past_roles": []
            },
            "preferences": {
                "preferred_roles": ["Software Engineer", "Developer"],
                "preferred_industries": ["Technology", "Finance"],
                "preferred_locations": ["San Francisco", "Remote"],
                "job_types": ["Full-time"],
                "experience_level": "mid"
            },
            "activity_history": [],
            "job_pool": [
                {
                    "id": "job1",
                    "title": "Senior Software Engineer",
                    "company": "TechCorp",
                    "location": "San Francisco",
                    "type": "Full-time",
                    "description": "Looking for experienced software engineers",
                    "requirements": ["Python", "Django", "AWS"],
                    "posted_date": "2023-01-01",
                    "is_remote": false,
                    "industry": "Technology",
                    "experience_level": "senior"
                }
            ]
        }
    """
    try:
        # Generate personalized recommendations
        recommendations = generate_recommendations(request)
        return recommendations
    except Exception as e:
        # Handle any errors during recommendation generation
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

# ----------------------------------------------------------------------------
# PERSONALIZED FEED ENDPOINT
# Endpoint for getting personalized "For You" job feed
# ----------------------------------------------------------------------------

@app.post("/for-you", response_model=List[JobRecommendation])
async def get_for_you_feed(request: RecommendationRequest):
    """
    Get personalized 'For You' job feed
    
    Args:
        request (RecommendationRequest): Request containing user data and job pool
        
    Returns:
        List[JobRecommendation]: Personalized job recommendations for "For You" feed
        
    Example:
        POST /for-you
        {
            "user_id": "user123",
            "career_trajectory": {...},
            "preferences": {...},
            "activity_history": [],
            "job_pool": [...]
        }
    """
    try:
        # Generate personalized recommendations and return only the "For You" feed
        recommendations = generate_recommendations(request)
        return recommendations.personalized_feed
    except Exception as e:
        # Handle any errors during feed generation
        raise HTTPException(status_code=500, detail=f"Error generating 'For You' feed: {str(e)}")

# ============================================================================
# APPLICATION ENTRY POINT
# Main execution block for running the service
# ============================================================================

if __name__ == "__main__":
    # Import uvicorn for running the ASGI application
    import uvicorn
    
    # Run the FastAPI application with uvicorn
    # Host 0.0.0.0 makes it accessible from outside the container
    # Port 8111 is the designated port for this microservice
    uvicorn.run(app, host="0.0.0.0", port=8111)