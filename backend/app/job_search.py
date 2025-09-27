"""
Job Search Module for MyBrand Job Application Platform
Version: v2
Purpose: Provides job search functionality with Adzuna API integration and local fallback
"""

# Standard library imports
import json
import logging
from typing import List, Optional

# Third-party imports
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
import httpx

# Local imports
from .config import get_adzuna_config
from .cache import cache_result

# Set up logging for this module
# This allows us to track errors and debug information
logger = logging.getLogger(__name__)

# Create a router for job search endpoints
# All endpoints in this module will have the prefix "/jobs"
# Tags help organize the API documentation
router = APIRouter(prefix="/jobs", tags=["Job Search"])


# ============================================================================
# DATA MODELS
# These Pydantic models define the structure of our job data and API requests/responses
# ============================================================================

class Job(BaseModel):
    """
    Represents a job posting with all relevant information.
    
    This model defines the structure of job data returned by our API.
    Each field represents a specific attribute of a job posting.
    """
    # Unique identifier for the job
    id: int
    
    # Job title and company information
    title: str
    company: str
    
    # Location information
    location: str
    
    # Salary range (optional)
    salary: Optional[str] = None
    
    # Employment type (e.g., Full-time, Part-time, Contract)
    type: str
    
    # Whether the job offers remote work options
    remote: bool
    
    # Whether the job is marked as urgent
    urgent: bool
    
    # Detailed job description
    description: str
    
    # Job requirements and benefits (optional lists)
    requirements: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    
    # When the job was posted
    posted: str
    
    # Whether this is a new job posting
    isNew: bool

class JobSearchRequest(BaseModel):
    """
    Represents a job search request with optional filtering parameters.
    
    This model defines the structure of search requests to our API.
    It includes validation methods to sanitize user inputs.
    """
    # Search keyword (e.g., job title, skills, etc.)
    keyword: Optional[str] = None
    
    # Location filter
    location: Optional[str] = None
    
    # Job type filter (e.g., Full-time, Part-time)
    jobType: Optional[str] = None
    
    # Company filter
    company: Optional[str] = None
    
    # Remote work filter
    remote: Optional[bool] = None
    
    # Pagination parameters
    limit: Optional[int] = 20  # Number of results per page
    offset: Optional[int] = 0  # Number of results to skip
    
    # ============================================================================
    # INPUT VALIDATION METHODS
    # These methods sanitize user inputs to prevent security issues
    # ============================================================================
    
    @validator('keyword')
    def validate_keyword(cls, v):
        """
        Validate and sanitize the keyword parameter.
        
        Strips whitespace and limits length to 100 characters to prevent
        potential injection attacks and ensure reasonable search terms.
        
        Args:
            v (str): The keyword value to validate
            
        Returns:
            str: The sanitized keyword value
        """
        if v is not None:
            # Remove leading/trailing whitespace and limit to 100 characters
            v = v.strip()[:100]
        return v
    
    @validator('location')
    def validate_location(cls, v):
        """
        Validate and sanitize the location parameter.
        
        Strips whitespace and limits length to 100 characters to ensure
        reasonable location search terms.
        
        Args:
            v (str): The location value to validate
            
        Returns:
            str: The sanitized location value
        """
        if v is not None:
            # Remove leading/trailing whitespace and limit to 100 characters
            v = v.strip()[:100]
        return v
    
    @validator('company')
    def validate_company(cls, v):
        """
        Validate and sanitize the company parameter.
        
        Strips whitespace and limits length to 100 characters to ensure
        reasonable company search terms.
        
        Args:
            v (str): The company value to validate
            
        Returns:
            str: The sanitized company value
        """
        if v is not None:
            # Remove leading/trailing whitespace and limit to 100 characters
            v = v.strip()[:100]
        return v
    
    @validator('limit')
    def validate_limit(cls, v):
        """
        Validate the limit parameter.
        
        Ensures the limit is between 1 and 100 to prevent excessive
        resource consumption from large result sets.
        
        Args:
            v (int): The limit value to validate
            
        Returns:
            int: The validated limit value (between 1 and 100)
        """
        if v is not None:
            # Ensure limit is between 1 and 100
            if v < 1:
                return 1
            if v > 100:
                return 100
        return v
    
    @validator('offset')
    def validate_offset(cls, v):
        """
        Validate the offset parameter.
        
        Ensures the offset is not negative to prevent invalid pagination.
        
        Args:
            v (int): The offset value to validate
            
        Returns:
            int: The validated offset value (not negative)
        """
        if v is not None:
            # Ensure offset is not negative
            if v < 0:
                return 0
        return v

