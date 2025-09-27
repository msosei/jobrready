"""
Course Recommendation Engine Service
Version: 1.0
Purpose: AI-powered recommendation engine for courses and learning paths based on skill gaps and career goals

This microservice provides functionality to:
1. Assess skill gaps based on target roles
2. Recommend courses for skill development
3. Generate personalized learning paths
4. Track learning progress
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for the application
# ============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import random

# ============================================================================
# APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata
# ============================================================================

app = FastAPI(
    title="Course Recommendation Engine",
    description="AI-powered recommendation engine for courses and learning paths based on skill gaps and career goals",
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

class SkillAssessmentRequest(BaseModel):
    """Request model for skill assessment"""
    current_skills: List[str]
    target_role: str
    experience_level: str  # Entry-level, Mid-level, Senior-level
    learning_preferences: Optional[List[str]] = None  # self_paced, instructor_led, hands_on, etc.

class CourseRecommendationRequest(BaseModel):
    """Request model for course recommendations"""
    user_id: str
    skills_to_learn: List[str]
    career_goal: str
    budget: Optional[float] = None
    time_commitment: Optional[str] = None  # hours_per_week

class LearningPathRequest(BaseModel):
    """Request model for learning path generation"""
    target_role: str
    current_skills: List[str]
    experience_level: str
    timeline: str  # short_term, medium_term, long_term

class CourseProgressRequest(BaseModel):
    """Request model for course progress tracking"""
    user_id: str
    course_id: str
    progress: float  # 0-100

# ----------------------------------------------------------------------------
# RESPONSE MODELS
# Models for API response data
# ----------------------------------------------------------------------------

class SkillAssessmentResponse(BaseModel):
    """Response model for skill assessment results"""
    skill_gaps: List[str]
    recommended_skills: List[str]
    proficiency_levels: Dict[str, str]  # beginner, intermediate, advanced, expert
    learning_priority: List[str]

class CourseRecommendationResponse(BaseModel):
    """Response model for course recommendations"""
    courses: List[Dict[str, Any]]
    total_cost: float
    time_to_complete: str
    skill_coverage: float  # 0-100

class LearningPathResponse(BaseModel):
    """Response model for learning path generation"""
    learning_path: List[Dict[str, Any]]
    estimated_duration: str
    milestones: List[str]
    recommended_resources: List[str]

class CourseProgressResponse(BaseModel):
    """Response model for course progress tracking"""
    user_id: str
    course_id: str
    progress: float
    next_steps: List[str]
    completion_estimate: str

# ============================================================================
# MOCK DATA
# Sample data for demonstration purposes
# ============================================================================

# ----------------------------------------------------------------------------
# COURSE DATABASE
# Mock database of available courses
# ----------------------------------------------------------------------------

COURSE_DATABASE = {
    "Python": [
        {
            "id": "py101",
            "title": "Python for Beginners",
            "provider": "Coursera",
            "duration": "4 weeks",
            "cost": 49.99,
            "level": "beginner",
            "format": "self_paced",
            "rating": 4.7
        },
        {
            "id": "py201",
            "title": "Intermediate Python",
            "provider": "edX",
            "duration": "6 weeks",
            "cost": 79.99,
            "level": "intermediate",
            "format": "instructor_led",
            "rating": 4.8
        },
        {
            "id": "py301",
            "title": "Advanced Python Programming",
            "provider": "Udemy",
            "duration": "8 weeks",
            "cost": 89.99,
            "level": "advanced",
            "format": "self_paced",
            "rating": 4.6
        }
    ],
    "Machine Learning": [
        {
            "id": "ml101",
            "title": "Machine Learning Fundamentals",
            "provider": "Coursera",
            "duration": "6 weeks",
            "cost": 59.99,
            "level": "intermediate",
            "format": "instructor_led",
            "rating": 4.9
        },
        {
            "id": "ml201",
            "title": "Deep Learning Specialization",
            "provider": "DeepLearning.AI",
            "duration": "12 weeks",
            "cost": 149.99,
            "level": "advanced",
            "format": "self_paced",
            "rating": 4.8
        }
    ],
    "Data Science": [
        {
            "id": "ds101",
            "title": "Data Science Essentials",
            "provider": "edX",
            "duration": "8 weeks",
            "cost": 89.99,
            "level": "intermediate",
            "format": "instructor_led",
            "rating": 4.7
        }
    ]
}

# ----------------------------------------------------------------------------
# SKILL MAPPINGS
# Mapping of roles to required skills
# ----------------------------------------------------------------------------

SKILL_MAPPINGS = {
    "Software Engineer": ["Python", "JavaScript", "SQL", "Git", "Docker"],
    "Data Scientist": ["Python", "Machine Learning", "Statistics", "R", "SQL"],
    "Product Manager": ["Product Strategy", "Market Analysis", "Agile", "User Research", "Data Analysis"]
}

# ============================================================================
# HELPER FUNCTIONS
# Utility functions for course recommendations
# ============================================================================

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the course recommendation service
# ============================================================================

# ----------------------------------------------------------------------------
# ROOT ENDPOINT
# Simple endpoint to verify service is running
# ----------------------------------------------------------------------------

@app.get("/")
def read_root():
    """
    Root endpoint to verify service is running
    
    Returns:
        dict: Welcome message
    """
    return {"message": "Course Recommendation Engine Service is running"}

# ----------------------------------------------------------------------------
# HEALTH CHECK ENDPOINT
# Endpoint for checking service health status
# ----------------------------------------------------------------------------

@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring service status
    
    Returns:
        dict: Health status information
    """
    return {"status": "healthy"}

