"""
Main application file for MyBrand Job Application Platform API
Version: v2
Purpose: Entry point for the FastAPI application with all router integrations
"""

# Standard library imports
import datetime

# Third-party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Local imports
from .config import app_settings
from .logging_config import setup_logging, StructuredLogger
from .security import add_security_headers
from .cache import initialize_cache, shutdown_cache

# Import all microservice routers
# Each router represents a distinct AI-powered service in the platform
from .job_search import router as job_search_router
from .skill_gap import router as skill_gap_router
from .resume_builder import router as resume_builder_router
from .resume_enhancer import router as resume_enhancer_router
from .interview_coach import router as interview_coach_router
from .job_matcher import router as job_matcher_router
from .document_summarizer import router as document_summarizer_router
from .course_recommender import router as course_recommender_router
from .job_recommender import router as job_recommender_router
from .application_filler import router as application_filler_router
from .mock_interviewer import router as mock_interviewer_router
from .diversity_insights import router as diversity_insights_router
from .multi_language import router as multi_language_router
from .voice_agent import router as voice_agent_router
from .notifications import router as notifications_router

# Set up logging
setup_logging()

# Create a structured logger for this module
logger = StructuredLogger(__name__)

# Initialize the FastAPI application with comprehensive metadata for documentation
app = FastAPI(
    title="MyBrand Job Application Platform API",
    description="""
MyBrand Job Application Platform API provides comprehensive job search and career development services.

## Features

* **Job Search**: Search for jobs with advanced filtering and Adzuna API integration
* **AI Career Tools**: Skill gap analysis, resume building, interview preparation, and job matching
* **Real-time Notifications**: WebSocket-based real-time notifications and messaging
* **Document Processing**: Resume parsing, summarization, and analysis

## Microservices

The API integrates with multiple AI-powered microservices:

* Skill Gap Analyzer
* Resume Builder & Enhancer
* Interview Coach
* Job Matcher & Recommender
* Document Summarizer
* And many more...

## Authentication

Most endpoints require authentication via JWT tokens. See the authentication service for details.
""",
    version="2.0.0",
    contact={
        "name": "MyBrand API Support",
        "email": "support@mybrand.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This controls which origins can access our API for security purposes
app.add_middleware(
    CORSMiddleware,
    # Allow requests only from the specified application URL
    allow_origins=[app_settings.app_url],
    # Allow credentials to be included in cross-origin requests
    allow_credentials=True,
    # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_methods=["*"],
    # Allow all headers in cross-origin requests
    allow_headers=["*"],
)

# Register all microservice routers with the main application
# Each router handles a specific domain of functionality
app.include_router(job_search_router)
app.include_router(skill_gap_router)
app.include_router(resume_builder_router)
app.include_router(resume_enhancer_router)
app.include_router(interview_coach_router)
app.include_router(job_matcher_router)
app.include_router(document_summarizer_router)
app.include_router(course_recommender_router)
app.include_router(job_recommender_router)
app.include_router(application_filler_router)
app.include_router(mock_interviewer_router)
app.include_router(diversity_insights_router)
app.include_router(multi_language_router)
app.include_router(voice_agent_router)
app.include_router(notifications_router)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers_middleware(request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    
    # Add security headers to the response
    response.headers.update(add_security_headers({}))
    
    return response

# Initialize cache on startup
@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup."""
    logger.info("Starting up application")
    
    # Initialize cache
    if initialize_cache():
        logger.info("Cache initialized successfully")
    else:
        logger.warning("Failed to initialize cache")

# Clean up on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up services on application shutdown."""
    logger.info("Shutting down application")
    
    # Shutdown cache
    shutdown_cache()
    logger.info("Cache shutdown completed")

# Main execution block
# This runs the application when the file is executed directly
if __name__ == "__main__":
    # Import uvicorn for running the ASGI application
    import uvicorn
    
    # Run the FastAPI application with uvicorn
    # Host 0.0.0.0 makes it accessible from outside the container
    # Port 8000 is the standard port for this application
    uvicorn.run(app, host="0.0.0.0", port=8000)