class JobSearchResponse(BaseModel):
    """
    Represents the response to a job search request.
    
    This model defines the structure of search results returned by our API.
    It includes pagination information to support client-side pagination.
    """
    # List of jobs matching the search criteria
    jobs: List[Job]
    
    # Total number of jobs matching the search criteria
    total: int
    
    # Whether there are more results available beyond the current page
    hasMore: bool

# ============================================================================
# SAMPLE JOB DATA
# This data is used when the Adzuna API is not available or fails
# It provides a basic set of job postings for demonstration purposes
# ============================================================================

sample_jobs = [
    Job(
        id=1,
        title="Senior Software Engineer",
        company="TechCorp Inc.",
        location="San Francisco, CA",
        salary="$120k - $160k",
        type="Full-time",
        remote=True,
        urgent=False,
        description="Join our team to build scalable web applications using React, Node.js, and cloud technologies. You will work on exciting projects that impact millions of users.",
        requirements=[
            "5+ years of software development experience",
            "Proficiency in React and Node.js",
            "Experience with cloud platforms",
            "Strong problem-solving skills"
        ],
        benefits=[
            "Health insurance",
            "Stock options",
            "Remote work",
            "Unlimited PTO"
        ],
        posted="2 days ago",
        isNew=True
    ),
    Job(
        id=2,
        title="Data Scientist",
        company="DataFlow Analytics",
        location="Remote",
        salary="$110k - $140k",
        type="Full-time",
        remote=True,
        urgent=True,
        description="Work with machine learning models and big data to derive actionable insights for our clients. You will be responsible for building predictive models and data pipelines.",
        requirements=[
            "PhD or Masters in Data Science/Statistics",
            "Experience with Python and R",
            "Machine learning expertise",
            "SQL proficiency"
        ],
        benefits=[
            "Flexible hours",
            "Learning budget",
            "Health benefits",
            "Work from anywhere"
        ],
        posted="1 day ago",
        isNew=True
    ),
    Job(
        id=3,
        title="UX Designer",
        company="Design Studio",
        location="New York, NY",
        salary="$80k - $110k",
        type="Full-time",
        remote=False,
        urgent=False,
        description="Create beautiful and intuitive user experiences for our digital products. You will work closely with product managers and developers to bring designs to life.",
        requirements=[
            "3+ years of UX design experience",
            "Proficiency in Figma and Sketch",
            "User research skills",
            "Portfolio of design work"
        ],
        benefits=[
            "Creative environment",
            "Design tools budget",
            "Health insurance",
            "Professional development"
        ],
        posted="3 days ago",
        isNew=True
    )
]


# ============================================================================
# LOCAL SEARCH FUNCTIONALITY
# These functions provide job search capabilities using local sample data
# ============================================================================

@cache_result(expiration=300, key_prefix="job_search")
def search_jobs_locally(request: JobSearchRequest) -> JobSearchResponse:
    """
    Search jobs from local sample data.
    
    This function filters the sample job data based on the search criteria
    provided in the JobSearchRequest object. It supports filtering by
    keyword, location, job type, company, and remote status, along with
    pagination support.
    
    Args:
        request (JobSearchRequest): The search criteria including filters
            and pagination parameters
            
    Returns:
        JobSearchResponse: The filtered job results with pagination info
        
    Example:
        >>> request = JobSearchRequest(keyword="software", limit=10)
        >>> result = search_jobs_locally(request)
        >>> print(f"Found {result.total} jobs")
    """
    # Start with a copy of all sample jobs
    filtered_jobs = sample_jobs.copy()
    
    # ============================================================================
    # APPLY FILTERS
    # Each filter narrows down the job results based on search criteria
    # ============================================================================
    
    # Filter by keyword if provided
    # Search in title, company, and description fields for better matching
    if request.keyword:
        keyword = request.keyword.lower()
        filtered_jobs = [
            job for job in filtered_jobs
            if (keyword in job.title.lower() or 
                keyword in job.company.lower() or 
                keyword in job.description.lower())
        ]
    
    # Filter by location if provided
    if request.location:
        location = request.location.lower()
        filtered_jobs = [
            job for job in filtered_jobs
            if location in job.location.lower()
        ]
    
    # Filter by job type if provided
    if request.jobType:
        filtered_jobs = [
            job for job in filtered_jobs
            if job.type.lower() == request.jobType.lower()
        ]
    
    # Filter by company if provided
    if request.company:
        company = request.company.lower()
        filtered_jobs = [
            job for job in filtered_jobs
            if company in job.company.lower()
        ]
    
    # Filter by remote status if provided
    if request.remote is not None:
        filtered_jobs = [
            job for job in filtered_jobs
            if job.remote == request.remote
        ]
    
    # ============================================================================
    # PAGINATION HANDLING
    # Apply pagination to limit results and provide page navigation
    # ============================================================================
    
    # Calculate total number of matching jobs
    total = len(filtered_jobs)
    
    # Handle pagination parameters
    # Use provided values or defaults
    offset = request.offset or 0
    limit = request.limit or 20
    
    # Determine if there are more results beyond the current page
    hasMore = offset + limit < total
    
    # Apply pagination to get the current page of results
    paginated_jobs = filtered_jobs[offset:offset + limit]
    
    # Return the search results with pagination information
    return JobSearchResponse(
        jobs=paginated_jobs,
        total=total,
        hasMore=hasMore
    )