# ----------------------------------------------------------------------------
# SKILL ASSESSMENT ENDPOINT
# Endpoint for assessing skill gaps and recommending learning priorities
# ----------------------------------------------------------------------------

@app.post("/assess-skills", response_model=SkillAssessmentResponse)
async def assess_skills(request: SkillAssessmentRequest):
    """
    Assess skill gaps and recommend learning priorities
    
    Args:
        request (SkillAssessmentRequest): Request containing current skills, target role, and experience level
        
    Returns:
        SkillAssessmentResponse: Response with skill gaps, recommended skills, proficiency levels, and learning priority
        
    Example:
        POST /assess-skills
        {
            "current_skills": ["Python", "SQL"],
            "target_role": "Data Scientist",
            "experience_level": "Entry-level"
        }
    """
    # In a real implementation, this would use more sophisticated algorithms
    # For this mock, we'll generate assessments based on the target role
    
    # Get required skills for target role
    required_skills = SKILL_MAPPINGS.get(request.target_role, ["General Skills"])
    
    # Identify skill gaps by comparing current skills with required skills
    skill_gaps = [skill for skill in required_skills if skill not in request.current_skills]
    
    # Recommend skills to learn (combine gaps and some additional skills)
    recommended_skills = skill_gaps.copy()
    if request.experience_level == "Entry-level":
        # Add some foundational skills for entry-level positions
        recommended_skills.extend(["Communication", "Problem Solving"])
    elif request.experience_level == "Mid-level":
        # Add some advanced skills for mid-level positions
        recommended_skills.extend(["Leadership", "Project Management"])
    
    # Generate proficiency levels for current skills
    proficiency_levels = {}
    for skill in request.current_skills:
        if skill in required_skills:
            # Higher proficiency for required skills based on experience level
            proficiency_levels[skill] = "intermediate" if request.experience_level == "Entry-level" else "advanced"
        else:
            # Lower proficiency for non-required skills
            proficiency_levels[skill] = "beginner" if request.experience_level == "Entry-level" else "intermediate"
    
    # Add proficiency levels for recommended skills
    for skill in recommended_skills:
        if skill not in proficiency_levels:
            proficiency_levels[skill] = "beginner"
    
    # Generate learning priority (mock implementation - top 5 priorities)
    learning_priority = recommended_skills[:5]  # Top 5 priorities
    
    # Return the skill assessment response
    return SkillAssessmentResponse(
        skill_gaps=skill_gaps,
        recommended_skills=recommended_skills,
        proficiency_levels=proficiency_levels,
        learning_priority=learning_priority
    )

