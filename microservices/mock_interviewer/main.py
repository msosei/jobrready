"""
AI Mock Interviewer Service
Version: 1.0
Purpose: AI-powered mock interviewer that simulates real interview scenarios with personalized questions and feedback

This microservice provides functionality to:
1. Conduct mock interviews with personalized questions
2. Provide AI-generated feedback on interview answers
3. Track interview sessions and progress
4. Offer practice questions for different job roles and interview types
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for the application
# ============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import random
import json

# ============================================================================
# APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata
# ============================================================================

app = FastAPI(
    title="AI Mock Interviewer",
    description="AI-powered mock interviewer that simulates real interview scenarios with personalized questions and feedback",
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

class InterviewRequest(BaseModel):
    """Request model for starting a mock interview"""
    job_title: str
    industry: str
    experience_level: str  # Entry-level, Mid-level, Senior-level
    interview_type: str  # Technical, Behavioral, Case, etc.
    skills: List[str]
    resume_summary: Optional[str] = None
    company_info: Optional[str] = None

class AnswerRequest(BaseModel):
    """Request model for submitting interview answers"""
    question_id: str
    answer: str
    job_title: str
    skills: List[str]

# ----------------------------------------------------------------------------
# RESPONSE MODELS
# Models for API response data
# ----------------------------------------------------------------------------

class QuestionResponse(BaseModel):
    """Response model for interview questions"""
    question_id: str
    question: str
    question_type: str  # Technical, Behavioral, Situational
    difficulty: str  # Easy, Medium, Hard
    suggested_time: int  # Suggested time to answer in seconds

class FeedbackResponse(BaseModel):
    """Response model for interview feedback"""
    feedback: str
    score: int  # 1-10
    strengths: List[str]
    improvements: List[str]
    follow_up_questions: List[str]
    resources: List[str]

class InterviewSession(BaseModel):
    """Model for tracking interview session state"""
    session_id: str
    questions_asked: List[str]
    answers_received: Dict[str, str]
    current_question_index: int

class InterviewCompletion(BaseModel):
    """Response model for completed interview results"""
    session_id: str
    overall_score: int
    overall_feedback: str
    strengths: List[str]
    areas_for_improvement: List[str]
    recommendations: List[str]

# ============================================================================
# IN-MEMORY STORAGE
# Data structures for storing interview session information
# ============================================================================

# ----------------------------------------------------------------------------
# INTERVIEW SESSIONS
# Dictionary to store active interview sessions
# ----------------------------------------------------------------------------

interview_sessions: Dict[str, InterviewSession] = {}

# ============================================================================
# INTERVIEW CONTENT DATABASE
# Collections of interview questions and feedback templates
# ============================================================================

# ----------------------------------------------------------------------------
# INTERVIEW QUESTIONS
# Database of interview questions organized by type and role
# ----------------------------------------------------------------------------

INTERVIEW_QUESTIONS = {
    "technical": {
        "software_engineer": [
            {
                "question": "Explain the difference between a process and a thread.",
                "difficulty": "Medium",
                "suggested_time": 120
            },
            {
                "question": "What is a deadlock and how can you prevent it?",
                "difficulty": "Hard",
                "suggested_time": 180
            },
            {
                "question": "Describe the differences between TCP and UDP.",
                "difficulty": "Medium",
                "suggested_time": 120
            }
        ],
        "data_scientist": [
            {
                "question": "Explain the bias-variance tradeoff in machine learning.",
                "difficulty": "Medium",
                "suggested_time": 150
            },
            {
                "question": "What is cross-validation and why is it important?",
                "difficulty": "Medium",
                "suggested_time": 120
            }
        ],
        "product_manager": [
            {
                "question": "How would you design a ride-sharing app like Uber?",
                "difficulty": "Hard",
                "suggested_time": 240
            }
        ]
    },
    "behavioral": [
        {
            "question": "Tell me about a time you had to work with a difficult team member. How did you handle it?",
            "difficulty": "Medium",
            "suggested_time": 120
        },
        {
            "question": "Describe a situation where you had to make a decision with incomplete information.",
            "difficulty": "Hard",
            "suggested_time": 150
        },
        {
            "question": "Give me an example of a goal you set for yourself and how you achieved it.",
            "difficulty": "Easy",
            "suggested_time": 90
        }
    ],
    "situational": [
        {
            "question": "If you noticed a colleague was consistently missing deadlines, what would you do?",
            "difficulty": "Medium",
            "suggested_time": 120
        },
        {
            "question": "How would you handle a situation where your manager asked you to complete a project with an unrealistic deadline?",
            "difficulty": "Hard",
            "suggested_time": 150
        }
    ]
}

# ----------------------------------------------------------------------------
# FEEDBACK TEMPLATES
# Templates for generating feedback on interview answers
# ----------------------------------------------------------------------------

FEEDBACK_TEMPLATES = {
    "technical": {
        "strengths": [
            "Good explanation of core concepts",
            "Demonstrated strong problem-solving approach",
            "Showed understanding of trade-offs",
            "Used relevant examples effectively"
        ],
        "improvements": [
            "Could provide more specific examples",
            "Consider mentioning edge cases",
            "Try to structure your answer more clearly",
            "Include more real-world applications"
        ]
    },
    "behavioral": {
        "strengths": [
            "Provided a clear situation and action",
            "Showed good self-awareness",
            "Demonstrated learning from the experience",
            "Used the STAR method effectively"
        ],
        "improvements": [
            "Could be more concise in your response",
            "Try to quantify your impact more",
            "Include more specific details about the outcome",
            "Better connect the experience to the role"
        ]
    }
}

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the mock interviewer service
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
    return {"message": "AI Mock Interviewer Service is running"}

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
# INTERVIEW START ENDPOINT
# Endpoint for starting a new mock interview session
# ----------------------------------------------------------------------------

@app.post("/start-interview", response_model=QuestionResponse)
async def start_interview(request: InterviewRequest):
    """
    Start a new mock interview session and return the first question
    
    Args:
        request (InterviewRequest): Request containing job title, interview type, and other interview parameters
        
    Returns:
        QuestionResponse: First interview question with metadata
        
    Example:
        POST /start-interview
        {
            "job_title": "Software Engineer",
            "industry": "Technology",
            "experience_level": "Mid-level",
            "interview_type": "Technical",
            "skills": ["Python", "JavaScript", "React"]
        }
    """
    # Generate unique session ID for tracking this interview
    import uuid
    session_id = str(uuid.uuid4())
    
    # Initialize list for storing interview questions
    questions = []
    
    # Generate questions based on job title and interview type
    if request.interview_type.lower() == "technical":
        # Add technical questions based on job title
        if request.job_title.lower() in INTERVIEW_QUESTIONS["technical"]:
            questions.extend(INTERVIEW_QUESTIONS["technical"][request.job_title.lower()])
        else:
            # Default to software engineer questions if job title not found
            questions.extend(INTERVIEW_QUESTIONS["technical"]["software_engineer"])
    else:
        # Add behavioral/situational questions for non-technical interviews
        if request.interview_type.lower() == "behavioral":
            questions.extend(INTERVIEW_QUESTIONS["behavioral"])
        elif request.interview_type.lower() == "situational":
            questions.extend(INTERVIEW_QUESTIONS["situational"])
        else:
            # Mix of behavioral and situational for other interview types
            questions.extend(INTERVIEW_QUESTIONS["behavioral"][:1])
            questions.extend(INTERVIEW_QUESTIONS["situational"][:1])
    
    # Store session information for tracking progress
    interview_sessions[session_id] = InterviewSession(
        session_id=session_id,
        questions_asked=[],
        answers_received={},
        current_question_index=0
    )
    
    # Return first question to start the interview
    if questions:
        first_question = questions[0]
        question_id = f"q_{session_id}_0"
        
        # Return the first question with all metadata
        return QuestionResponse(
            question_id=question_id,
            question=first_question["question"],
            question_type=request.interview_type,
            difficulty=first_question["difficulty"],
            suggested_time=first_question["suggested_time"]
        )
    else:
        # Raise error if no questions are available
        raise HTTPException(status_code=404, detail="No questions available for this interview type")

# ----------------------------------------------------------------------------
# NEXT QUESTION ENDPOINT
# Endpoint for getting the next question after submitting an answer
# ----------------------------------------------------------------------------

@app.post("/next-question", response_model=QuestionResponse)
async def next_question(request: AnswerRequest):
    """
    Submit answer to current question and get the next question
    
    Args:
        request (AnswerRequest): Request containing previous question ID and answer
        
    Returns:
        QuestionResponse: Next interview question with metadata
        
    Example:
        POST /next-question
        {
            "question_id": "q_12345_0",
            "answer": "A process is an independent unit of execution...",
            "job_title": "Software Engineer",
            "skills": ["Python", "JavaScript"]
        }
    """
    # In a real implementation, we would analyze the answer and adapt questions
    # For this mock, we'll just return a random question
    
    # Select a random question type for variety
    question_types = ["technical", "behavioral", "situational"]
    selected_type = random.choice(question_types)
    
    # Get questions based on selected type
    if selected_type == "technical":
        # Get a random technical question from available roles
        tech_roles = list(INTERVIEW_QUESTIONS["technical"].keys())
        selected_role = random.choice(tech_roles)
        questions = INTERVIEW_QUESTIONS["technical"][selected_role]
    elif selected_type == "behavioral":
        # Get behavioral questions
        questions = INTERVIEW_QUESTIONS["behavioral"]
    else:  # situational
        # Get situational questions
        questions = INTERVIEW_QUESTIONS["situational"]
    
    # Return a randomly selected question
    if questions:
        selected_question = random.choice(questions)
        question_id = f"q_mock_{random.randint(1000, 9999)}"
        
        # Return the next question with all metadata
        return QuestionResponse(
            question_id=question_id,
            question=selected_question["question"],
            question_type=selected_type,
            difficulty=selected_question["difficulty"],
            suggested_time=selected_question["suggested_time"]
        )
    else:
        # Raise error if no more questions are available
        raise HTTPException(status_code=404, detail="No more questions available")

# ----------------------------------------------------------------------------
# ANSWER SUBMISSION ENDPOINT
# Endpoint for submitting answers and getting AI-generated feedback
# ----------------------------------------------------------------------------

@app.post("/submit-answer", response_model=FeedbackResponse)
async def submit_answer(request: AnswerRequest):
    """
    Submit an answer and get AI-generated feedback
    
    Args:
        request (AnswerRequest): Request containing question ID, answer, job title, and skills
        
    Returns:
        FeedbackResponse: AI-generated feedback on the submitted answer
        
    Example:
        POST /submit-answer
        {
            "question_id": "q_12345_0",
            "answer": "A process is an independent unit of execution...",
            "job_title": "Software Engineer",
            "skills": ["Python", "JavaScript"]
        }
    """
    # Determine question type based on answer content and skills
    question_type = "technical" if any(skill.lower() in request.answer.lower() for skill in request.skills) else "behavioral"
    
    # Select appropriate feedback templates based on question type
    strengths = FEEDBACK_TEMPLATES.get(question_type, FEEDBACK_TEMPLATES["behavioral"])["strengths"]
    improvements = FEEDBACK_TEMPLATES.get(question_type, FEEDBACK_TEMPLATES["behavioral"])["improvements"]
    
    # Generate personalized feedback based on job title and answer
    feedback = f"Your answer to the {request.job_title} question shows good understanding. "
    feedback += "You provided relevant examples and demonstrated clear communication skills."
    
    # Generate score based on answer length and keywords (mock logic)
    score = min(10, max(1, len(request.answer.split()) // 10 + 5))
    
    # Select random strengths and improvements for variety
    selected_strengths = random.sample(strengths, min(2, len(strengths)))
    selected_improvements = random.sample(improvements, min(2, len(improvements)))
    
    # Generate follow-up questions for deeper exploration
    follow_up_questions = [
        "Can you tell me more about the challenges you faced in that situation?",
        "How would you approach a similar problem with different constraints?"
    ]
    
    # Generate learning resources for improvement
    resources = [
        f"https://interviewing.io/guides/{request.job_title.lower().replace(' ', '-')}-interview-questions",
        "https://www.pramp.com/#/"
    ]
    
    # Return comprehensive feedback with all components
    return FeedbackResponse(
        feedback=feedback,
        score=score,
        strengths=selected_strengths,
        improvements=selected_improvements,
        follow_up_questions=follow_up_questions,
        resources=resources
    )

# ----------------------------------------------------------------------------
# INTERVIEW COMPLETION ENDPOINT
# Endpoint for completing the interview and getting overall feedback
# ----------------------------------------------------------------------------

@app.post("/complete-interview", response_model=InterviewCompletion)
async def complete_interview(session_id: str):
    """
    Complete the interview session and provide overall feedback
    
    Args:
        session_id (str): ID of the interview session to complete
        
    Returns:
        InterviewCompletion: Overall interview results and feedback
        
    Example:
        POST /complete-interview?session_id=123e4567-e89b-12d3-a456-426614174000
    """
    # Verify that the session exists
    if session_id not in interview_sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    # Get session information
    session = interview_sessions[session_id]
    
    # Generate overall feedback based on session performance
    overall_feedback = f"Great job completing this mock interview for a {session_id} role. "
    overall_feedback += "You demonstrated strong communication skills and relevant knowledge."
    
    # Generate overall score (mock implementation)
    overall_score = random.randint(7, 9)
    
    # Generate key strengths observed during the interview
    strengths = [
        "Clear communication",
        "Good problem-solving approach",
        "Relevant examples from experience"
    ]
    
    # Generate areas for improvement
    areas_for_improvement = [
        "Try to be more concise in technical explanations",
        "Include more quantifiable results in your examples"
    ]
    
    # Generate personalized recommendations for further practice
    recommendations = [
        "Practice answering technical questions under time pressure",
        "Review common behavioral interview frameworks like STAR",
        "Research the company culture and values more deeply"
    ]
    
    # Clean up session data to free memory
    del interview_sessions[session_id]
    
    # Return comprehensive interview completion results
    return InterviewCompletion(
        session_id=session_id,
        overall_score=overall_score,
        overall_feedback=overall_feedback,
        strengths=strengths,
        areas_for_improvement=areas_for_improvement,
        recommendations=recommendations
    )

# ----------------------------------------------------------------------------
# QUESTION BANK ENDPOINT
# Endpoint for retrieving practice questions
# ----------------------------------------------------------------------------

@app.get("/question-bank")
async def get_question_bank(job_title: str = "software_engineer", question_type: str = "technical"):
    """
    Get a list of available questions for practice
    
    Args:
        job_title (str): Job title to get questions for (default: "software_engineer")
        question_type (str): Type of questions to retrieve (default: "technical")
        
    Returns:
        dict: List of available practice questions
        
    Example:
        GET /question-bank?job_title=data_scientist&question_type=technical
    """
    # Return questions based on requested job title and question type
    if question_type.lower() == "technical" and job_title.lower() in INTERVIEW_QUESTIONS["technical"]:
        return {"questions": INTERVIEW_QUESTIONS["technical"][job_title.lower()]}
    elif question_type.lower() == "behavioral":
        return {"questions": INTERVIEW_QUESTIONS["behavioral"]}
    elif question_type.lower() == "situational":
        return {"questions": INTERVIEW_QUESTIONS["situational"]}
    else:
        # Default to software engineer technical questions
        return {"questions": INTERVIEW_QUESTIONS["technical"]["software_engineer"]}

# ============================================================================
# APPLICATION ENTRY POINT
# Main execution block for running the service
# ============================================================================

if __name__ == "__main__":
    # Import uvicorn for running the ASGI application
    import uvicorn
    
    # Run the FastAPI application with uvicorn
    # Host 0.0.0.0 makes it accessible from outside the container
    # Port 8114 is the designated port for this microservice
    uvicorn.run(app, host="0.0.0.0", port=8114)