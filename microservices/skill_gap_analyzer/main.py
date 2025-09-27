"""
Skill Gap Analyzer Service
Version: 1.0
Purpose: AI microservice to analyze skill gaps between resumes and job descriptions

This microservice provides functionality to:
1. Extract skills from resumes and job descriptions
2. Identify missing skills and matched skills
3. Calculate skill gap scores
4. Provide learning recommendations for skill development
5. Analyze market demand for specific skills
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for the application
# ============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import re
from typing import List, Dict, Any, Optional

# ============================================================================
# APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata
# ============================================================================

app = FastAPI(
    title="Skill Gap Analyzer",
    description="AI microservice to analyze skill gaps between resumes and job descriptions",
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

class SkillGapRequest(BaseModel):
    """Request model for skill gap analysis"""
    resume_text: str
    job_description: str
    learning_platform: Optional[str] = "general"  # "coursera", "udemy", "edx", "general"

# ----------------------------------------------------------------------------
# RESPONSE MODELS
# Models for API response data
# ----------------------------------------------------------------------------

class SkillGapResponse(BaseModel):
    """Response model for skill gap analysis results"""
    missing_skills: List[str]
    matched_skills: List[str]
    skill_gap_score: float
    recommendations: List[Dict[str, Any]]
    market_demand: Dict[str, str]  # Skill: demand level (High, Medium, Low)

class LearningResource(BaseModel):
    """Model for learning resources"""
    title: str
    url: str
    platform: str
    type: str  # "course", "tutorial", "certification", "book"
    duration: Optional[str] = None
    cost: Optional[str] = None

# ============================================================================
# SKILL DATABASE
# Comprehensive database of skills with market demand levels and alternatives
# ============================================================================

# Enhanced skill database with market demand levels
skill_database = {
    "python": {"demand": "High", "alternatives": ["java", "javascript"]},
    "javascript": {"demand": "High", "alternatives": ["typescript", "python"]},
    "react": {"demand": "High", "alternatives": ["vue.js", "angular"]},
    "node.js": {"demand": "High", "alternatives": ["express", "django"]},
    "sql": {"demand": "High", "alternatives": ["mongodb", "postgresql"]},
    "docker": {"demand": "High", "alternatives": ["kubernetes", "podman"]},
    "kubernetes": {"demand": "High", "alternatives": ["docker", "openshift"]},
    "aws": {"demand": "High", "alternatives": ["azure", "gcp"]},
    "machine learning": {"demand": "High", "alternatives": ["data science", "ai"]},
    "data analysis": {"demand": "High", "alternatives": ["business intelligence", "data science"]},
    "tensorflow": {"demand": "Medium", "alternatives": ["pytorch", "scikit-learn"]},
    "pytorch": {"demand": "Medium", "alternatives": ["tensorflow", "scikit-learn"]},
    "java": {"demand": "High", "alternatives": ["python", "c#"]},
    "spring": {"demand": "Medium", "alternatives": ["django", "express"]},
    "angular": {"demand": "Medium", "alternatives": ["react", "vue.js"]},
    "vue.js": {"demand": "Medium", "alternatives": ["react", "angular"]},
    "mongodb": {"demand": "Medium", "alternatives": ["postgresql", "mysql"]},
    "postgresql": {"demand": "High", "alternatives": ["mysql", "mongodb"]},
    "azure": {"demand": "High", "alternatives": ["aws", "gcp"]},
    "gcp": {"demand": "High", "alternatives": ["aws", "azure"]},
    "ci/cd": {"demand": "High", "alternatives": ["jenkins", "github actions"]},
    "git": {"demand": "High", "alternatives": ["svn", "mercurial"]},
    "agile": {"demand": "High", "alternatives": ["scrum", "kanban"]},
    "scrum": {"demand": "High", "alternatives": ["agile", "kanban"]},
    "api": {"demand": "High", "alternatives": ["rest", "graphql"]},
    "rest": {"demand": "High", "alternatives": ["api", "graphql"]},
    "graphql": {"demand": "Medium", "alternatives": ["rest", "api"]},
    "devops": {"demand": "High", "alternatives": ["sre", "platform engineering"]},
    "linux": {"demand": "High", "alternatives": ["unix", "bash"]},
    "bash": {"demand": "Medium", "alternatives": ["powershell", "shell"]},
    "r": {"demand": "Medium", "alternatives": ["python", "sas"]},
    "tableau": {"demand": "Medium", "alternatives": ["power bi", "qlik"]},
    "power bi": {"demand": "Medium", "alternatives": ["tableau", "qlik"]},
    "excel": {"demand": "Medium", "alternatives": ["google sheets", "numbers"]},
    "hadoop": {"demand": "Low", "alternatives": ["spark", "kafka"]},
    "spark": {"demand": "Medium", "alternatives": ["hadoop", "kafka"]},
    "kafka": {"demand": "Medium", "alternatives": ["rabbitmq", "activemq"]},
    "elasticsearch": {"demand": "Medium", "alternatives": ["solr", "splunk"]},
    "redis": {"demand": "Medium", "alternatives": ["memcached", "hazelcast"]},
    "jenkins": {"demand": "Medium", "alternatives": ["github actions", "gitlab ci"]},
    "ansible": {"demand": "Medium", "alternatives": ["puppet", "chef"]},
    "terraform": {"demand": "Medium", "alternatives": ["cloudformation", "pulumi"]},
    "pandas": {"demand": "High", "alternatives": ["numpy", "dplyr"]},
    "numpy": {"demand": "High", "alternatives": ["pandas", "scipy"]},
    "matplotlib": {"demand": "Medium", "alternatives": ["seaborn", "ggplot2"]},
    "seaborn": {"demand": "Medium", "alternatives": ["matplotlib", "plotly"]},
    "scikit-learn": {"demand": "High", "alternatives": ["tensorflow", "pytorch"]},
    "nltk": {"demand": "Low", "alternatives": ["spacy", "stanford nlp"]},
    "spacy": {"demand": "Medium", "alternatives": ["nltk", "stanford nlp"]},
    "computer vision": {"demand": "Medium", "alternatives": ["image processing", "deep learning"]},
    "nlp": {"demand": "Medium", "alternatives": ["natural language processing", "text mining"]},
    "deep learning": {"demand": "High", "alternatives": ["machine learning", "neural networks"]},
    "neural networks": {"demand": "High", "alternatives": ["deep learning", "machine learning"]},
    "data mining": {"demand": "Medium", "alternatives": ["data analysis", "data science"]},
    "statistical analysis": {"demand": "High", "alternatives": ["statistics", "data analysis"]},
    "sas": {"demand": "Low", "alternatives": ["r", "python"]},
    "oracle": {"demand": "Medium", "alternatives": ["postgresql", "mysql"]},
    "sql server": {"demand": "Medium", "alternatives": ["postgresql", "mysql"]},
    "communication": {"demand": "High", "alternatives": ["interpersonal skills", "presentation"]},
    "leadership": {"demand": "High", "alternatives": ["management", "teamwork"]},
    "teamwork": {"demand": "High", "alternatives": ["collaboration", "leadership"]},
    "problem solving": {"demand": "High", "alternatives": ["critical thinking", "analytical skills"]},
    "critical thinking": {"demand": "High", "alternatives": ["problem solving", "analytical skills"]},
    "html": {"demand": "High", "alternatives": ["css", "javascript"]},
    "css": {"demand": "High", "alternatives": ["html", "sass"]},
    "bootstrap": {"demand": "Medium", "alternatives": ["tailwind", "bulma"]},
    "jquery": {"demand": "Low", "alternatives": ["vanilla js", "javascript"]},
    "express": {"demand": "Medium", "alternatives": ["fastapi", "flask"]},
    "flask": {"demand": "Medium", "alternatives": ["express", "fastapi"]},
    "django": {"demand": "Medium", "alternatives": ["flask", "express"]},
    "hibernate": {"demand": "Low", "alternatives": ["mybatis", "jpa"]},
    "maven": {"demand": "Low", "alternatives": ["gradle", "ant"]},
    "gradle": {"demand": "Medium", "alternatives": ["maven", "ant"]},
    "puppet": {"demand": "Low", "alternatives": ["ansible", "chef"]},
    "chef": {"demand": "Low", "alternatives": ["ansible", "puppet"]},
    "cloudformation": {"demand": "Low", "alternatives": ["terraform", "pulumi"]},
    "pulumi": {"demand": "Low", "alternatives": ["terraform", "cloudformation"]}
}

# ============================================================================
# CORE FUNCTIONS
# Main functions for skill extraction, gap analysis, and recommendations
# ============================================================================

# ----------------------------------------------------------------------------
# SKILL EXTRACTION
# Function to extract potential skills from text using pattern matching
# ----------------------------------------------------------------------------

def extract_skills(text: str) -> List[str]:
    """
    Extract potential skills from text using pattern matching
    
    Args:
        text (str): Text to extract skills from (resume or job description)
        
    Returns:
        List[str]: List of identified skills
    """
    found_skills = []
    text_lower = text.lower()
    
    # Check for each skill in the skill database
    for skill in skill_database.keys():
        if skill in text_lower:
            found_skills.append(skill.title())
    
    # Return unique skills only
    return list(set(found_skills))

# ----------------------------------------------------------------------------
# SKILL GAP CALCULATION
# Function to calculate a skill gap score between resume and job requirements
# ----------------------------------------------------------------------------

def calculate_skill_gap_score(resume_skills: List[str], job_skills: List[str]) -> float:
    """
    Calculate a skill gap score between 0 and 1
    
    Args:
        resume_skills (List[str]): Skills found in the resume
        job_skills (List[str]): Skills required for the job
        
    Returns:
        float: Skill gap score (0.0 = no match, 1.0 = perfect match)
    """
    # Handle edge case of no job skills
    if not job_skills:
        return 1.0
    
    # Calculate the ratio of matched skills to required skills
    matched_count = len(set(resume_skills) & set(job_skills))
    return matched_count / len(set(job_skills))

# ----------------------------------------------------------------------------
# MARKET DEMAND ANALYSIS
# Function to get market demand levels for skills
# ----------------------------------------------------------------------------

def get_market_demand(skills: List[str]) -> Dict[str, str]:
    """
    Get market demand levels for skills
    
    Args:
        skills (List[str]): List of skills to analyze
        
    Returns:
        Dict[str, str]: Dictionary mapping skills to their demand levels
    """
    demand_levels = {}
    for skill in skills:
        skill_key = skill.lower()
        if skill_key in skill_database:
            demand_levels[skill] = skill_database[skill_key]["demand"]
        else:
            demand_levels[skill] = "Unknown"
    return demand_levels

# ----------------------------------------------------------------------------
# RECOMMENDATION GENERATION
# Function to generate learning recommendations based on missing skills
# ----------------------------------------------------------------------------

def generate_recommendations(missing_skills: List[str], learning_platform: str = "general") -> List[Dict[str, Any]]:
    """
    Generate learning recommendations based on missing skills
    
    Args:
        missing_skills (List[str]): List of skills missing from the resume
        learning_platform (str): Preferred learning platform
        
    Returns:
        List[Dict[str, Any]]: List of recommendations with learning resources
    """
    recommendations = []
    
    # Learning resources database organized by skill
    learning_resources = {
        "Python": [
            {"title": "Python for Everybody", "url": "https://www.coursera.org/specializations/python", "platform": "Coursera", "type": "course", "duration": "3 months"},
            {"title": "Complete Python Bootcamp", "url": "https://www.udemy.com/course/complete-python-bootcamp/", "platform": "Udemy", "type": "course", "duration": "4 weeks"}
        ],
        "Machine Learning": [
            {"title": "Machine Learning by Andrew Ng", "url": "https://www.coursera.org/learn/machine-learning", "platform": "Coursera", "type": "course", "duration": "2 months"},
            {"title": "Hands-On Machine Learning", "url": "https://www.amazon.com/Hands-Machine-Learning-Scikit-Learn-TensorFlow/dp/1492032646", "platform": "Amazon", "type": "book"}
        ],
        "Docker": [
            {"title": "Docker Mastery", "url": "https://www.udemy.com/course/docker-mastery/", "platform": "Udemy", "type": "course", "duration": "6 weeks"},
            {"title": "Docker for Developers", "url": "https://www.pluralsight.com/courses/docker-deep-dive", "platform": "Pluralsight", "type": "course"}
        ],
        "Kubernetes": [
            {"title": "Kubernetes for Developers", "url": "https://www.pluralsight.com/courses/kubernetes-developers-core-concepts", "platform": "Pluralsight", "type": "course"},
            {"title": "Certified Kubernetes Administrator", "url": "https://www.cncf.io/certification/cka/", "platform": "CNCF", "type": "certification"}
        ],
        "AWS": [
            {"title": "AWS Certified Solutions Architect", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/", "platform": "AWS", "type": "certification"},
            {"title": "AWS Fundamentals", "url": "https://www.coursera.org/learn/aws-fundamentals-going-cloud-native", "platform": "Coursera", "type": "course"}
        ],
        "React": [
            {"title": "React Front to Back", "url": "https://www.udemy.com/course/modern-react-front-to-back/", "platform": "Udemy", "type": "course", "duration": "8 weeks"},
            {"title": "Advanced React", "url": "https://www.pluralsight.com/courses/reactjs-advanced", "platform": "Pluralsight", "type": "course"}
        ],
        "Node.Js": [
            {"title": "The Complete Node.js Developer Course", "url": "https://www.udemy.com/course/the-complete-nodejs-developer-course-2/", "platform": "Udemy", "type": "course"},
            {"title": "Node.js: The Complete Guide", "url": "https://www.academind.com/courses/nodejs-the-complete-guide/", "platform": "Academind", "type": "course"}
        ],
        "Sql": [
            {"title": "SQL for Data Science", "url": "https://www.coursera.org/learn/sql-for-data-science", "platform": "Coursera", "type": "course"},
            {"title": "The Complete SQL Bootcamp", "url": "https://www.udemy.com/course/the-complete-sql-bootcamp/", "platform": "Udemy", "type": "course"}
        ]
    }
    
    # Generate recommendations for each missing skill
    for skill in missing_skills[:10]:  # Limit to top 10 recommendations
        skill_key = skill.title()
        resources = learning_resources.get(skill_key, [])
        
        # Filter by platform if specified
        if learning_platform and learning_platform != "general":
            resources = [r for r in resources if learning_platform.lower() in r["platform"].lower()]
        
        # If no platform-specific resources, add general ones
        if not resources and skill_key in learning_resources:
            resources = learning_resources[skill_key]
        
        # Add alternatives if no direct resources
        if not resources:
            skill_lower = skill.lower()
            if skill_lower in skill_database and "alternatives" in skill_database[skill_lower]:
                alternatives = skill_database[skill_lower]["alternatives"]
                for alt in alternatives[:2]:  # Check first 2 alternatives
                    alt_key = alt.title()
                    if alt_key in learning_resources:
                        resources = learning_resources[alt_key]
                        break
        
        # Add recommendation with resources and priority level
        recommendations.append({
            "skill": skill,
            "resources": resources[:3],  # Limit to 3 resources per skill
            "priority": "High" if skill_database.get(skill.lower(), {}).get("demand") == "High" else "Medium"
        })
    
    return recommendations

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the skill gap analyzer service
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
# SKILL GAP ANALYSIS ENDPOINT
# Endpoint for analyzing skill gaps between resumes and job descriptions
# ----------------------------------------------------------------------------

@app.post("/analyze", response_model=SkillGapResponse)
async def analyze_skill_gaps(request: SkillGapRequest):
    """
    Analyze skill gaps between a resume and job description
    
    Args:
        request (SkillGapRequest): Request containing resume text and job description
        
    Returns:
        SkillGapResponse: Analysis results including missing skills, recommendations, and gap score
        
    Example:
        POST /analyze
        {
            "resume_text": "Experienced Python developer with 5 years of experience...",
            "job_description": "We are looking for a developer with Python, React, and AWS experience...",
            "learning_platform": "coursera"
        }
    """
    try:
        # Extract skills from both resume and job description
        resume_skills = extract_skills(request.resume_text)
        job_skills = extract_skills(request.job_description)
        
        # Find missing and matched skills
        missing_skills = list(set(job_skills) - set(resume_skills))
        matched_skills = list(set(resume_skills) & set(job_skills))
        
        # Calculate skill gap score
        skill_gap_score = calculate_skill_gap_score(resume_skills, job_skills)
        
        # Get market demand for skills
        market_demand = get_market_demand(job_skills)
        
        # Generate recommendations based on missing skills and preferred platform
        platform = request.learning_platform or "general"
        recommendations = generate_recommendations(missing_skills, platform)
        
        # Return comprehensive skill gap analysis
        return SkillGapResponse(
            missing_skills=missing_skills,
            matched_skills=matched_skills,
            skill_gap_score=skill_gap_score,
            recommendations=recommendations,
            market_demand=market_demand
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing skill gaps: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8105)