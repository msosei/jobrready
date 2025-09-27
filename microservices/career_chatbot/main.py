"""
Career Chatbot Service
Version: 1.0
Purpose: Conversational AI for career guidance and job search assistance

This microservice provides functionality to:
1. Engage in conversational career guidance
2. Provide advice on resumes, interviews, job searching, and skill development
3. Generate contextual responses based on user input
4. Offer follow-up suggestions and next questions to continue conversations
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for the application
# ============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import random
import re

# ============================================================================
# APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata
# ============================================================================

app = FastAPI(
    title="AI Career Chatbot",
    description="Conversational AI for career guidance and job search assistance",
    version="1.0.0"
)

# ============================================================================
# DATA MODELS
# Pydantic models for data validation and serialization
# ============================================================================

# ----------------------------------------------------------------------------
# CHAT MESSAGE MODELS
# Models for handling chat conversation data
# ----------------------------------------------------------------------------

class ChatMessage(BaseModel):
    """Model for individual chat messages"""
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    """Request model for chat conversations"""
    messages: List[ChatMessage]
    user_id: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    """Response model for chat conversations"""
    response: str
    suggestions: List[str]
    next_questions: List[str]

# ----------------------------------------------------------------------------
# CAREER ADVICE MODELS
# Models for handling career advice requests and responses
# ----------------------------------------------------------------------------

class CareerAdviceRequest(BaseModel):
    """Request model for career advice"""
    topic: str  # "resume", "interview", "job_search", "career_change", "skill_development"
    user_profile: Optional[Dict[str, Any]] = None

class CareerAdviceResponse(BaseModel):
    """Response model for career advice"""
    advice: str
    resources: List[Dict[str, str]]
    action_items: List[str]

# ============================================================================
# KNOWLEDGE BASE
# Predefined knowledge and responses for different career topics
# ============================================================================

# ----------------------------------------------------------------------------
# CAREER TOPICS KNOWLEDGE BASE
# Comprehensive knowledge base with tips and common mistakes for each topic
# ----------------------------------------------------------------------------

# Knowledge base for different career topics
knowledge_base = {
    "resume": {
        "tips": [
            "Use action verbs to describe your accomplishments",
            "Quantify your achievements with numbers and metrics",
            "Tailor your resume for each job application",
            "Keep your resume to one page if you have less than 10 years of experience",
            "Use a clean, professional format that's easy to scan"
        ],
        "common_mistakes": [
            "Typos and grammatical errors",
            "Including irrelevant information",
            "Using an unprofessional email address",
            "Having inconsistent formatting",
            "Not quantifying achievements"
        ]
    },
    "interview": {
        "tips": [
            "Research the company and role thoroughly",
            "Practice answering common interview questions",
            "Prepare questions to ask the interviewer",
            "Dress appropriately for the company culture",
            "Arrive 10-15 minutes early"
        ],
        "common_mistakes": [
            "Not preparing specific examples of your work",
            "Speaking negatively about previous employers",
            "Not asking questions about the role or company",
            "Being unprepared to discuss salary expectations",
            "Poor body language or lack of eye contact"
        ]
    },
    "job_search": {
        "tips": [
            "Use multiple job boards and company websites",
            "Network with professionals in your field",
            "Set up job alerts for relevant positions",
            "Follow up on applications within a week",
            "Consider working with a recruiter"
        ],
        "common_mistakes": [
            "Applying to jobs without customizing your application",
            "Not following application instructions",
            "Applying to too many jobs without quality",
            "Not leveraging your professional network",
            "Giving up after a few rejections"
        ]
    },
    "career_change": {
        "tips": [
            "Identify transferable skills from your current role",
            "Research the new field thoroughly",
            "Consider taking courses or earning certifications",
            "Network with professionals in the target field",
            "Start making the transition while still employed"
        ],
        "common_mistakes": [
            "Not researching the new field adequately",
            "Underestimating the time and effort required",
            "Not building a network in the new field",
            "Making the change without a financial plan",
            "Expecting immediate success"
        ]
    },
    "skill_development": {
        "tips": [
            "Identify skills that are in high demand in your field",
            "Set specific, measurable learning goals",
            "Create a learning schedule and stick to it",
            "Practice new skills through projects or volunteer work",
            "Seek feedback from mentors or peers"
        ],
        "common_mistakes": [
            "Trying to learn too many skills at once",
            "Not practicing skills in real-world scenarios",
            "Not updating skills regularly",
            "Focusing only on technical skills and ignoring soft skills",
            "Not measuring progress or adjusting approach"
        ]
    }
}

# ----------------------------------------------------------------------------
# PREDEFINED RESPONSES
# Collection of predefined responses for common questions and greetings
# ----------------------------------------------------------------------------

# Predefined responses for common questions
predefined_responses = {
    "hello": ["Hi there! I'm your career assistant. How can I help you today?", "Hello! I'm here to help with your career journey. What would you like to discuss?"],
    "hi": ["Hi there! I'm your career assistant. How can I help you today?", "Hello! I'm here to help with your career journey. What would you like to discuss?"],
    "help": ["I can help you with resume tips, interview preparation, job search strategies, career change advice, and skill development. What topic would you like to explore?", "I'm here to assist with various career topics. You can ask me about resumes, interviews, job searching, changing careers, or developing new skills."],
    "resume": ["I'd be happy to help with your resume! I can provide tips on formatting, content, and how to tailor it for specific roles. What specific aspect of your resume would you like advice on?", "Resume help is one of my specialties! I can suggest improvements to make your resume stand out. Do you have a specific resume question?"],
    "interview": ["Preparing for an interview? I can help you with common questions, how to present yourself, and strategies for success. What type of interview are you preparing for?", "Interview preparation is crucial for success! I can provide tips on how to answer questions, what to wear, and how to follow up. What would you like to know?"],
    "job": ["Looking for job search advice? I can help with strategies for finding opportunities, networking, and making your applications stand out. Are you currently job searching?", "Job searching can be challenging, but I'm here to help! I can provide tips on where to look, how to apply, and how to follow up. What aspect of job searching would you like advice on?"],
    "career": ["Thinking about your career path? I can help with advice on career changes, advancement, and long-term planning. What career topic would you like to discuss?", "Career development is important for long-term success. I can provide guidance on setting goals, identifying opportunities, and making strategic moves. What's on your mind?"],
    "skill": ["Developing new skills is key to career growth! I can help you identify in-demand skills and suggest resources for learning. What skills are you interested in developing?", "Skill development is crucial in today's job market. I can provide advice on how to learn effectively and which skills are most valuable. What would you like to learn?"],
    "thank": ["You're welcome! Feel free to ask anytime you need career advice.", "Happy to help! Don't hesitate to reach out if you have more questions."],
    "bye": ["Goodbye! Best of luck with your career journey!", "Take care! Remember, I'm here whenever you need career guidance."]
}

# ============================================================================
# CORE FUNCTIONS
# Main functions for generating responses, suggestions, and advice
# ============================================================================

# ----------------------------------------------------------------------------
# CONTEXTUAL RESPONSE GENERATION
# Function to generate contextual responses based on user input
# ----------------------------------------------------------------------------

def generate_contextual_response(user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate a contextual response based on the user's message
    
    Args:
        user_message (str): The user's message to respond to
        context (Optional[Dict[str, Any]]): Additional context for the conversation
        
    Returns:
        str: Generated response to the user's message
    """
    message_lower = user_message.lower()
    
    # Check for predefined responses
    for key, responses in predefined_responses.items():
        if key in message_lower:
            return random.choice(responses)
    
    # Generate a response based on keywords
    if "resume" in message_lower:
        return random.choice([
            "When it comes to resumes, focus on quantifying your achievements. Instead of saying 'Managed a team,' try 'Managed a team of 5 people, increasing productivity by 20%.'",
            "A strong resume uses keywords from the job description. Make sure to include relevant skills and experiences that match what the employer is looking for.",
            "Keep your resume concise and focused on achievements rather than responsibilities. Use bullet points to make it easy to scan."
        ])
    elif "interview" in message_lower:
        return random.choice([
            "For interviews, practice the STAR method - Situation, Task, Action, Result. This helps you structure your responses to behavioral questions.",
            "Research common interview questions for your field and practice answering them out loud. This will help you feel more confident and articulate.",
            "Remember to ask thoughtful questions at the end of the interview. This shows your interest in the role and helps you determine if it's a good fit."
        ])
    elif "job" in message_lower:
        return random.choice([
            "When job searching, don't just apply online. Reach out to people in your network who work at companies you're interested in.",
            "Set up job alerts on multiple platforms to ensure you don't miss opportunities that match your criteria.",
            "Customize your application materials for each position. Generic applications are easy to spot and often get rejected."
        ])
    elif "career" in message_lower:
        return random.choice([
            "Career growth often comes from taking on new challenges. Look for opportunities to lead projects or develop new skills in your current role.",
            "Consider finding a mentor in your field. They can provide valuable guidance and may even help open doors to new opportunities.",
            "Regular self-assessment is important for career development. Take time to evaluate your goals and progress periodically."
        ])
    elif "skill" in message_lower:
        return random.choice([
            "Focus on developing both technical and soft skills. Employers value well-rounded candidates who can communicate effectively and work well in teams.",
            "Online learning platforms like Coursera, Udemy, and LinkedIn Learning offer courses on almost any skill you want to develop.",
            "Practice new skills through personal projects or volunteer work. This gives you hands-on experience and something to showcase."
        ])
    else:
        # Default response
        return random.choice([
            "That's an interesting point. Could you tell me more about what you're looking for?",
            "I'd be happy to help with that. Can you provide a bit more detail about your situation?",
            "That's a great question. Let me think about how I can best assist you with this.",
            "I understand you're interested in this topic. What specific aspect would you like to explore?"
        ])

