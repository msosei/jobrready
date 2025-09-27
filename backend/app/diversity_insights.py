"""
Diversity Insights Service for MyBrand Job Application Platform
Version: v2
Purpose: Provides AI-powered diversity and inclusion analysis for job postings and companies
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for diversity insights functionality
# ============================================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os

# ============================================================================
# ROUTER CONFIGURATION
# Create router for diversity insights endpoints with appropriate prefix and tags
# ============================================================================

router = APIRouter(prefix="/diversity-insights", tags=["Diversity Insights"])

# ============================================================================
# SERVICE CONFIGURATION
# Get the service URL from environment variables for microservice communication
# ============================================================================

# Get the diversity insights service URL from environment variables
# In development, this would be http://localhost:8115
# In production, this would be the deployed service URL
DIVERSITY_INSIGHTS_SERVICE_URL = os.getenv("DIVERSITY_INSIGHTS_SERVICE_URL", "http://diversity_insights:8115")

# ============================================================================
# DATA MODELS
# Pydantic models for diversity insights data structures and API requests
# ============================================================================

class JobAnalysisRequest(BaseModel):
    """
    Request model for job posting diversity analysis.
    
    Contains information about a job posting to analyze for diversity
    and inclusion metrics, including title, description, and company context.
    """
    job_title: str
    company_name: str
    job_description: str
    company_description: Optional[str] = None
    industry: Optional[str] = None

class CompanyAnalysisRequest(BaseModel):
    """
    Request model for company inclusivity analysis.
    
    Contains comprehensive information about a company to analyze
    for inclusivity across multiple dimensions and metrics.
    """
    company_name: str
    company_description: str
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    locations: Optional[List[str]] = None

class BiasAnalysisRequest(BaseModel):
    """
    Request model for bias detection in text content.
    
    Contains text content to analyze for potential bias and provide
    suggestions for more inclusive language.
    """
    text_content: str

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for diversity insights functionality
# ============================================================================

@router.post("/analyze-job")
async def analyze_job_posting(request: JobAnalysisRequest):
    """
    Analyze a job posting for diversity and inclusion metrics.
    
    This endpoint forwards the job posting analysis request to a dedicated
    microservice that evaluates the job description for inclusive language,
    potential bias, and diversity metrics compared to industry benchmarks.
    
    Args:
        request (JobAnalysisRequest): Contains job posting information for analysis
        
    Returns:
        dict: Diversity and inclusion analysis results with recommendations
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = JobAnalysisRequest(
        ...     job_title="Senior Software Engineer",
        ...     company_name="TechCorp",
        ...     job_description="We're looking for an experienced developer...",
        ...     industry="Technology"
        ... )
        >>> analysis = await analyze_job_posting(request)
        >>> print(f"Inclusivity score: {analysis['inclusivity_score']}")
    """
    # Forward the request to the diversity insights microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{DIVERSITY_INSIGHTS_SERVICE_URL}/analyze-job",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Diversity insights service unavailable: {str(e)}"
            )

@router.post("/analyze-company")
async def analyze_company_inclusivity(request: CompanyAnalysisRequest):
    """
    Analyze a company's inclusivity across multiple dimensions.
    
    This endpoint forwards the company analysis request to a dedicated
    microservice that evaluates organizational inclusivity based on
    company description, size, locations, and industry context.
    
    Args:
        request (CompanyAnalysisRequest): Contains company information for analysis
        
    Returns:
        dict: Comprehensive inclusivity analysis with dimension scores
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = CompanyAnalysisRequest(
        ...     company_name="InclusiveTech",
        ...     company_description="We build technology for everyone...",
        ...     industry="Technology",
        ...     employee_count=500,
        ...     locations=["San Francisco", "New York", "Remote"]
        ... )
        >>> analysis = await analyze_company_inclusivity(request)
        >>> print(f"Overall inclusivity: {analysis['overall_score']}")
    """
    # Forward the request to the diversity insights microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{DIVERSITY_INSIGHTS_SERVICE_URL}/analyze-company",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Diversity insights service unavailable: {str(e)}"
            )

@router.post("/detect-bias")
async def detect_bias(request: BiasAnalysisRequest):
    """
    Detect bias in text content and suggest revisions.
    
    This endpoint forwards the bias detection request to a dedicated
    microservice that identifies potentially biased language in text
    and provides suggestions for more inclusive alternatives.
    
    Args:
        request (BiasAnalysisRequest): Contains text content to analyze for bias
        
    Returns:
        dict: Bias detection results with flagged content and suggestions
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = BiasAnalysisRequest(
        ...     text_content="We're looking for a strong candidate who can hit the ground running..."
        ... )
        >>> bias_results = await detect_bias(request)
        >>> print(f"Found {len(bias_results['issues'])} potential bias issues")
    """
    # Forward the request to the diversity insights microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{DIVERSITY_INSIGHTS_SERVICE_URL}/detect-bias",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Diversity insights service unavailable: {str(e)}"
            )

@router.post("/analyze-language")
async def analyze_language_inclusivity(request: BiasAnalysisRequest):
    """
    Analyze text for inclusive language usage.
    
    This endpoint forwards the language analysis request to a dedicated
    microservice that evaluates text content for inclusive language
    patterns and provides recommendations for improvement.
    
    Args:
        request (BiasAnalysisRequest): Contains text content to analyze for inclusivity
        
    Returns:
        dict: Language inclusivity analysis with scores and suggestions
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = BiasAnalysisRequest(
        ...     text_content="We're looking for the best candidate for this position..."
        ... )
        >>> language_analysis = await analyze_language_inclusivity(request)
        >>> print(f"Inclusive language score: {language_analysis['score']}")
    """
    # Forward the request to the diversity insights microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{DIVERSITY_INSIGHTS_SERVICE_URL}/analyze-language",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Diversity insights service unavailable: {str(e)}"
            )

@router.get("/industry-benchmarks")
async def get_industry_benchmarks(industry: str = "Technology"):
    """
    Get diversity and inclusion benchmarks for different industries.
    
    This endpoint retrieves industry-specific diversity and inclusion
    benchmarks from the dedicated microservice to help organizations
    compare their performance against industry standards.
    
    Args:
        industry (str): Industry to retrieve benchmarks for (default: "Technology")
        
    Returns:
        dict: Industry-specific diversity and inclusion benchmarks
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> benchmarks = await get_industry_benchmarks("Finance")
        >>> print(f"Industry benchmark score: {benchmarks['average_score']}")
    """
    # Forward the request to the diversity insights microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{DIVERSITY_INSIGHTS_SERVICE_URL}/industry-benchmarks",
                params={"industry": industry},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Diversity insights service unavailable: {str(e)}"
            )