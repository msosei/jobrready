"""
Mock Interviewer Service for MyBrand Job Application Platform
Version: v2
Purpose: Provides AI-powered mock interview experiences for job candidates
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for mock interview functionality
# ============================================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os

# ============================================================================
# ROUTER CONFIGURATION
# Create router for mock interviewer endpoints with appropriate prefix and tags
# ============================================================================

router = APIRouter(prefix="/mock-interviewer", tags=["Mock Interviewer"])

# ============================================================================
# SERVICE CONFIGURATION
# Get the service URL from environment variables for microservice communication
# ============================================================================

# Get the mock interviewer service URL from environment variables
# In development, this would be http://localhost:8114
# In production, this would be the deployed service URL
MOCK_INTERVIEWER_SERVICE_URL = os.getenv("MOCK_INTERVIEWER_SERVICE_URL", "http://mock_interviewer:8114")

# ============================================================================
# DATA MODELS
# Pydantic models for mock interview data structures and API requests
# ============================================================================

class InterviewRequest(BaseModel):
    """
    Request model for starting a mock interview session.
    
    Contains information about the job position, industry, experience level,
    and other factors to customize the interview experience.
    """
    job_title: str
    industry: str
    experience_level: str
    interview_type: str
    skills: List[str]
    resume_summary: Optional[str] = None
    company_info: Optional[str] = None

class AnswerRequest(BaseModel):
    """
    Request model for submitting interview answers.
    
    Contains the question ID, candidate's answer, and context information
    for providing feedback and generating follow-up questions.
    """
    question_id: str
    answer: str
    job_title: str
    skills: List[str]

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for mock interview functionality
# ============================================================================

@router.post("/start-interview")
async def start_interview(request: InterviewRequest):
    """
    Start a new mock interview session.
    
    This endpoint initializes a new mock interview session by forwarding
    the request to the dedicated mock interviewer microservice, which
    generates personalized interview questions based on the provided context.
    
    Args:
        request (InterviewRequest): Contains job and candidate information
        
    Returns:
        dict: Interview session details including first question
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = InterviewRequest(
        ...     job_title="Software Engineer",
        ...     industry="Technology",
        ...     experience_level="Mid-level",
        ...     interview_type="Technical",
        ...     skills=["Python", "React", "AWS"]
        ... )
        >>> response = await start_interview(request)
        >>> print(f"Interview started with question: {response['question']}")
    """
    # Forward the request to the mock interviewer microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{MOCK_INTERVIEWER_SERVICE_URL}/start-interview",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Mock interviewer service unavailable: {str(e)}"
            )

@router.post("/next-question")
async def next_question(request: AnswerRequest):
    """
    Get the next interview question in the session.
    
    This endpoint requests the next question in an ongoing mock interview
    session from the dedicated microservice, which generates follow-up
    questions based on previous answers and session context.
    
    Args:
        request (AnswerRequest): Contains previous answer and context
        
    Returns:
        dict: Next interview question and related information
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = AnswerRequest(
        ...     question_id="q123",
        ...     answer="I used Python and Django to build a REST API...",
        ...     job_title="Software Engineer",
        ...     skills=["Python", "Django", "REST"]
        ... )
        >>> response = await next_question(request)
        >>> print(f"Next question: {response['question']}")
    """
    # Forward the request to the mock interviewer microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{MOCK_INTERVIEWER_SERVICE_URL}/next-question",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Mock interviewer service unavailable: {str(e)}"
            )

@router.post("/submit-answer")
async def submit_answer(request: AnswerRequest):
    """
    Submit an interview answer and receive AI-powered feedback.
    
    This endpoint submits a candidate's answer to the mock interviewer
    microservice, which analyzes the response and provides detailed
    feedback on content, structure, and improvement suggestions.
    
    Args:
        request (AnswerRequest): Contains answer and context for feedback
        
    Returns:
        dict: Detailed feedback on the submitted answer
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = AnswerRequest(
        ...     question_id="q123",
        ...     answer="I used Python and Django to build a REST API...",
        ...     job_title="Software Engineer",
        ...     skills=["Python", "Django", "REST"]
        ... )
        >>> feedback = await submit_answer(request)
        >>> print(f"Feedback score: {feedback['score']}")
    """
    # Forward the request to the mock interviewer microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{MOCK_INTERVIEWER_SERVICE_URL}/submit-answer",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Mock interviewer service unavailable: {str(e)}"
            )

@router.post("/complete-interview")
async def complete_interview(session_id: str):
    """
    Complete the interview and receive overall performance feedback.
    
    This endpoint signals the completion of a mock interview session
    and requests comprehensive performance analysis from the microservice,
    including strengths, areas for improvement, and final recommendations.
    
    Args:
        session_id (str): Unique identifier for the interview session
        
    Returns:
        dict: Comprehensive interview performance analysis
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> feedback = await complete_interview("session123")
        >>> print(f"Overall score: {feedback['overall_score']}")
    """
    # Forward the request to the mock interviewer microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{MOCK_INTERVIEWER_SERVICE_URL}/complete-interview",
                params={"session_id": session_id},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Mock interviewer service unavailable: {str(e)}"
            )

@router.get("/question-bank")
async def get_question_bank(job_title: str = "software_engineer", question_type: str = "technical"):
    """
    Get a list of available questions for interview practice.
    
    This endpoint retrieves a bank of practice questions from the
    mock interviewer microservice, organized by job title and question type.
    
    Args:
        job_title (str): Job title to filter questions (default: "software_engineer")
        question_type (str): Type of questions to retrieve (default: "technical")
        
    Returns:
        dict: Collection of practice questions for the specified criteria
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> questions = await get_question_bank("data_scientist", "behavioral")
        >>> print(f"Found {len(questions['questions'])} behavioral questions")
    """
    # Forward the request to the mock interviewer microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{MOCK_INTERVIEWER_SERVICE_URL}/question-bank",
                params={"job_title": job_title, "question_type": question_type},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Mock interviewer service unavailable: {str(e)}"
            )