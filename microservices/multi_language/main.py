"""
Multi-Language Support Service
Version: 1.0
Purpose: AI service for translating and localizing job search content for global users

This microservice provides functionality to:
1. Translate text between multiple languages
2. Localize content for specific locales and cultural contexts
3. Detect languages of provided text
4. Adapt content for cultural norms and expectations
5. Provide information about supported languages and locales
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
    title="Multi-Language Support",
    description="AI service for translating and localizing job search content for global users",
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

class TranslationRequest(BaseModel):
    """Request model for text translation"""
    text: str
    source_language: str = "en"
    target_language: str

class LocalizationRequest(BaseModel):
    """Request model for content localization"""
    content: str
    target_locale: str  # e.g., "es-ES", "fr-CA", "zh-CN"
    content_type: str  # resume, job_description, cover_letter, etc.

class LanguageDetectionRequest(BaseModel):
    """Request model for language detection"""
    text: str

class CulturalAdaptationRequest(BaseModel):
    """Request model for cultural content adaptation"""
    content: str
    target_culture: str  # e.g., "German", "Japanese", "Brazilian"
    content_type: str

# ----------------------------------------------------------------------------
# RESPONSE MODELS
# Models for API response data
# ----------------------------------------------------------------------------

class TranslationResponse(BaseModel):
    """Response model for text translation results"""
    translated_text: str
    source_language: str
    target_language: str
    confidence: float  # 0-100

class LocalizationResponse(BaseModel):
    """Response model for content localization results"""
    localized_content: str
    locale: str
    adaptations_made: List[str]
    cultural_notes: List[str]

class LanguageDetectionResponse(BaseModel):
    """Response model for language detection results"""
    detected_language: str
    confidence: float  # 0-100
    alternative_languages: List[str]

class CulturalAdaptationResponse(BaseModel):
    """Response model for cultural adaptation results"""
    adapted_content: str
    culture: str
    adaptations_made: List[str]
    explanation: str

# ============================================================================
# LANGUAGE SUPPORT DATABASE
# Collections of supported languages, locales, and cultural contexts
# ============================================================================

# ----------------------------------------------------------------------------
# SUPPORTED LANGUAGES
# List of languages supported by the service
# ----------------------------------------------------------------------------

SUPPORTED_LANGUAGES = [
    "en", "es", "fr", "de", "zh", "ja", "pt", "ru", "ar", "hi"
]

# ----------------------------------------------------------------------------
# SUPPORTED LOCALES
# List of specific locales supported by the service
# ----------------------------------------------------------------------------

SUPPORTED_LOCALES = [
    "en-US", "en-GB", "es-ES", "es-MX", "fr-FR", "fr-CA", "de-DE", 
    "zh-CN", "zh-TW", "ja-JP", "pt-BR", "pt-PT", "ru-RU", "ar-SA", "hi-IN"
]

# ----------------------------------------------------------------------------
# CULTURAL CONTEXTS
# List of cultural contexts supported by the service
# ----------------------------------------------------------------------------

CULTURAL_CONTEXTS = [
    "American", "British", "Spanish", "Mexican", "French", "Canadian", 
    "German", "Chinese", "Japanese", "Brazilian", "Russian", "Arabic", "Indian"
]

# ----------------------------------------------------------------------------
# TRANSLATION DATABASE
# Mock database of translations for demonstration purposes
# ----------------------------------------------------------------------------

TRANSLATION_DB = {
    "en": {
        "es": {
            "Software Engineer": "Ingeniero de Software",
            "experience": "experiencia",
            "skills": "habilidades",
            "education": "educación"
        },
        "fr": {
            "Software Engineer": "Ingénieur Logiciel",
            "experience": "expérience",
            "skills": "compétences",
            "education": "éducation"
        },
        "de": {
            "Software Engineer": "Softwareingenieur",
            "experience": "Erfahrung",
            "skills": "Fähigkeiten",
            "education": "Bildung"
        }
    }
}

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the multi-language support service
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
    return {"message": "Multi-Language Support Service is running"}

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
# TEXT TRANSLATION ENDPOINT
# Endpoint for translating text between languages
# ----------------------------------------------------------------------------

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Translate text from source language to target language
    
    Args:
        request (TranslationRequest): Request containing text and language codes
        
    Returns:
        TranslationResponse: Translated text with metadata
        
    Example:
        POST /translate
        {
            "text": "Software Engineer with 5 years experience",
            "source_language": "en",
            "target_language": "es"
        }
    """
    # In a real implementation, this would use a translation service like Google Translate or AWS Translate
    # For this mock, we'll use our translation database or generate mock translations
    
    # Check if we have a direct translation in our database
    if request.source_language in TRANSLATION_DB and request.target_language in TRANSLATION_DB[request.source_language]:
        translation_dict = TRANSLATION_DB[request.source_language][request.target_language]
        # Simple word replacement using the translation database
        translated_text = request.text
        for english_word, translated_word in translation_dict.items():
            translated_text = translated_text.replace(english_word, translated_word)
    else:
        # Mock translation - in a real system, this would call an actual translation API
        translated_text = f"[Translated to {request.target_language}] {request.text}"
    
    # Calculate confidence level for the translation (mock implementation)
    if request.source_language in TRANSLATION_DB and request.target_language in TRANSLATION_DB[request.source_language]:
        confidence = random.uniform(85, 95)
    else:
        confidence = random.uniform(70, 85)
    
    # Return the translation response with all metadata
    return TranslationResponse(
        translated_text=translated_text,
        source_language=request.source_language,
        target_language=request.target_language,
        confidence=confidence
    )

