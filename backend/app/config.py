"""
Configuration Management Module for MyBrand Job Application Platform
Version: v2
Purpose: Centralized configuration management with environment variable loading and validation
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for configuration management
# ============================================================================

from pydantic_settings import BaseSettings
from pydantic import Field, validator
import os
from typing import Optional

# ============================================================================
# CONFIGURATION CLASSES
# Pydantic models for application configuration with validation
# ============================================================================

class DatabaseSettings(BaseSettings):
    """Database configuration settings with validation."""
    url: Optional[str] = Field(None, env="DATABASE_URL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class SupabaseSettings(BaseSettings):
    """Supabase configuration settings with validation."""
    url: str = Field(..., env="SUPABASE_URL")
    anon_key: str = Field(..., env="SUPABASE_ANON_KEY")
    service_role_key: str = Field(..., env="SUPABASE_SERVICE_ROLE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class StripeSettings(BaseSettings):
    """Stripe configuration settings with validation."""
    secret_key: str = Field(..., env="STRIPE_SECRET_KEY")
    webhook_secret: str = Field(..., env="STRIPE_WEBHOOK_SECRET")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class OpenAISettings(BaseSettings):
    """OpenAI configuration settings with validation."""
    api_key: str = Field(..., env="OPENAI_API_KEY")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class RedisSettings(BaseSettings):
    """Redis configuration settings with validation."""
    url: str = Field(..., env="REDIS_URL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class AdzunaSettings(BaseSettings):
    """Adzuna API configuration settings with validation."""
    app_id: str = Field(..., env="ADZUNA_APP_ID")
    app_key: str = Field(..., env="ADZUNA_APP_KEY")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class ApplicationSettings(BaseSettings):
    """Main application configuration settings with validation."""
    app_url: str = Field("http://localhost:5173", env="APP_URL")
    api_url: str = Field("http://localhost:8000", env="API_URL")
    jwt_secret: str = Field(..., env="JWT_SECRET")
    
    # Service URLs for microservices
    skill_gap_service_url: str = Field("http://localhost:8105", env="SKILL_GAP_SERVICE_URL")
    resume_builder_service_url: str = Field("http://localhost:8106", env="RESUME_BUILDER_SERVICE_URL")
    resume_enhancer_service_url: str = Field("http://localhost:8107", env="RESUME_ENHANCER_SERVICE_URL")
    interview_coach_service_url: str = Field("http://localhost:8108", env="INTERVIEW_COACH_SERVICE_URL")
    application_filler_service_url: str = Field("http://localhost:8109", env="APPLICATION_FILLER_SERVICE_URL")
    semantic_matcher_service_url: str = Field("http://localhost:8110", env="SEMANTIC_MATCHER_SERVICE_URL")
    job_recommender_service_url: str = Field("http://localhost:8111", env="JOB_RECOMMENDER_SERVICE_URL")
    mock_interviewer_service_url: str = Field("http://localhost:8114", env="MOCK_INTERVIEWER_SERVICE_URL")
    diversity_insights_service_url: str = Field("http://localhost:8115", env="DIVERSITY_INSIGHTS_SERVICE_URL")
    document_summarizer_service_url: str = Field("http://localhost:8116", env="DOCUMENT_SUMMARIZER_SERVICE_URL")
    voice_agent_service_url: str = Field("http://localhost:8117", env="VOICE_AGENT_SERVICE_URL")
    multi_language_service_url: str = Field("http://localhost:8118", env="MULTI_LANGUAGE_SERVICE_URL")
    course_recommender_service_url: str = Field("http://localhost:8119", env="COURSE_RECOMMENDER_SERVICE_URL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# ============================================================================
# CONFIGURATION INSTANCES
# Singleton instances of configuration classes for application use
# ============================================================================

# Load database settings
database_settings = DatabaseSettings()

# Load Supabase settings
supabase_settings = SupabaseSettings()

# Load Stripe settings
stripe_settings = StripeSettings()

# Load OpenAI settings
openai_settings = OpenAISettings()

# Load Redis settings
redis_settings = RedisSettings()

# Load Adzuna settings
adzuna_settings = AdzunaSettings()

# Load application settings
app_settings = ApplicationSettings()

# ============================================================================
# CONFIGURATION ACCESS FUNCTIONS
# Functions for safely accessing configuration values
# ============================================================================

def get_database_url() -> Optional[str]:
    """Get the database URL from configuration."""
    return database_settings.url

def get_supabase_config() -> dict:
    """Get Supabase configuration as a dictionary."""
    return {
        "url": supabase_settings.url,
        "anon_key": supabase_settings.anon_key,
        "service_role_key": supabase_settings.service_role_key
    }

def get_stripe_config() -> dict:
    """Get Stripe configuration as a dictionary."""
    return {
        "secret_key": stripe_settings.secret_key,
        "webhook_secret": stripe_settings.webhook_secret
    }

def get_openai_config() -> dict:
    """Get OpenAI configuration as a dictionary."""
    return {
        "api_key": openai_settings.api_key
    }

def get_redis_config() -> dict:
    """Get Redis configuration as a dictionary."""
    return {
        "url": redis_settings.url
    }

def get_adzuna_config() -> dict:
    """Get Adzuna API configuration as a dictionary."""
    return {
        "app_id": adzuna_settings.app_id,
        "app_key": adzuna_settings.app_key
    }

def get_app_config() -> dict:
    """Get application configuration as a dictionary."""
    return {
        "app_url": app_settings.app_url,
        "api_url": app_settings.api_url,
        "jwt_secret": app_settings.jwt_secret,
        "service_urls": {
            "skill_gap": app_settings.skill_gap_service_url,
            "resume_builder": app_settings.resume_builder_service_url,
            "resume_enhancer": app_settings.resume_enhancer_service_url,
            "interview_coach": app_settings.interview_coach_service_url,
            "application_filler": app_settings.application_filler_service_url,
            "semantic_matcher": app_settings.semantic_matcher_service_url,
            "job_recommender": app_settings.job_recommender_service_url,
            "mock_interviewer": app_settings.mock_interviewer_service_url,
            "diversity_insights": app_settings.diversity_insights_service_url,
            "document_summarizer": app_settings.document_summarizer_service_url,
            "voice_agent": app_settings.voice_agent_service_url,
            "multi_language": app_settings.multi_language_service_url,
            "course_recommender": app_settings.course_recommender_service_url
        }
    }