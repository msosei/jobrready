"""
Document Summarizer Service
Version: 1.0
Purpose: AI service that summarizes resumes, job descriptions, and other career-related documents

This microservice provides functionality to:
1. Summarize various types of career documents
2. Compare documents for compatibility analysis
3. Extract keywords, skills, and important terms
4. Analyze document readability, sentiment, and tone
5. Provide templates for different document types
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
    title="Document Summarizer",
    description="AI service that summarizes resumes, job descriptions, and other career-related documents",
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

class DocumentRequest(BaseModel):
    """Request model for document processing"""
    document_text: str
    document_type: str  # resume, job_description, cover_letter, etc.
    summary_length: Optional[str] = "medium"  # short, medium, long

class DocumentComparisonRequest(BaseModel):
    """Request model for document comparison"""
    document1_text: str
    document2_text: str
    document1_type: str
    document2_type: str

# ----------------------------------------------------------------------------
# RESPONSE MODELS
# Models for API response data
# ----------------------------------------------------------------------------

class SummaryResponse(BaseModel):
    """Response model for document summarization"""
    summary: str
    key_points: List[str]
    word_count: int
    original_word_count: int
    compression_ratio: float

class ComparisonResponse(BaseModel):
    """Response model for document comparison"""
    similarities: List[str]
    differences: List[str]
    compatibility_score: float  # 0-100
    recommendations: List[str]

class KeywordExtractionResponse(BaseModel):
    """Response model for keyword extraction"""
    keywords: List[str]
    skills: List[str]
    action_verbs: List[str]
    industry_terms: List[str]

class DocumentInsightsResponse(BaseModel):
    """Response model for document analysis insights"""
    readability_score: float  # 0-100
    sentiment: str  # positive, neutral, negative
    tone: str  # professional, casual, technical, etc.
    suggestions: List[str]

# ============================================================================
# DOCUMENT PROCESSING DATABASE
# Collections of skills, action verbs, and keywords for document analysis
# ============================================================================

# ----------------------------------------------------------------------------
# SKILLS DATABASE
# List of common professional skills for keyword extraction
# ----------------------------------------------------------------------------

SKILLS_DATABASE = [
    "Python", "JavaScript", "Java", "C++", "React", "Angular", "Vue.js", 
    "Node.js", "Express", "Django", "Flask", "AWS", "Docker", "Kubernetes",
    "SQL", "MongoDB", "PostgreSQL", "Git", "CI/CD", "Agile", "Scrum",
    "Machine Learning", "Data Analysis", "Project Management", "Leadership"
]

# ----------------------------------------------------------------------------
# ACTION VERBS
# List of action verbs commonly found in professional documents
# ----------------------------------------------------------------------------

ACTION_VERBS = [
    "developed", "managed", "implemented", "designed", "created", "optimized",
    "analyzed", "collaborated", "led", "mentored", "streamlined", "automated"
]

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the document summarizer service
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
    return {"message": "Document Summarizer Service is running"}

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
# DOCUMENT SUMMARIZATION ENDPOINT
# Endpoint for summarizing documents based on type and desired length
# ----------------------------------------------------------------------------

@app.post("/summarize", response_model=SummaryResponse)
async def summarize_document(request: DocumentRequest):
    """
    Summarize a document based on its type and desired length
    
    Args:
        request (DocumentRequest): Request containing document text, type, and summary length preference
        
    Returns:
        SummaryResponse: Response with document summary, key points, and statistics
        
    Example:
        POST /summarize
        {
            "document_text": "Experienced software engineer with 5 years of Python development...",
            "document_type": "resume",
            "summary_length": "medium"
        }
    """
    # In a real implementation, this would use NLP techniques
    # For this mock, we'll generate a summary based on the document type
    
    # Split document into sentences for processing
    sentences = request.document_text.split(". ")
    
    # Determine summary length based on user preference
    if request.summary_length == "short":
        num_sentences = max(1, len(sentences) // 4)
    elif request.summary_length == "long":
        num_sentences = max(2, len(sentences) // 2)
    else:  # medium
        num_sentences = max(1, len(sentences) // 3)
    
    # Select sentences for summary (in a real implementation, this would use more sophisticated methods)
    summary_sentences = sentences[:num_sentences] if len(sentences) > num_sentences else sentences
    summary = ". ".join(summary_sentences) + "." if summary_sentences else "No summary available."
    
    # Extract key points from the summary sentences
    key_points = []
    for i, sentence in enumerate(summary_sentences[:5]):  # Limit to 5 key points
        if sentence.strip():
            key_points.append(f"Key point {i+1}: {sentence.strip()}")
    
    # Calculate document statistics
    original_word_count = len(request.document_text.split())
    summary_word_count = len(summary.split())
    compression_ratio = summary_word_count / original_word_count if original_word_count > 0 else 0
    
    # Return the summary response with all generated information
    return SummaryResponse(
        summary=summary,
        key_points=key_points,
        word_count=summary_word_count,
        original_word_count=original_word_count,
        compression_ratio=compression_ratio
    )

# ----------------------------------------------------------------------------
# DOCUMENT COMPARISON ENDPOINT
# Endpoint for comparing two documents for similarities and differences
# ----------------------------------------------------------------------------

@app.post("/compare", response_model=ComparisonResponse)
async def compare_documents(request: DocumentComparisonRequest):
    """
    Compare two documents for similarities and differences
    
    Args:
        request (DocumentComparisonRequest): Request containing two documents and their types
        
    Returns:
        ComparisonResponse: Response with similarities, differences, compatibility score, and recommendations
        
    Example:
        POST /compare
        {
            "document1_text": "John Doe's resume with Python experience...",
            "document2_text": "Job description for Python developer...",
            "document1_type": "resume",
            "document2_type": "job_description"
        }
    """
    # In a real implementation, this would use document similarity algorithms
    # For this mock, we'll generate comparison results based on document types
    
    # Initialize lists for storing comparison results
    similarities = []
    differences = []
    recommendations = []
    
    # Generate comparison results based on document types
    if request.document1_type == "resume" and request.document2_type == "job_description":
        # Specific comparison logic for resume vs job description
        similarities.append("Both documents mention software development experience")
        similarities.append("Both reference Python programming skills")
        differences.append("Resume emphasizes backend development while job focuses on full-stack")
        recommendations.append("Highlight full-stack experience in resume")
        recommendations.append("Emphasize backend projects that align with job requirements")
        compatibility_score = 85.5
    elif request.document1_type == "cover_letter" and request.document2_type == "job_description":
        # Specific comparison logic for cover letter vs job description
        similarities.append("Both documents mention the company's mission")
        differences.append("Cover letter focuses on personal experience while job description focuses on requirements")
        recommendations.append("Align personal achievements more closely with job requirements")
        compatibility_score = 72.0
    else:
        # Generic comparison for other document type combinations
        similarities.append("Both documents are well-structured")
        differences.append("Documents have different focus areas")
        recommendations.append("Consider tailoring content to specific audience")
        compatibility_score = random.uniform(60, 90)
    
    # Return the comparison response with all analysis results
    return ComparisonResponse(
        similarities=similarities,
        differences=differences,
        compatibility_score=compatibility_score,
        recommendations=recommendations
    )

# ----------------------------------------------------------------------------
# KEYWORD EXTRACTION ENDPOINT
# Endpoint for extracting keywords, skills, and important terms from documents
# ----------------------------------------------------------------------------

@app.post("/extract-keywords", response_model=KeywordExtractionResponse)
async def extract_keywords(request: DocumentRequest):
    """
    Extract keywords, skills, and important terms from a document
    
    Args:
        request (DocumentRequest): Request containing document text and type
        
    Returns:
        KeywordExtractionResponse: Response with extracted keywords, skills, action verbs, and industry terms
        
    Example:
        POST /extract-keywords
        {
            "document_text": "Experienced Python developer with skills in Django and AWS...",
            "document_type": "resume"
        }
    """
    # In a real implementation, this would use NLP techniques like TF-IDF or named entity recognition
    # For this mock, we'll identify keywords based on our database
    
    # Convert document to lowercase for case-insensitive matching
    doc_lower = request.document_text.lower()
    
    # Extract skills from document by matching against skills database
    found_skills = [skill for skill in SKILLS_DATABASE if skill.lower() in doc_lower]
    
    # Extract action verbs from document by matching against action verbs list
    found_verbs = [verb for verb in ACTION_VERBS if verb.lower() in doc_lower]
    
    # Extract other common keywords from document
    common_keywords = ["experience", "skills", "responsibilities", "requirements", "qualifications"]
    found_keywords = [keyword for keyword in common_keywords if keyword.lower() in doc_lower]
    
    # Extract industry terms from document
    industry_terms = ["innovation", "efficiency", "collaboration", "leadership", "growth"]
    found_industry_terms = [term for term in industry_terms if term.lower() in doc_lower]
    
    # Return the keyword extraction response with all found terms
    return KeywordExtractionResponse(
        keywords=found_keywords,
        skills=found_skills[:10],  # Limit to 10 skills for readability
        action_verbs=found_verbs[:10],  # Limit to 10 verbs for readability
        industry_terms=found_industry_terms
    )

# ----------------------------------------------------------------------------
# DOCUMENT ANALYSIS ENDPOINT
# Endpoint for providing insights about document readability, sentiment, and tone
# ----------------------------------------------------------------------------

@app.post("/analyze", response_model=DocumentInsightsResponse)
async def analyze_document(request: DocumentRequest):
    """
    Provide insights about a document's readability, sentiment, and tone
    
    Args:
        request (DocumentRequest): Request containing document text and type
        
    Returns:
        DocumentInsightsResponse: Response with readability score, sentiment, tone, and suggestions
        
    Example:
        POST /analyze
        {
            "document_text": "I successfully led a team of developers to complete a project...",
            "document_type": "resume"
        }
    """
    # In a real implementation, this would use NLP libraries for analysis
    # For this mock, we'll generate insights based on document characteristics
    
    # Calculate document word count for analysis
    word_count = len(request.document_text.split())
    
    # Calculate readability score based on document length
    if word_count < 100:
        readability_score = 90
    elif word_count < 300:
        readability_score = 80
    elif word_count < 500:
        readability_score = 70
    else:
        readability_score = 60
    
    # Determine sentiment by analyzing positive and negative words
    positive_words = ["success", "achieved", "improved", "excellent", "outstanding", "exceptional"]
    negative_words = ["failed", "difficult", "challenging", "problem", "issue"]
    
    # Count positive and negative word occurrences
    pos_count = sum(1 for word in positive_words if word in request.document_text.lower())
    neg_count = sum(1 for word in negative_words if word in request.document_text.lower())
    
    # Determine overall sentiment based on word counts
    if pos_count > neg_count:
        sentiment = "positive"
    elif neg_count > pos_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    # Determine document tone based on document type
    if request.document_type == "resume":
        tone = "professional"
    elif request.document_type == "cover_letter":
        tone = "professional"
    elif request.document_type == "job_description":
        tone = "technical"
    else:
        tone = "neutral"
    
    # Generate actionable suggestions based on analysis
    suggestions = []
    if word_count > 500:
        suggestions.append("Consider shortening the document for better readability")
    
    if sentiment == "negative":
        suggestions.append("Use more positive language to describe challenges and solutions")
    
    if "experience" not in request.document_text.lower() and request.document_type in ["resume", "cover_letter"]:
        suggestions.append("Include more specific details about your experience")
    
    # Return the document insights response with all analysis results
    return DocumentInsightsResponse(
        readability_score=readability_score,
        sentiment=sentiment,
        tone=tone,
        suggestions=suggestions
    )

# ----------------------------------------------------------------------------
# SUMMARY TEMPLATES ENDPOINT
# Endpoint for retrieving templates for different document types
# ----------------------------------------------------------------------------

@app.get("/templates")
async def get_summary_templates(document_type: str = "resume"):
    """
    Get templates for different types of document summaries
    
    Args:
        document_type (str): Type of document to get template for (default: "resume")
        
    Returns:
        dict: Template structure and recommendations for the specified document type
        
    Example:
        GET /templates?document_type=job_description
    """
    # Define templates for different document types
    templates = {
        "resume": {
            "structure": "Summary of professional experience, key skills, and achievements",
            "key_sections": ["Professional Summary", "Core Competencies", "Career Highlights"],
            "recommended_length": "100-200 words"
        },
        "job_description": {
            "structure": "Overview of role responsibilities, required qualifications, and company information",
            "key_sections": ["Role Overview", "Key Responsibilities", "Qualifications"],
            "recommended_length": "150-250 words"
        },
        "cover_letter": {
            "structure": "Introduction, body paragraphs highlighting relevant experience, closing statement",
            "key_sections": ["Introduction", "Relevant Experience", "Value Proposition", "Closing"],
            "recommended_length": "200-300 words"
        }
    }
    
    # Return template for requested document type or default to resume template
    return templates.get(document_type, templates["resume"])

# ============================================================================
# APPLICATION ENTRY POINT
# Main execution block for running the service
# ============================================================================

if __name__ == "__main__":
    # Import uvicorn for running the ASGI application
    import uvicorn
    
    # Run the FastAPI application with uvicorn
    # Host 0.0.0.0 makes it accessible from outside the container
    # Port 8116 is the designated port for this microservice
    uvicorn.run(app, host="0.0.0.0", port=8116)