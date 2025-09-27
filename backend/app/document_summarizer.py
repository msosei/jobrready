"""
Document Summarizer Service for MyBrand Job Application Platform
Version: v2
Purpose: Provides AI-powered document summarization, comparison, and analysis capabilities
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for document summarization functionality
# ============================================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os

# ============================================================================
# ROUTER CONFIGURATION
# Create router for document summarizer endpoints with appropriate prefix and tags
# ============================================================================

router = APIRouter(prefix="/document-summarizer", tags=["Document Summarizer"])

# ============================================================================
# SERVICE CONFIGURATION
# Get the service URL from environment variables for microservice communication
# ============================================================================

# Get the document summarizer service URL from environment variables
# In development, this would be http://localhost:8116
# In production, this would be the deployed service URL
DOCUMENT_SUMMARIZER_SERVICE_URL = os.getenv("DOCUMENT_SUMMARIZER_SERVICE_URL", "http://document_summarizer:8116")

# ============================================================================
# DATA MODELS
# Pydantic models for document summarization data structures and API requests
# ============================================================================

class DocumentRequest(BaseModel):
    """
    Request model for document processing operations.
    
    Contains the document text to process along with type and processing preferences.
    """
    document_text: str
    document_type: str
    summary_length: Optional[str] = "medium"

class DocumentComparisonRequest(BaseModel):
    """
    Request model for comparing two documents.
    
    Contains two documents to compare along with their types for contextual analysis.
    """
    document1_text: str
    document2_text: str
    document1_type: str
    document2_type: str

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for document summarization functionality
# ============================================================================

@router.post("/summarize")
async def summarize_document(request: DocumentRequest):
    """
    Summarize a document based on its type and desired length.
    
    This endpoint forwards the document summarization request to a dedicated
    microservice that uses AI to create concise summaries of various document
    types while preserving key information and context.
    
    Args:
        request (DocumentRequest): Contains document text, type, and summary preferences
        
    Returns:
        dict: Generated document summary with metadata
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = DocumentRequest(
        ...     document_text="Long document content...",
        ...     document_type="job_description",
        ...     summary_length="short"
        ... )
        >>> summary = await summarize_document(request)
        >>> print(f"Summary: {summary['summary']}")
    """
    # Forward the request to the document summarizer microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{DOCUMENT_SUMMARIZER_SERVICE_URL}/summarize",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Document summarizer service unavailable: {str(e)}"
            )

@router.post("/compare")
async def compare_documents(request: DocumentComparisonRequest):
    """
    Compare two documents for similarities and differences.
    
    This endpoint forwards the document comparison request to a dedicated
    microservice that analyzes two documents to identify similarities,
    differences, and potential alignment issues.
    
    Args:
        request (DocumentComparisonRequest): Contains two documents to compare
        
    Returns:
        dict: Comparison results including similarities, differences, and alignment score
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = DocumentComparisonRequest(
        ...     document1_text="Resume content...",
        ...     document2_text="Job description content...",
        ...     document1_type="resume",
        ...     document2_type="job_description"
        ... )
        >>> comparison = await compare_documents(request)
        >>> print(f"Alignment score: {comparison['alignment_score']}")
    """
    # Forward the request to the document summarizer microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{DOCUMENT_SUMMARIZER_SERVICE_URL}/compare",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Document summarizer service unavailable: {str(e)}"
            )

@router.post("/extract-keywords")
async def extract_keywords(request: DocumentRequest):
    """
    Extract keywords, skills, and important terms from a document.
    
    This endpoint forwards the keyword extraction request to a dedicated
    microservice that identifies and extracts important terms, skills,
    and concepts from document content.
    
    Args:
        request (DocumentRequest): Contains document text and type for analysis
        
    Returns:
        dict: Extracted keywords, skills, and important terms with relevance scores
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = DocumentRequest(
        ...     document_text="Experienced Python developer with AWS and React skills...",
        ...     document_type="resume"
        ... )
        >>> keywords = await extract_keywords(request)
        >>> print(f"Extracted skills: {keywords['skills']}")
    """
    # Forward the request to the document summarizer microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{DOCUMENT_SUMMARIZER_SERVICE_URL}/extract-keywords",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Document summarizer service unavailable: {str(e)}"
            )

@router.post("/analyze")
async def analyze_document(request: DocumentRequest):
    """
    Provide insights about a document's readability, sentiment, and tone.
    
    This endpoint forwards the document analysis request to a dedicated
    microservice that evaluates document characteristics including
    readability metrics, sentiment analysis, and tone assessment.
    
    Args:
        request (DocumentRequest): Contains document text and type for analysis
        
    Returns:
        dict: Document analysis results including readability, sentiment, and tone
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = DocumentRequest(
        ...     document_text="We are seeking a talented software engineer...",
        ...     document_type="job_description"
        ... )
        >>> analysis = await analyze_document(request)
        >>> print(f"Readability score: {analysis['readability_score']}")
    """
    # Forward the request to the document summarizer microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{DOCUMENT_SUMMARIZER_SERVICE_URL}/analyze",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Document summarizer service unavailable: {str(e)}"
            )

@router.get("/templates")
async def get_summary_templates(document_type: str = "resume"):
    """
    Get templates for different types of document summaries.
    
    This endpoint retrieves pre-defined summary templates from the
    document summarizer microservice for various document types.
    
    Args:
        document_type (str): Type of document to get templates for (default: "resume")
        
    Returns:
        dict: Available summary templates for the specified document type
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> templates = await get_summary_templates("cover_letter")
        >>> print(f"Available templates: {list(templates.keys())}")
    """
    # Forward the request to the document summarizer microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{DOCUMENT_SUMMARIZER_SERVICE_URL}/templates",
                params={"document_type": document_type},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Document summarizer service unavailable: {str(e)}"
            )