# ============================================================================
# ADZUNA API INTEGRATION
# These functions provide job search capabilities using the Adzuna job API
# ============================================================================

@cache_result(expiration=600, key_prefix="adzuna_search")
async def search_jobs_adzuna(request: JobSearchRequest) -> JobSearchResponse:
    """
    Search jobs using Adzuna API.
    
    This function queries the Adzuna job search API and formats the results
    to match our internal Job model. It includes error handling and fallback
    to local search when the API is unavailable.
    
    Args:
        request (JobSearchRequest): The search criteria including filters
            and pagination parameters
            
    Returns:
        JobSearchResponse: The job search results from Adzuna API or
            local fallback if API fails
            
    Raises:
        httpx.TimeoutException: If the API request times out
        httpx.RequestError: If there's an error making the API request
        Exception: For any other unexpected errors
        
    Example:
        >>> request = JobSearchRequest(keyword="developer", location="NYC")
        >>> result = await search_jobs_adzuna(request)
        >>> print(f"Found {result.total} jobs via Adzuna")
    """
    # ============================================================================
    # API CREDENTIALS RETRIEVAL
    # Get API credentials from configuration
    # ============================================================================
    
    # Get API credentials from configuration
    # These are required to access the Adzuna API
    adzuna_config = get_adzuna_config()
    app_id = adzuna_config.get("app_id")
    app_key = adzuna_config.get("app_key")
    
    # Return local search if API credentials are not configured
    # This provides a fallback when the Adzuna API is not available
    if not app_id or not app_key:
        logger.info("Adzuna API credentials not configured, using local search")
        return search_jobs_locally(request)
    
    # ============================================================================
    # API REQUEST CONSTRUCTION
    # Build Adzuna API URL with search parameters
    # ============================================================================
    
    # Build Adzuna API URL with search parameters
    base_url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": request.limit or 20,
        "what": request.keyword,
        "where": request.location,
        "company": request.company,
        "content-type": "application/json"
    }
    
    # Remove None values from parameters to avoid sending empty values
    params = {k: v for k, v in params.items() if v is not None}
    
    # ============================================================================
    # API REQUEST EXECUTION AND ERROR HANDLING
    # Make the API request with proper error handling and fallback
    # ============================================================================
    
    try:
        # Make the API request with a 10-second timeout
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url, params=params, timeout=10.0)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            
            # ============================================================================
            # RESPONSE DATA TRANSFORMATION
            # Convert Adzuna job data to our Job model
            # ============================================================================
            
            # Convert Adzuna job data to our Job model
            jobs = []
            for i, adzuna_job in enumerate(data.get("results", [])):
                # Map Adzuna fields to our Job model
                # Generate a simple ID since Adzuna doesn't provide one
                job = Job(
                    id=i + 1,
                    title=adzuna_job.get("title", "Untitled"),
                    company=adzuna_job.get("company", {}).get("display_name", "Unknown Company"),
                    location=adzuna_job.get("location", {}).get("display_name", "Unknown Location"),
                    # Format salary information if available
                    salary=adzuna_job.get("salary_min") and adzuna_job.get("salary_max") and 
                           f"${int(adzuna_job['salary_min'])} - ${int(adzuna_job['salary_max'])}" or None,
                    type=adzuna_job.get("contract_time", "Full-time"),
                    # Determine if the job offers remote work
                    remote="remote" in adzuna_job.get("title", "").lower() or 
                           "remote" in adzuna_job.get("description", "").lower(),
                    # Determine if the job is urgent
                    urgent=adzuna_job.get("urgency", "") == "immediate",
                    description=adzuna_job.get("description", "No description provided"),
                    # Adzuna doesn't provide structured requirements/benefits
                    requirements=None,
                    benefits=None,
                    # Use the job creation date or a default value
                    posted=adzuna_job.get("created", "Unknown date"),
                    # Use the 'top' field as an indicator for new jobs
                    isNew=adzuna_job.get("top", False)
                )
                jobs.append(job)
            
            # Return the formatted search results
            return JobSearchResponse(
                jobs=jobs,
                total=data.get("count", 0),
                hasMore=data.get("count", 0) > (request.offset or 0) + len(jobs)
            )
    except httpx.TimeoutException:
        # Handle timeout errors by falling back to local search
        logger.warning("Adzuna API timeout")
        return search_jobs_locally(request)
    except httpx.RequestError as e:
        # Handle request errors by falling back to local search
        logger.error(f"Adzuna API request error: {e}")
        return search_jobs_locally(request)
    except Exception as e:
        # Handle any other unexpected errors by falling back to local search
        logger.error(f"Adzuna API error: {e}")
        return search_jobs_locally(request)


