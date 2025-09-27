"""
Multi-Language Service for MyBrand Job Application Platform
Version: v2
Purpose: Provides AI-powered language translation, localization, and cultural adaptation capabilities
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for multi-language functionality
# ============================================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os

# ============================================================================
# ROUTER CONFIGURATION
# Create router for multi-language endpoints with appropriate prefix and tags
# ============================================================================

router = APIRouter(prefix="/multi-language", tags=["Multi-Language"])

# ============================================================================
# SERVICE CONFIGURATION
# Get the service URL from environment variables for microservice communication
# ============================================================================

# Get the multi-language service URL from environment variables
# In development, this would be http://localhost:8118
# In production, this would be the deployed service URL
MULTI_LANGUAGE_SERVICE_URL = os.getenv("MULTI_LANGUAGE_SERVICE_URL", "http://multi_language:8118")

# ============================================================================
# DATA MODELS
# Pydantic models for multi-language data structures and API requests
# ============================================================================

class TranslationRequest(BaseModel):
    """
    Request model for text translation.
    
    Contains text to translate along with source and target language specifications.
    """
    text: str
    source_language: str = "en"
    target_language: str

class LocalizationRequest(BaseModel):
    """
    Request model for content localization.
    
    Contains content to localize along with target locale and content type for context.
    """
    content: str
    target_locale: str
    content_type: str

class LanguageDetectionRequest(BaseModel):
    """
    Request model for language detection.
    
    Contains text for which to detect the language.
    """
    text: str

class CulturalAdaptationRequest(BaseModel):
    """
    Request model for cultural content adaptation.
    
    Contains content to adapt along with target culture and content type for context.
    """
    content: str
    target_culture: str
    content_type: str

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for multi-language functionality
# ============================================================================

@router.post("/translate")
async def translate_text(request: TranslationRequest):
    """
    Translate text from source language to target language.
    
    This endpoint forwards the translation request to a dedicated
    microservice that provides high-quality AI-powered translation
    between supported languages while preserving context and meaning.
    
    Args:
        request (TranslationRequest): Contains text and language specifications
        
    Returns:
        dict: Translated text with quality metrics and metadata
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = TranslationRequest(
        ...     text="Welcome to our job platform",
        ...     source_language="en",
        ...     target_language="es"
        ... )
        >>> translation = await translate_text(request)
        >>> print(f"Translation: {translation['translated_text']}")
    """
    # Forward the request to the multi-language microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{MULTI_LANGUAGE_SERVICE_URL}/translate",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Multi-language service unavailable: {str(e)}"
            )

@router.post("/localize")
async def localize_content(request: LocalizationRequest):
    """
    Localize content for a specific locale.
    
    This endpoint forwards the localization request to a dedicated
    microservice that adapts content for specific locales, including
    regional formatting, cultural references, and local conventions.
    
    Args:
        request (LocalizationRequest): Contains content and locale specifications
        
    Returns:
        dict: Localized content with adaptation details
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = LocalizationRequest(
        ...     content="The meeting is at 2:00 PM",
        ...     target_locale="en-GB",
        ...     content_type="notification"
        ... )
        >>> localization = await localize_content(request)
        >>> print(f"Localized content: {localization['localized_content']}")
    """
    # Forward the request to the multi-language microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{MULTI_LANGUAGE_SERVICE_URL}/localize",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Multi-language service unavailable: {str(e)}"
            )

@router.post("/detect-language")
async def detect_language(request: LanguageDetectionRequest):
    """
    Detect the language of provided text.
    
    This endpoint forwards the language detection request to a dedicated
    microservice that identifies the language of input text with high accuracy.
    
    Args:
        request (LanguageDetectionRequest): Contains text for language detection
        
    Returns:
        dict: Detected language with confidence score and alternatives
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = LanguageDetectionRequest(
        ...     text="Bonjour, comment allez-vous?"
        ... )
        >>> detection = await detect_language(request)
        >>> print(f"Detected language: {detection['language']}")
    """
    # Forward the request to the multi-language microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{MULTI_LANGUAGE_SERVICE_URL}/detect-language",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Multi-language service unavailable: {str(e)}"
            )

@router.post("/cultural-adaptation")
async def cultural_adaptation(request: CulturalAdaptationRequest):
    """
    Adapt content for specific cultural contexts.
    
    This endpoint forwards the cultural adaptation request to a dedicated
    microservice that modifies content to be appropriate and effective
    for specific cultural contexts and audiences.
    
    Args:
        request (CulturalAdaptationRequest): Contains content and cultural specifications
        
    Returns:
        dict: Culturally adapted content with explanation of changes
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> request = CulturalAdaptationRequest(
        ...     content="We're looking for the best candidate",
        ...     target_culture="Japan",
        ...     content_type="job_description"
        ... )
        >>> adaptation = await cultural_adaptation(request)
        >>> print(f"Adapted content: {adaptation['adapted_content']}")
    """
    # Forward the request to the multi-language microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{MULTI_LANGUAGE_SERVICE_URL}/cultural-adaptation",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Multi-language service unavailable: {str(e)}"
            )

@router.get("/supported-languages")
async def get_supported_languages():
    """
    Get a list of supported languages.
    
    This endpoint retrieves the current list of supported languages
    from the multi-language microservice for user guidance and selection.
    
    Returns:
        dict: Supported languages organized by language code and name
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> languages = await get_supported_languages()
        >>> print(f"Supported languages: {len(languages['languages'])}")
    """
    # Forward the request to the multi-language microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{MULTI_LANGUAGE_SERVICE_URL}/supported-languages",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Multi-language service unavailable: {str(e)}"
            )

@router.get("/language-pair-support")
async def check_language_pair_support(source: str, target: str):
    """
    Check if a specific language pair is supported.
    
    This endpoint verifies whether translation between a specific
    source and target language pair is supported by the system.
    
    Args:
        source (str): Source language code (e.g., "en" for English)
        target (str): Target language code (e.g., "es" for Spanish)
        
    Returns:
        dict: Support status for the language pair with quality information
        
    Raises:
        HTTPException: If the microservice is unavailable or returns an error
        
    Example:
        >>> support = await check_language_pair_support("en", "fr")
        >>> print(f"Support status: {support['supported']}")
    """
    # Forward the request to the multi-language microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{MULTI_LANGUAGE_SERVICE_URL}/language-pair-support",
                params={"source": source, "target": target},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Multi-language service unavailable: {str(e)}"
            )