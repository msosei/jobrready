"""
Interview Prep Coach Service
Version: 1.0
Purpose: Generate likely interview questions based on job description and resume

This microservice provides functionality to:
1. Generate behavioral, technical, and situational interview questions
2. Create personalized interview preparation plans
3. Provide preparation tips based on skills and experience
4. Estimate preparation time for interview practice
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for the application
# ============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import random

# ============================================================================
# APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata
# ============================================================================

app = FastAPI(
    title="Interview Prep Coach",
    description="Generate likely interview questions based on job description and resume",
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

class InterviewPrepRequest(BaseModel):
    """Request model for interview preparation"""
    resume_text: str
    job_description: str
    question_types: List[str] = ["behavioral", "technical", "situational"]

# ----------------------------------------------------------------------------
# RESPONSE MODELS
# Models for API response data
# ----------------------------------------------------------------------------

class InterviewQuestion(BaseModel):
    """Model for individual interview questions"""
    question: str
    type: str  # "behavioral", "technical", "situational"
    category: str
    difficulty: str  # "easy", "medium", "hard"
    tips: List[str]

class InterviewPrepResponse(BaseModel):
    """Response model for interview preparation results"""
    questions: List[InterviewQuestion]
    preparation_tips: List[str]
    estimated_duration: int  # minutes

# ============================================================================
# INTERVIEW QUESTION DATABASE
# Collections of question templates, technical questions, and behavioral categories
# ============================================================================

# ----------------------------------------------------------------------------
# BEHAVIORAL QUESTION TEMPLATES
# Generic templates for generating behavioral interview questions
# ----------------------------------------------------------------------------

behavioral_templates = [
    "Tell me about a time when you had to {challenge}.",
    "Describe a situation where you {action}.",
    "Give me an example of when you {situation}.",
    "Tell me about a time when you had to {conflict}.",
    "Describe a situation where you {decision}."
]

# ----------------------------------------------------------------------------
# TECHNICAL QUESTIONS
# Subject-specific technical questions organized by skill area
# ----------------------------------------------------------------------------

technical_questions = {
    "python": [
        "What is the difference between a list and a tuple in Python?",
        "Explain Python decorators and provide an example.",
        "How does garbage collection work in Python?",
        "What is the GIL in Python and how does it affect performance?"
    ],
    "javascript": [
        "Explain the difference between == and === in JavaScript.",
        "What is closure in JavaScript?",
        "Explain event delegation in JavaScript.",
        "What is the difference between let, const, and var?"
    ],
    "react": [
        "What is the virtual DOM and how does it work?",
        "Explain the component lifecycle in React.",
        "What are React hooks and how do they work?",
        "How do you optimize performance in a React application?"
    ],
    "sql": [
        "Explain the difference between INNER JOIN and LEFT JOIN.",
        "What is normalization and why is it important?",
        "How do you optimize a slow SQL query?",
        "Explain the ACID properties of a database transaction."
    ],
    "docker": [
        "What is the difference between an image and a container?",
        "Explain Docker volumes and when to use them.",
        "How do you ensure security in Docker containers?",
        "What is Docker Compose and how is it used?"
    ]
}

# ----------------------------------------------------------------------------
# BEHAVIORAL CATEGORIES
# Categories and specific challenges for behavioral questions
# ----------------------------------------------------------------------------

behavioral_categories = {
    "leadership": ["lead a team", "manage a project", "mentor a colleague", "resolve team conflict"],
    "problem_solving": ["solve a complex problem", "debug a difficult issue", "overcome a technical challenge", "improve a process"],
    "communication": ["explain a complex topic", "persuade a team", "handle difficult feedback", "present to executives"],
    "adaptability": ["adapt to change", "learn a new technology", "handle multiple priorities", "work under pressure"],
    "collaboration": ["work with a difficult colleague", "collaborate across teams", "influence without authority", "handle disagreement"]
}

# ============================================================================
# HELPER FUNCTIONS
# Utility functions for question generation and text analysis
# ============================================================================

# ----------------------------------------------------------------------------
# SKILL EXTRACTION
# Function to extract technical skills from text content
# ----------------------------------------------------------------------------

def extract_skills(text: str) -> List[str]:
    """
    Extract technical skills from text
    
    Args:
        text (str): Text content to analyze for skills
        
    Returns:
        List[str]: List of technical skills found in the text
    """
    skills = []
    text_lower = text.lower()
    
    # Check for technical skills in the text
    for skill in technical_questions.keys():
        if skill in text_lower:
            skills.append(skill)
    
    return skills

# ----------------------------------------------------------------------------
# EXPERIENCE EXTRACTION
# Function to extract experience areas from text content
# ----------------------------------------------------------------------------

def extract_experience(text: str) -> List[str]:
    """
    Extract experience areas from text
    
    Args:
        text (str): Text content to analyze for experience
        
    Returns:
        List[str]: List of experience areas found in the text
    """
    experiences = []
    text_lower = text.lower()
    
    # Check for experience keywords in the text
    experience_keywords = ["managed", "led", "developed", "created", "implemented", "optimized"]
    for keyword in experience_keywords:
        if keyword in text_lower:
            experiences.append(keyword)
    
    return experiences

# ----------------------------------------------------------------------------
# BEHAVIORAL QUESTION GENERATION
# Function to generate behavioral interview questions
# ----------------------------------------------------------------------------

def generate_behavioral_questions(resume_text: str, job_description: str, count: int = 5) -> List[InterviewQuestion]:
    """
    Generate behavioral interview questions
    
    Args:
        resume_text (str): Candidate's resume text
        job_description (str): Job description text
        count (int): Number of questions to generate (default: 5)
        
    Returns:
        List[InterviewQuestion]: List of generated behavioral questions
    """
    questions = []
    
    # Extract categories from resume and job description
    categories = list(behavioral_categories.keys())
    
    # Generate questions for each category
    for i in range(min(count, len(categories))):
        category = categories[i % len(categories)]
        challenges = behavioral_categories[category]
        challenge = random.choice(challenges)
        
        # Select a template and format it with the challenge
        template = random.choice(behavioral_templates)
        question_text = template.format(**{template.split('{')[1].split('}')[0]: challenge})
        
        # Create interview question object with tips
        questions.append(InterviewQuestion(
            question=question_text,
            type="behavioral",
            category=category,
            difficulty="medium",
            tips=[
                "Use the STAR method (Situation, Task, Action, Result)",
                "Be specific about your role and actions",
                "Focus on measurable outcomes when possible",
                "Keep your answer concise but comprehensive"
            ]
        ))
    
    return questions

# ----------------------------------------------------------------------------
# TECHNICAL QUESTION GENERATION
# Function to generate technical interview questions based on skills
# ----------------------------------------------------------------------------

def generate_technical_questions(resume_text: str, job_description: str, count: int = 5) -> List[InterviewQuestion]:
    """
    Generate technical interview questions based on skills
    
    Args:
        resume_text (str): Candidate's resume text
        job_description (str): Job description text
        count (int): Number of questions to generate (default: 5)
        
    Returns:
        List[InterviewQuestion]: List of generated technical questions
    """
    questions = []
    
    # Extract skills from both resume and job description
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    common_skills = list(set(resume_skills) & set(job_skills))
    
    # If no common skills, use job skills
    skills_to_use = common_skills if common_skills else job_skills
    
    # If still no skills, use a default set
    if not skills_to_use:
        skills_to_use = ["python", "javascript"]
    
    # Generate questions for each skill
    for i in range(min(count, len(skills_to_use))):
        skill = skills_to_use[i % len(skills_to_use)]
        if skill in technical_questions:
            question_texts = technical_questions[skill]
            if question_texts:
                question_text = random.choice(question_texts)
                difficulty = "hard" if "advanced" in question_text.lower() or "optimize" in question_text.lower() else "medium"
                
                # Create interview question object with tips
                questions.append(InterviewQuestion(
                    question=question_text,
                    type="technical",
                    category=skill,
                    difficulty=difficulty,
                    tips=[
                        "Explain your thought process clearly",
                        "Ask clarifying questions if needed",
                        "Start with a simple solution and optimize if time permits",
                        "Consider edge cases and error handling"
                    ]
                ))
    
    # Fill remaining slots with random technical questions
    while len(questions) < count:
        skill = random.choice(list(technical_questions.keys()))
        question_texts = technical_questions[skill]
        if question_texts:
            question_text = random.choice(question_texts)
            difficulty = "hard" if "advanced" in question_text.lower() or "optimize" in question_text.lower() else "medium"
            
            # Create interview question object with tips
            questions.append(InterviewQuestion(
                question=question_text,
                type="technical",
                category=skill,
                difficulty=difficulty,
                tips=[
                    "Explain your thought process clearly",
                    "Ask clarifying questions if needed",
                    "Start with a simple solution and optimize if time permits",
                    "Consider edge cases and error handling"
                ]
            ))
    
    return questions

# ----------------------------------------------------------------------------
# SITUATIONAL QUESTION GENERATION
# Function to generate situational interview questions
# ----------------------------------------------------------------------------

def generate_situational_questions(resume_text: str, job_description: str, count: int = 3) -> List[InterviewQuestion]:
    """
    Generate situational interview questions
    
    Args:
        resume_text (str): Candidate's resume text
        job_description (str): Job description text
        count (int): Number of questions to generate (default: 3)
        
    Returns:
        List[InterviewQuestion]: List of generated situational questions
    """
    questions = [
        InterviewQuestion(
            question="If you noticed a critical bug in production just before a major release, what would you do?",
            type="situational",
            category="problem_solving",
            difficulty="medium",
            tips=[
                "Prioritize based on impact and severity",
                "Communicate with stakeholders immediately",
                "Document the issue and your decision-making process",
                "Consider both short-term fixes and long-term solutions"
            ]
        ),
        InterviewQuestion(
            question="How would you handle working with a team member who consistently misses deadlines?",
            type="situational",
            category="collaboration",
            difficulty="medium",
            tips=[
                "Address the issue directly but professionally",
                "Try to understand their challenges",
                "Offer help or resources if appropriate",
                "Escalate to management if necessary"
            ]
        ),
        InterviewQuestion(
            question="If asked to implement a feature you believe is technically flawed, how would you respond?",
            type="situational",
            category="communication",
            difficulty="hard",
            tips=[
                "Present your concerns with data and examples",
                "Suggest alternatives with clear reasoning",
                "Be respectful of the decision-making process",
                "Document your concerns for future reference"
            ]
        )
    ]
    
    return questions[:count]

# ----------------------------------------------------------------------------
# PREPARATION TIPS GENERATION
# Function to generate general preparation tips
# ----------------------------------------------------------------------------

def generate_preparation_tips(resume_text: str, job_description: str) -> List[str]:
    """
    Generate general preparation tips
    
    Args:
        resume_text (str): Candidate's resume text
        job_description (str): Job description text
        
    Returns:
        List[str]: List of preparation tips
    """
    tips = [
        "Review your resume thoroughly and be ready to elaborate on any point",
        "Research the company culture, mission, and recent news",
        "Practice the STAR method for behavioral questions",
        "Prepare questions to ask the interviewer about the role and team",
        "Dress appropriately and arrive early (or test your tech setup for virtual interviews)",
        "Think of specific examples that demonstrate your skills and achievements",
        "Practice explaining technical concepts in simple terms",
        "Prepare for both technical and cultural fit questions"
    ]
    
    # Add skill-specific tips based on extracted skills
    skills = extract_skills(resume_text + job_description)
    if "python" in skills:
        tips.append("Review Python fundamentals, data structures, and common libraries")
    if "javascript" in skills:
        tips.append("Brush up on JavaScript ES6+ features and asynchronous programming")
    if "react" in skills:
        tips.append("Practice React concepts like hooks, state management, and performance optimization")
    if "sql" in skills:
        tips.append("Review SQL joins, indexing, and query optimization techniques")
    if "docker" in skills:
        tips.append("Understand containerization concepts and Docker best practices")
    
    return tips

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the interview coach service
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
# INTERVIEW QUESTION GENERATION ENDPOINT
# Main endpoint for generating interview questions based on resume and job description
# ----------------------------------------------------------------------------

@app.post("/generate-questions", response_model=InterviewPrepResponse)
async def generate_interview_questions(request: InterviewPrepRequest):
    """
    Generate interview questions based on resume and job description
    
    Args:
        request (InterviewPrepRequest): Request containing resume text, job description, and question types
        
    Returns:
        InterviewPrepResponse: Response with generated questions, preparation tips, and estimated duration
        
    Example:
        POST /generate-questions
        {
            "resume_text": "Experienced Python developer with 5 years of experience...",
            "job_description": "Looking for a senior Python developer with React experience...",
            "question_types": ["behavioral", "technical"]
        }
    """
    try:
        # Initialize list for storing generated questions
        questions = []
        
        # Generate questions based on requested types
        if "behavioral" in request.question_types:
            questions.extend(generate_behavioral_questions(
                request.resume_text, request.job_description, 5))
        
        if "technical" in request.question_types:
            questions.extend(generate_technical_questions(
                request.resume_text, request.job_description, 5))
        
        if "situational" in request.question_types:
            questions.extend(generate_situational_questions(
                request.resume_text, request.job_description, 3))
        
        # Generate preparation tips based on resume and job description
        preparation_tips = generate_preparation_tips(
            request.resume_text, request.job_description)
        
        # Estimate preparation duration (3 minutes per question + 10 minutes for tips)
        estimated_duration = len(questions) * 3 + 10
        
        # Return the interview preparation response with all generated content
        return InterviewPrepResponse(
            questions=questions,
            preparation_tips=preparation_tips,
            estimated_duration=estimated_duration
        )
    except Exception as e:
        # Handle any errors during question generation
        raise HTTPException(status_code=500, detail=f"Error generating interview questions: {str(e)}")

# ============================================================================
# APPLICATION ENTRY POINT
# Main execution block for running the service
# ============================================================================

if __name__ == "__main__":
    # Import uvicorn for running the ASGI application
    import uvicorn
    
    # Run the FastAPI application with uvicorn
    # Host 0.0.0.0 makes it accessible from outside the container
    # Port 8108 is the designated port for this microservice
    uvicorn.run(app, host="0.0.0.0", port=8108)