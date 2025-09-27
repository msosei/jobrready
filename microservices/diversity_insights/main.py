"""
Diversity & Inclusion Insights Service
Version: 1.0
Purpose: AI service that analyzes job postings and companies for diversity and inclusion metrics

This microservice provides functionality to:
1. Analyze job postings for diversity and inclusion metrics
2. Evaluate company inclusivity across multiple dimensions
3. Detect biased language in text content
4. Provide language inclusivity analysis
5. Offer industry benchmarks for comparison
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
    title="Diversity & Inclusion Insights",
    description="AI service that analyzes job postings and companies for diversity and inclusion metrics",
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

class JobAnalysisRequest(BaseModel):
    """Request model for job posting analysis"""
    job_title: str
    company_name: str
    job_description: str
    company_description: Optional[str] = None
    industry: Optional[str] = None

class CompanyAnalysisRequest(BaseModel):
    """Request model for company inclusivity analysis"""
    company_name: str
    company_description: str
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    locations: Optional[List[str]] = None

class BiasAnalysisRequest(BaseModel):
    """Request model for bias detection in text content"""
    text_content: str  # Job description, company policy, etc.

# ----------------------------------------------------------------------------
# RESPONSE MODELS
# Models for API response data
# ----------------------------------------------------------------------------

class DiversityScoreResponse(BaseModel):
    """Response model for diversity and inclusion scores"""
    diversity_score: float  # 0-100
    inclusion_score: float  # 0-100
    overall_rating: str  # Poor, Fair, Good, Excellent
    strengths: List[str]
    areas_for_improvement: List[str]
    recommendations: List[str]
    detected_bias: List[str]
    bias_severity: str  # Low, Medium, High

class BiasDetectionResponse(BaseModel):
    """Response model for bias detection results"""
    bias_indicators: List[str]
    bias_explanations: List[str]
    suggested_revisions: List[str]
    severity: str  # Low, Medium, High, Critical

class InclusionMetricsResponse(BaseModel):
    """Response model for detailed inclusion metrics"""
    gender_inclusivity: float  # 0-100
    racial_inclusivity: float  # 0-100
    age_inclusivity: float  # 0-100
    disability_inclusivity: float  # 0-100
    lgbtq_inclusivity: float  # 0-100
    overall_score: float  # 0-100

class LanguageAnalysisResponse(BaseModel):
    """Response model for language inclusivity analysis"""
    inclusive_language_score: float  # 0-100
    exclusive_terms: List[str]
    suggested_alternatives: Dict[str, str]
    tone_analysis: str

# ============================================================================
# BIAS DETECTION DATABASE
# Collections of bias indicators and inclusive language alternatives
# ============================================================================

# ----------------------------------------------------------------------------
# BIAS INDICATORS
# List of terms and phrases that may indicate bias in job postings
# ----------------------------------------------------------------------------

BIAS_INDICATORS = [
    "require.*experience", "must have.*years", "native speaker", 
    "recent graduate", "digital native", "cultural fit", "rockstar", 
    "ninja", "guru", "master", "competitive", "aggressive"
]

# ----------------------------------------------------------------------------
# INCLUSIVE ALTERNATIVES
# Dictionary mapping biased terms to inclusive alternatives
# ----------------------------------------------------------------------------

INCLUSIVE_ALTERNATIVES = {
    "native speaker": "fluent speaker",
    "recent graduate": "candidate with relevant educational background",
    "digital native": "candidate with digital skills",
    "cultural fit": "values alignment",
    "rockstar": "high performer",
    "ninja": "expert",
    "guru": "specialist",
    "master": "expert",
    "competitive": "results-oriented",
    "aggressive": "assertive"
}

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the diversity insights service
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
    return {"message": "Diversity & Inclusion Insights Service is running"}

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
# JOB POSTING ANALYSIS ENDPOINT
# Endpoint for analyzing job postings for diversity and inclusion metrics
# ----------------------------------------------------------------------------

@app.post("/analyze-job", response_model=DiversityScoreResponse)
async def analyze_job_posting(request: JobAnalysisRequest):
    """
    Analyze a job posting for diversity and inclusion metrics
    
    Args:
        request (JobAnalysisRequest): Request containing job title, company name, and job description
        
    Returns:
        DiversityScoreResponse: Response with diversity scores, strengths, areas for improvement, and recommendations
        
    Example:
        POST /analyze-job
        {
            "job_title": "Software Engineer",
            "company_name": "TechCorp",
            "job_description": "We are looking for a rockstar developer...",
            "company_description": "Innovative tech company committed to diversity"
        }
    """
    # Combine job description and company description for comprehensive analysis
    full_text = f"{request.job_description} {request.company_description or ''}"
    
    # Detect bias indicators using regex patterns
    detected_bias = []
    for indicator in BIAS_INDICATORS:
        if re.search(indicator, full_text, re.IGNORECASE):
            detected_bias.append(indicator)
    
    # Calculate diversity and inclusion scores based on detected bias
    # More bias indicators result in lower scores
    diversity_score = max(0, 100 - len(detected_bias) * 5)
    inclusion_score = max(0, 100 - len(detected_bias) * 3)
    
    # Determine overall rating based on average of diversity and inclusion scores
    avg_score = (diversity_score + inclusion_score) / 2
    if avg_score >= 80:
        overall_rating = "Excellent"
    elif avg_score >= 60:
        overall_rating = "Good"
    elif avg_score >= 40:
        overall_rating = "Fair"
    else:
        overall_rating = "Poor"
    
    # Generate strengths based on positive indicators in the text
    strengths = []
    if "equal opportunity" in full_text.lower():
        strengths.append("Explicit equal opportunity statement")
    if "diversity" in full_text.lower():
        strengths.append("Mentions diversity and inclusion")
    if "accommodation" in full_text.lower():
        strengths.append("Includes accommodation statement")
    
    # Generate areas for improvement based on detected issues
    areas_for_improvement = []
    if not strengths:
        areas_for_improvement.append("Add explicit diversity and inclusion statements")
    if len(detected_bias) > 0:
        areas_for_improvement.append("Remove biased language that may discourage diverse applicants")
    
    # Generate actionable recommendations for improvement
    recommendations = [
        "Include specific diversity and inclusion initiatives",
        "Add information about employee resource groups",
        "Specify flexible work arrangements"
    ]
    
    # Determine bias severity level based on number of detected indicators
    if len(detected_bias) == 0:
        bias_severity = "Low"
    elif len(detected_bias) <= 3:
        bias_severity = "Medium"
    elif len(detected_bias) <= 6:
        bias_severity = "High"
    else:
        bias_severity = "Critical"
    
    # Return the diversity score response with all analysis results
    return DiversityScoreResponse(
        diversity_score=diversity_score,
        inclusion_score=inclusion_score,
        overall_rating=overall_rating,
        strengths=strengths or ["General job posting structure"],
        areas_for_improvement=areas_for_improvement or ["Consider adding more inclusive language"],
        recommendations=recommendations,
        detected_bias=detected_bias,
        bias_severity=bias_severity
    )

# ----------------------------------------------------------------------------
# COMPANY INCLUSIVITY ANALYSIS ENDPOINT
# Endpoint for analyzing company inclusivity across multiple dimensions
# ----------------------------------------------------------------------------

@app.post("/analyze-company", response_model=InclusionMetricsResponse)
async def analyze_company_inclusivity(request: CompanyAnalysisRequest):
    """
    Analyze a company's inclusivity across multiple dimensions
    
    Args:
        request (CompanyAnalysisRequest): Request containing company name and description
        
    Returns:
        InclusionMetricsResponse: Response with detailed inclusion metrics across different dimensions
        
    Example:
        POST /analyze-company
        {
            "company_name": "InclusiveTech",
            "company_description": "We value diversity and inclusion in all aspects of our work",
            "industry": "Technology",
            "employee_count": 500,
            "locations": ["New York", "San Francisco", "London"]
        }
    """
    # This would typically involve more complex analysis in a real implementation
    # For now, we'll generate mock scores with some randomness to demonstrate functionality
    
    # Generate a base score for the company
    base_score = random.randint(60, 90)
    
    # Return detailed inclusion metrics with slight variations for each dimension
    return InclusionMetricsResponse(
        gender_inclusivity=max(0, min(100, base_score + random.randint(-10, 10))),
        racial_inclusivity=max(0, min(100, base_score + random.randint(-15, 15))),
        age_inclusivity=max(0, min(100, base_score + random.randint(-5, 5))),
        disability_inclusivity=max(0, min(100, base_score + random.randint(-10, 10))),
        lgbtq_inclusivity=max(0, min(100, base_score + random.randint(-8, 8))),
        overall_score=max(0, min(100, base_score))
    )

# ----------------------------------------------------------------------------
# BIAS DETECTION ENDPOINT
# Endpoint for detecting bias in text content and suggesting revisions
# ----------------------------------------------------------------------------

@app.post("/detect-bias", response_model=BiasDetectionResponse)
async def detect_bias(request: BiasAnalysisRequest):
    """
    Detect bias in text content and suggest revisions
    
    Args:
        request (BiasAnalysisRequest): Request containing text content to analyze
        
    Returns:
        BiasDetectionResponse: Response with detected bias indicators, explanations, and suggested revisions
        
    Example:
        POST /detect-bias
        {
            "text_content": "We're looking for a rockstar developer who is a digital native..."
        }
    """
    # Initialize lists for storing detection results
    detected_indicators = []
    explanations = []
    suggested_revisions = []
    
    # Check for bias indicators in the provided text content
    for indicator in BIAS_INDICATORS:
        matches = re.findall(indicator, request.text_content, re.IGNORECASE)
        if matches:
            # Add detected indicators to results
            detected_indicators.extend(matches)
            
            # Generate explanations for why these terms may be problematic
            explanations.append(f"The term '{matches[0]}' may discourage diverse candidates by implying specific characteristics")
            
            # Suggest inclusive alternatives for detected biased terms
            for match in matches:
                if match.lower() in INCLUSIVE_ALTERNATIVES:
                    suggested_revisions.append(f"Replace '{match}' with '{INCLUSIVE_ALTERNATIVES[match.lower()]}'")
    
    # Determine severity level based on number of detected bias indicators
    if len(detected_indicators) == 0:
        severity = "Low"
    elif len(detected_indicators) <= 2:
        severity = "Medium"
    elif len(detected_indicators) <= 5:
        severity = "High"
    else:
        severity = "Critical"
    
    # Return the bias detection response with all findings
    return BiasDetectionResponse(
        bias_indicators=detected_indicators or ["No significant bias detected"],
        bias_explanations=explanations or ["The text appears to use inclusive language"],
        suggested_revisions=suggested_revisions or ["Continue using inclusive language practices"],
        severity=severity
    )

# ----------------------------------------------------------------------------
# LANGUAGE INCLUSIVITY ANALYSIS ENDPOINT
# Endpoint for analyzing text for inclusive language usage
# ----------------------------------------------------------------------------

@app.post("/analyze-language", response_model=LanguageAnalysisResponse)
async def analyze_language_inclusivity(request: BiasAnalysisRequest):
    """
    Analyze text for inclusive language usage
    
    Args:
        request (BiasAnalysisRequest): Request containing text content to analyze
        
    Returns:
        LanguageAnalysisResponse: Response with inclusive language score and analysis
        
    Example:
        POST /analyze-language
        {
            "text_content": "We welcome candidates from all backgrounds and experiences..."
        }
    """
    # Initialize lists and dictionaries for storing analysis results
    exclusive_terms = []
    suggested_alternatives = {}
    
    # Check for exclusive terms that could be replaced with inclusive alternatives
    for term, alternative in INCLUSIVE_ALTERNATIVES.items():
        if re.search(term, request.text_content, re.IGNORECASE):
            exclusive_terms.append(term)
            suggested_alternatives[term] = alternative
    
    # Calculate inclusive language score based on number of exclusive terms found
    # Fewer exclusive terms result in higher scores
    inclusive_score = max(0, 100 - len(exclusive_terms) * 10)
    
    # Generate tone analysis based on inclusive language score
    if inclusive_score >= 80:
        tone_analysis = "Highly inclusive language that welcomes diverse candidates"
    elif inclusive_score >= 60:
        tone_analysis = "Generally inclusive with minor improvements possible"
    elif inclusive_score >= 40:
        tone_analysis = "Moderately inclusive but could benefit from revision"
    else:
        tone_analysis = "Limited inclusive language that may deter diverse applicants"
    
    # Return the language analysis response with all findings
    return LanguageAnalysisResponse(
        inclusive_language_score=inclusive_score,
        exclusive_terms=exclusive_terms,
        suggested_alternatives=suggested_alternatives,
        tone_analysis=tone_analysis
    )

# ----------------------------------------------------------------------------
# INDUSTRY BENCHMARKS ENDPOINT
# Endpoint for retrieving diversity and inclusion benchmarks by industry
# ----------------------------------------------------------------------------

@app.get("/industry-benchmarks")
async def get_industry_benchmarks(industry: str = "Technology"):
    """
    Get diversity and inclusion benchmarks for different industries
    
    Args:
        industry (str): Industry to retrieve benchmarks for (default: "Technology")
        
    Returns:
        dict: Industry benchmarks for diversity and inclusion metrics
        
    Example:
        GET /industry-benchmarks?industry=Healthcare
    """
    # Define industry benchmarks for comparison
    benchmarks = {
        "Technology": {
            "diversity_score": 65,
            "inclusion_score": 60,
            "gender_inclusivity": 62,
            "racial_inclusivity": 58
        },
        "Finance": {
            "diversity_score": 60,
            "inclusion_score": 55,
            "gender_inclusivity": 58,
            "racial_inclusivity": 52
        },
        "Healthcare": {
            "diversity_score": 70,
            "inclusion_score": 68,
            "gender_inclusivity": 72,
            "racial_inclusivity": 65
        },
        "Education": {
            "diversity_score": 75,
            "inclusion_score": 72,
            "gender_inclusivity": 78,
            "racial_inclusivity": 70
        }
    }
    
    # Return benchmarks for requested industry or default to Technology
    return benchmarks.get(industry, benchmarks["Technology"])

# ============================================================================
# APPLICATION ENTRY POINT
# Main execution block for running the service
# ============================================================================

if __name__ == "__main__":
    # Import uvicorn for running the ASGI application
    import uvicorn
    
    # Run the FastAPI application with uvicorn
    # Host 0.0.0.0 makes it accessible from outside the container
    # Port 8115 is the designated port for this microservice
    uvicorn.run(app, host="0.0.0.0", port=8115)