# ----------------------------------------------------------------------------
# SUGGESTION GENERATION
# Function to generate follow-up suggestions based on user input
# ----------------------------------------------------------------------------

def generate_suggestions(user_message: str) -> List[str]:
    """
    Generate follow-up suggestions based on the user's message
    
    Args:
        user_message (str): The user's message to base suggestions on
        
    Returns:
        List[str]: List of follow-up suggestions
    """
    message_lower = user_message.lower()
    
    if "resume" in message_lower:
        return [
            "Get resume formatting tips",
            "Learn how to quantify achievements",
            "See examples of strong resumes"
        ]
    elif "interview" in message_lower:
        return [
            "Practice common interview questions",
            "Learn about body language tips",
            "Get advice on salary negotiation"
        ]
    elif "job" in message_lower:
        return [
            "Discover effective job search strategies",
            "Learn networking techniques",
            "Get tips on following up with employers"
        ]
    elif "career" in message_lower:
        return [
            "Explore career change options",
            "Learn about career advancement",
            "Get advice on setting career goals"
        ]
    elif "skill" in message_lower:
        return [
            "Identify in-demand skills",
            "Find learning resources",
            "Get advice on skill practice"
        ]
    else:
        return [
            "Get resume advice",
            "Prepare for interviews",
            "Improve job search strategies",
            "Explore career development",
            "Develop new skills"
        ]