# ============================================================================
# SEARCH INTERFACE FUNCTIONS
# These functions provide different ways to access job search functionality
# ============================================================================

def search_jobs(request: JobSearchRequest) -> JobSearchResponse:
    """
    Search jobs (synchronous wrapper for async function).
    
    This function provides a synchronous interface for job searching.
    In a production environment, you might want to use the async version
    for better performance with I/O-bound operations.
    
    Args:
        request (JobSearchRequest): The search criteria including filters
            and pagination parameters
            
    Returns:
        JobSearchResponse: The job search results from either Adzuna API
            or local fallback
    """
    # For now, we'll use the local search as the main function
    # In a production environment, you might want to use the async version
    return search_jobs_locally(request)


# ============================================================================
# API ENDPOINTS
# These functions define the HTTP endpoints for job search functionality
# ============================================================================

@router.get("/search", response_model=JobSearchResponse)
async def get_jobs(
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    jobType: Optional[str] = None,
    company: Optional[str] = None,
    remote: Optional[bool] = None,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0
):
    """
    Search for jobs with optional filters.
    
    This is the main API endpoint for job searching. It accepts various
    query parameters to filter job results and supports pagination.
    
    Query Parameters:
        keyword (str, optional): Search keyword to match in job titles,
            companies, or descriptions
        location (str, optional): Location filter to match job locations
        jobType (str, optional): Job type filter (e.g., "Full-time", "Part-time")
        company (str, optional): Company filter to match specific companies
        remote (bool, optional): Remote work filter (True for remote jobs only)
        limit (int, optional): Number of results per page (default: 20, max: 100)
        offset (int, optional): Number of results to skip for pagination (default: 0)
        
    Returns:
        JobSearchResponse: The job search results with pagination information
        
    Raises:
        HTTPException: If there's an error processing the request
        
    Example:
        GET /jobs/search?keyword=developer&location=NYC&limit=10&offset=0
    """
    # ============================================================================
    # REQUEST PROCESSING
    # Create a JobSearchRequest object from the query parameters
    # ============================================================================
    
    # Create a JobSearchRequest object from the query parameters
    request = JobSearchRequest(
        keyword=keyword,
        location=location,
        jobType=jobType,
        company=company,
        remote=remote,
        limit=limit,
        offset=offset
    )
    
    # ============================================================================
    # SEARCH EXECUTION WITH ERROR HANDLING
    # Try to use Adzuna API, fall back to local search if it fails
    # ============================================================================
    
    # Try to use Adzuna API, fall back to local search if it fails
    try:
        return await search_jobs_adzuna(request)
    except Exception as e:
        # Log the error and fall back to local search
        logger.error(f"Error using Adzuna API, falling back to local search: {e}")
        return search_jobs_locally(request)