# ----------------------------------------------------------------------------
# CONTENT LOCALIZATION ENDPOINT
# Endpoint for localizing content for specific locales
# ----------------------------------------------------------------------------

@app.post("/localize", response_model=LocalizationResponse)
async def localize_content(request: LocalizationRequest):
    """
    Localize content for a specific locale
    
    Args:
        request (LocalizationRequest): Request containing content, target locale, and content type
        
    Returns:
        LocalizationResponse: Localized content with adaptations and cultural notes
        
    Example:
        POST /localize
        {
            "content": "We are looking for a Software Engineer...",
            "target_locale": "es-ES",
            "content_type": "job_description"
        }
    """
    # In a real implementation, this would adapt content for cultural and linguistic nuances
    # For this mock, we'll generate localization adaptations
    
    # Initialize lists for storing localization information
    adaptations = []
    cultural_notes = []
    
    # Generate adaptations based on target locale
    if "es" in request.target_locale.lower():
        adaptations.append("Adjusted date formats to DD/MM/YYYY")
        adaptations.append("Replaced 'color' with 'colour' where appropriate")
        cultural_notes.append("In Spanish-speaking countries, it's common to include more personal information")
    elif "fr" in request.target_locale.lower():
        adaptations.append("Adjusted number formats to use commas as decimal separators")
        cultural_notes.append("In French culture, formal language is preferred in professional documents")
    elif "de" in request.target_locale.lower():
        adaptations.append("Adjusted address format for German conventions")
        cultural_notes.append("German job applications typically include a photo")
    elif "zh" in request.target_locale.lower():
        adaptations.append("Converted text direction to right-to-left where appropriate")
        cultural_notes.append("In Chinese culture, modesty is valued in self-descriptions")
    else:
        adaptations.append("Applied general localization rules")
        cultural_notes.append("Consider cultural norms for professional communication")
    
    # Generate localized content with locale identifier
    localized_content = f"[Localized for {request.target_locale}] {request.content}"
    
    # Return the localization response with all adaptations
    return LocalizationResponse(
        localized_content=localized_content,
        locale=request.target_locale,
        adaptations_made=adaptations,
        cultural_notes=cultural_notes
    )

# ----------------------------------------------------------------------------
# LANGUAGE DETECTION ENDPOINT
# Endpoint for detecting the language of provided text
# ----------------------------------------------------------------------------

@app.post("/detect-language", response_model=LanguageDetectionResponse)
async def detect_language(request: LanguageDetectionRequest):
    """
    Detect the language of provided text
    
    Args:
        request (LanguageDetectionRequest): Request containing text to analyze
        
    Returns:
        LanguageDetectionResponse: Detected language with confidence and alternatives
        
    Example:
        POST /detect-language
        {
            "text": "Ingeniero de Software con 5 años de experiencia"
        }
    """
    # In a real implementation, this would use language detection algorithms
    # For this mock, we'll randomly select a language with some logic
    
    # Simple heuristic: check for common language patterns
    text_lower = request.text.lower()
    
    # Detect language based on common words and patterns
    if any(word in text_lower for word in ["the", "and", "is", "are"]):
        detected_language = "en"
    elif any(word in text_lower for word in ["el", "la", "de", "que"]):
        detected_language = "es"
    elif any(word in text_lower for word in ["le", "la", "de", "et"]):
        detected_language = "fr"
    elif any(word in text_lower for word in ["der", "die", "und", "ist"]):
        detected_language = "de"
    else:
        # Random selection from supported languages if no patterns match
        detected_language = random.choice(SUPPORTED_LANGUAGES)
    
    # Calculate confidence level for detection (mock implementation)
    confidence = random.uniform(80, 98)
    
    # Generate alternative language suggestions
    alternative_languages = random.sample(
        [lang for lang in SUPPORTED_LANGUAGES if lang != detected_language], 
        min(3, len(SUPPORTED_LANGUAGES) - 1)
    )
    
    # Return the language detection response with all results
    return LanguageDetectionResponse(
        detected_language=detected_language,
        confidence=confidence,
        alternative_languages=alternative_languages
    )