# ----------------------------------------------------------------------------
# NEXT QUESTION GENERATION
# Function to generate next questions to continue the conversation
# ----------------------------------------------------------------------------

def generate_next_questions(user_message: str) -> List[str]:
    """
    Generate next questions to keep the conversation going
    
    Args:
        user_message (str): The user's message to base next questions on
        
    Returns:
        List[str]: List of follow-up questions
    """
    message_lower = user_message.lower()
    
    if "resume" in message_lower:
        return [
            "Would you like help with resume formatting?",
            "Do you need assistance quantifying your achievements?",
            "Are you struggling with a particular section of your resume?"
        ]
    elif "interview" in message_lower:
        return [
            "Are you preparing for a specific type of interview?",
            "Do you need help with behavioral questions?",
            "Would you like mock interview practice?"
        ]
    elif "job" in message_lower:
        return [
            "Are you currently job searching?",
            "Do you need help with networking?",
            "Would you like tips on job boards to use?"
        ]
    elif "career" in message_lower:
        return [
            "Are you considering a career change?",
            "Do you need help setting career goals?",
            "Are you looking for advancement opportunities?"
        ]
    elif "skill" in message_lower:
        return [
            "What specific skills are you looking to develop?",
            "Do you need help finding learning resources?",
            "Are you looking to certify any skills?"
        ]
    else:
        return [
            "What aspect of your career are you most interested in improving?",
            "Do you have a specific career challenge you're facing?",
            "What are your career goals for the next year?"
        ]