# ----------------------------------------------------------------------------
# COURSE RECOMMENDATION ENDPOINT
# Endpoint for recommending courses based on skills to learn
# ----------------------------------------------------------------------------

@app.post("/recommend-courses", response_model=CourseRecommendationResponse)
async def recommend_courses(request: CourseRecommendationRequest):
    """
    Recommend courses based on skills to learn and career goals
    
    Args:
        request (CourseRecommendationRequest): Request containing user ID, skills to learn, and career goal
        
    Returns:
        CourseRecommendationResponse: Response with recommended courses, total cost, time to complete, and skill coverage
        
    Example:
        POST /recommend-courses
        {
            "user_id": "user123",
            "skills_to_learn": ["Python", "Machine Learning"],
            "career_goal": "Data Scientist"
        }
    """
    # In a real implementation, this would use recommendation algorithms
    # For this mock, we'll generate recommendations based on the skills
    
    # Initialize variables for storing recommendations
    recommended_courses = []
    total_cost = 0.0
    covered_skills = set()
    
    # Find courses for each skill the user wants to learn
    for skill in request.skills_to_learn:
        if skill in COURSE_DATABASE:
            # Get available courses for this skill
            courses = COURSE_DATABASE[skill]
            
            # Filter by budget if provided by the user
            if request.budget:
                affordable_courses = [c for c in courses if c["cost"] <= request.budget]
                if affordable_courses:
                    courses = affordable_courses
            
            # Select the best course (highest rated) from available options
            if courses:
                best_course = max(courses, key=lambda x: x["rating"])
                recommended_courses.append(best_course)
                total_cost += best_course["cost"]
                covered_skills.add(skill)
    
    # Calculate skill coverage percentage
    skill_coverage = (len(covered_skills) / len(request.skills_to_learn)) * 100 if request.skills_to_learn else 0
    
    # Estimate total time to complete all recommended courses
    total_weeks = sum(int(course["duration"].split()[0]) for course in recommended_courses)
    time_to_complete = f"{total_weeks} weeks"
    
    # Return the course recommendation response
    return CourseRecommendationResponse(
        courses=recommended_courses,
        total_cost=total_cost,
        time_to_complete=time_to_complete,
        skill_coverage=skill_coverage
    )

# ----------------------------------------------------------------------------
# LEARNING PATH ENDPOINT
# Endpoint for generating personalized learning paths
# ----------------------------------------------------------------------------

@app.post("/generate-learning-path", response_model=LearningPathResponse)
async def generate_learning_path(request: LearningPathRequest):
    """
    Generate a personalized learning path to reach career goals
    
    Args:
        request (LearningPathRequest): Request containing target role, current skills, experience level, and timeline
        
    Returns:
        LearningPathResponse: Response with learning path, estimated duration, milestones, and recommended resources
        
    Example:
        POST /generate-learning-path
        {
            "target_role": "Data Scientist",
            "current_skills": ["Python", "SQL"],
            "experience_level": "Entry-level",
            "timeline": "medium_term"
        }
    """
    # In a real implementation, this would create a detailed learning path
    # For this mock, we'll generate a structured path
    
    # Get required skills for target role
    required_skills = SKILL_MAPPINGS.get(request.target_role, ["General Skills"])
    
    # Identify skill gaps by comparing current skills with required skills
    skill_gaps = [skill for skill in required_skills if skill not in request.current_skills]
    
    # Initialize data structures for the learning path
    learning_path = []
    milestones = []
    resources = []
    
    # Add courses for skill gaps (limit to 5 skills for demo)
    for i, skill in enumerate(skill_gaps[:5]):
        if skill in COURSE_DATABASE:
            courses = COURSE_DATABASE[skill]
            if courses:
                course = courses[0]  # Take the first course
                learning_path.append({
                    "step": i + 1,
                    "skill": skill,
                    "course": course["title"],
                    "provider": course["provider"],
                    "duration": course["duration"],
                    "prerequisites": [] if i == 0 else [skill_gaps[i-1]]
                })
    
    # Generate career development milestones
    milestones = [
        "Complete foundational courses",
        "Build first project",
        "Apply for entry-level positions",
        "Network with professionals"
    ]
    
    # Generate recommended learning resources
    resources = [
        "Industry blogs and publications",
        "Professional networking events",
        "Open source projects",
        "Mentorship programs"
    ]
    
    # Estimate duration based on user's timeline preference
    if request.timeline == "short_term":
        estimated_duration = "3-6 months"
    elif request.timeline == "medium_term":
        estimated_duration = "6-12 months"
    else:  # long_term
        estimated_duration = "12+ months"
    
    # Return the learning path response
    return LearningPathResponse(
        learning_path=learning_path,
        estimated_duration=estimated_duration,
        milestones=milestones,
        recommended_resources=resources
    )