# ----------------------------------------------------------------------------
# CULTURAL ADAPTATION ENDPOINT
# Endpoint for adapting content for specific cultural contexts
# ----------------------------------------------------------------------------

@app.post("/cultural-adaptation", response_model=CulturalAdaptationResponse)
async def cultural_adaptation(request: CulturalAdaptationRequest):
    """
    Adapt content for specific cultural contexts
    
    Args:
        request (CulturalAdaptationRequest): Request containing content, target culture, and content type
        
    Returns:
        CulturalAdaptationResponse: Culturally adapted content with explanations
        
    Example:
        POST /cultural-adaptation
        {
            "content": "I am the best candidate for this position...",
            "target_culture": "Japanese",
            "content_type": "cover_letter"
        }
    """
    # In a real implementation, this would adjust content based on cultural norms and expectations
    # For this mock, we'll generate cultural adaptations
    
    # Format culture name for display
    culture = request.target_culture.capitalize()
    
    # Generate cultural adaptations based on target culture
    adaptations = []
    
    if "american" in request.target_culture.lower():
        adaptations.append("Emphasized individual achievements and results")
        adaptations.append("Used active voice and direct language")
    elif "german" in request.target_culture.lower():
        adaptations.append("Added formality and structure to communication")
        adaptations.append("Included detailed technical specifications")
    elif "japanese" in request.target_culture.lower():
        adaptations.append("Used more humble and group-oriented language")
        adaptations.append("Added respect for hierarchy and seniority")
    elif "brazilian" in request.target_culture.lower():
        adaptations.append("Used warmer and more personal language")
        adaptations.append("Emphasized relationship-building aspects")
    else:
        adaptations.append("Applied general cultural adaptation principles")
        adaptations.append("Adjusted tone and formality levels")
    
    # Generate culturally adapted content
    adapted_content = f"[Culturally adapted for {culture}] {request.content}"
    
    # Generate explanation of cultural adaptations
    explanation = f"This content has been adapted for {culture} cultural norms, "
    explanation += "focusing on communication style, formality levels, and cultural expectations."
    
    # Return the cultural adaptation response with all information
    return CulturalAdaptationResponse(
        adapted_content=adapted_content,
        culture=culture,
        adaptations_made=adaptations,
        explanation=explanation
    )

# ----------------------------------------------------------------------------
# SUPPORTED LANGUAGES ENDPOINT
# Endpoint for retrieving information about supported languages
# ----------------------------------------------------------------------------

@app.get("/supported-languages")
async def get_supported_languages():
    """
    Get a list of supported languages
    
    Returns:
        dict: Lists of supported languages, locales, and cultures
        
    Example:
        GET /supported-languages
    """
    # Return comprehensive information about language support
    return {"languages": SUPPORTED_LANGUAGES, "locales": SUPPORTED_LOCALES, "cultures": CULTURAL_CONTEXTS}

# ----------------------------------------------------------------------------
# LANGUAGE PAIR SUPPORT ENDPOINT
# Endpoint for checking support for specific language pairs
# ----------------------------------------------------------------------------

@app.get("/language-pair-support")
async def check_language_pair_support(source: str, target: str):
    """
    Check if a specific language pair is supported
    
    Args:
        source (str): Source language code
        target (str): Target language code
        
    Returns:
        dict: Information about support for the language pair
        
    Example:
        GET /language-pair-support?source=en&target=es
    """
    # Check if both languages are in our supported languages list
    supported = source in SUPPORTED_LANGUAGES and target in SUPPORTED_LANGUAGES
    
    # Determine quality level based on support status
    quality = "high" if supported else "unsupported"
    
    # Return information about language pair support
    return {
        "source_language": source,
        "target_language": target,
        "supported": supported,
        "quality": quality,
        "notes": "High-quality translations available" if supported else "Language pair not currently supported"
    }

# ============================================================================
# APPLICATION ENTRY POINT
# Main execution block for running the service
# ============================================================================

if __name__ == "__main__":
    # Import uvicorn for running the ASGI application
    import uvicorn
    
    # Run the FastAPI application with uvicorn
    # Host 0.0.0.0 makes it accessible from outside the container
    # Port 8118 is the designated port for this microservice
    uvicorn.run(app, host="0.0.0.0", port=8118)