# ----------------------------------------------------------------------------
# CAREER ADVICE GENERATION
# Function to generate comprehensive career advice for specific topics
# ----------------------------------------------------------------------------

def generate_career_advice(topic: str, user_profile: Optional[Dict[str, Any]] = None) -> tuple[str, List[Dict[str, str]], List[str]]:
    """
    Generate career advice for a specific topic
    
    Args:
        topic (str): The career topic to provide advice on
        user_profile (Optional[Dict[str, Any]]): User profile information for personalized advice
        
    Returns:
        tuple[str, List[Dict[str, str]], List[str]]: Advice text, resources, and action items
    """
    if topic not in knowledge_base:
        topic = "resume"  # Default to resume advice
    
    topic_info = knowledge_base[topic]
    
    # Generate advice
    advice = f"Here's some advice on {topic.replace('_', ' ')}:\n\n"
    advice += "Key Tips:\n"
    for i, tip in enumerate(topic_info["tips"][:3], 1):
        advice += f"{i}. {tip}\n"
    
    advice += "\nCommon Mistakes to Avoid:\n"
    for i, mistake in enumerate(topic_info["common_mistakes"][:3], 1):
        advice += f"{i}. {mistake}\n"
    
    # Generate resources
    resources = [
        {"title": f"{topic.title()} Best Practices Guide", "url": f"https://example.com/{topic}-guide"},
        {"title": f"Top 10 {topic.title()} Tips", "url": f"https://example.com/{topic}-tips"},
        {"title": f"{topic.title()} Video Tutorial", "url": f"https://example.com/{topic}-tutorial"}
    ]
    
    # Generate action items
    action_items = [
        f"Review your {topic.replace('_', ' ')} for the common mistakes mentioned",
        f"Implement at least one of the tips provided",
        "Set a reminder to follow up on your progress in one week"
    ]
    
    return advice, resources, action_items

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the career chatbot service
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
# CHAT CONVERSATION ENDPOINT
# Endpoint for handling chat conversations with the career assistant
# ----------------------------------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle chat conversations with the career assistant
    
    Args:
        request (ChatRequest): Request containing chat messages and context
        
    Returns:
        ChatResponse: Generated response with suggestions and next questions
        
    Example:
        POST /chat
        {
            "messages": [
                {"role": "user", "content": "I need help with my resume"}
            ],
            "user_id": "user123"
        }
    """
    try:
        # Get the last user message
        user_message = ""
        for message in reversed(request.messages):
            if message.role == "user":
                user_message = message.content
                break
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No user message found")
        
        # Generate response
        response_text = generate_contextual_response(user_message, request.context)
        suggestions = generate_suggestions(user_message)
        next_questions = generate_next_questions(user_message)
        
        return ChatResponse(
            response=response_text,
            suggestions=suggestions,
            next_questions=next_questions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chat response: {str(e)}")

# ----------------------------------------------------------------------------
# CAREER ADVICE ENDPOINT
# Endpoint for providing career advice on specific topics
# ----------------------------------------------------------------------------

@app.post("/career-advice", response_model=CareerAdviceResponse)
async def get_career_advice(request: CareerAdviceRequest):
    """
    Get career advice on a specific topic
    
    Args:
        request (CareerAdviceRequest): Request containing the topic and user profile
        
    Returns:
        CareerAdviceResponse: Career advice with resources and action items
        
    Example:
        POST /career-advice
        {
            "topic": "resume",
            "user_profile": {"experience_years": 5, "industry": "technology"}
        }
    """
    try:
        advice, resources, action_items = generate_career_advice(
            request.topic, request.user_profile
        )
        
        return CareerAdviceResponse(
            advice=advice,
            resources=resources,
            action_items=action_items
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating career advice: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8112)