# ----------------------------------------------------------------------------
# PROGRESS TRACKING ENDPOINT
# Endpoint for tracking course progress and providing next steps
# ----------------------------------------------------------------------------

@app.post("/track-progress", response_model=CourseProgressResponse)
async def track_progress(request: CourseProgressRequest):
    """
    Track course progress and provide next steps
    
    Args:
        request (CourseProgressRequest): Request containing user ID, course ID, and progress percentage
        
    Returns:
        CourseProgressResponse: Response with progress tracking information and next steps
        
    Example:
        POST /track-progress
        {
            "user_id": "user123",
            "course_id": "py101",
            "progress": 45.5
        }
    """
    # In a real implementation, this would integrate with course platforms
    # For this mock, we'll generate progress tracking
    
    # Generate personalized next steps based on progress percentage
    next_steps = []
    if request.progress < 25:
        next_steps = ["Complete the first module", "Take notes on key concepts", "Join course discussion forums"]
    elif request.progress < 50:
        next_steps = ["Finish current module", "Start working on assignments", "Connect with classmates"]
    elif request.progress < 75:
        next_steps = ["Complete remaining modules", "Work on capstone project", "Review previous materials"]
    else:
        next_steps = ["Finalize project work", "Prepare for final assessment", "Plan next learning steps"]
    
    # Estimate completion time based on remaining progress
    remaining_progress = 100 - request.progress
    completion_estimate = f"{int(remaining_progress / 10)} weeks remaining"
    
    # Return the course progress response
    return CourseProgressResponse(
        user_id=request.user_id,
        course_id=request.course_id,
        progress=request.progress,
        next_steps=next_steps,
        completion_estimate=completion_estimate
    )

# ----------------------------------------------------------------------------
# COURSE CATALOG ENDPOINT
# Endpoint for retrieving the course catalog with filtering
# ----------------------------------------------------------------------------

@app.get("/course-catalog")
async def get_course_catalog(skills: Optional[str] = None, level: Optional[str] = None):
    """
    Get the course catalog with optional filtering
    
    Args:
        skills (str, optional): Comma-separated list of skills to filter by
        level (str, optional): Skill level to filter by (beginner, intermediate, advanced)
        
    Returns:
        dict: Course catalog with filtered courses and total count
        
    Example:
        GET /course-catalog?skills=Python,Machine%20Learning&level=intermediate
    """
    # Initialize list for storing filtered courses
    filtered_courses = []
    
    # Filter courses based on skills parameter if provided
    if skills:
        skill_list = skills.split(",")
        for skill in skill_list:
            skill = skill.strip()
            if skill in COURSE_DATABASE:
                filtered_courses.extend(COURSE_DATABASE[skill])
    else:
        # Return all courses if no skills filter provided
        for course_list in COURSE_DATABASE.values():
            filtered_courses.extend(course_list)
    
    # Filter by level if provided
    if level:
        filtered_courses = [course for course in filtered_courses if course["level"] == level]
    
    # Return the course catalog response
    return {"courses": filtered_courses, "total_count": len(filtered_courses)}

# ============================================================================
# APPLICATION ENTRY POINT
# Main execution block for running the service
# ============================================================================

if __name__ == "__main__":
    # Import uvicorn for running the ASGI application
    import uvicorn
    
    # Run the FastAPI application with uvicorn
    # Host 0.0.0.0 makes it accessible from outside the container
    # Port 8119 is the designated port for this microservice
    uvicorn.run(app, host="0.0.0.0", port=8119)