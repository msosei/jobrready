"""
Error Handling Module for MyBrand Job Application Platform
Version: v2
Purpose: Centralized error handling with graceful fallbacks and user-friendly error messages
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for error handling
# ============================================================================

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError as PydanticValidationError
import logging
import traceback
from typing import Dict, Any, Optional
import httpx

# Local imports
from .logging_config import StructuredLogger

# Create a structured logger for this module
logger = StructuredLogger(__name__)

# ============================================================================
# CUSTOM EXCEPTION CLASSES
# Custom exception classes for different error types
# ============================================================================

class ServiceUnavailableError(Exception):
    """Exception raised when a required service is unavailable."""
    def __init__(self, service_name: str, original_error: Optional[Exception] = None):
        self.service_name = service_name
        self.original_error = original_error
        super().__init__(f"Service {service_name} is unavailable")

class ValidationError(Exception):
    """Exception raised when data validation fails."""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"Validation error for field '{field}': {message}")

class ExternalAPIError(Exception):
    """Exception raised when an external API returns an error."""
    def __init__(self, api_name: str, status_code: int, message: str):
        self.api_name = api_name
        self.status_code = status_code
        self.message = message
        super().__init__(f"External API {api_name} error ({status_code}): {message}")

# ============================================================================
# ERROR RESPONSE STRUCTURE
# Standardized error response format
# ============================================================================

class ErrorResponse:
    """Standardized error response structure."""
    
    def __init__(self, error_code: str, message: str, details: Optional[Dict[str, Any]] = None):
        self.error_code = error_code
        self.message = message
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the error response to a dictionary."""
        return {
            "error": {
                "code": self.error_code,
                "message": self.message,
                "details": self.details
            }
        }

# ============================================================================
# ERROR HANDLERS
# FastAPI exception handlers for different error types
# ============================================================================

async def service_unavailable_handler(request: Request, exc: ServiceUnavailableError) -> JSONResponse:
    """
    Handle ServiceUnavailableError exceptions.
    
    Args:
        request (Request): The incoming request
        exc (ServiceUnavailableError): The exception
        
    Returns:
        JSONResponse: A JSON response with error details
    """
    logger.error("Service unavailable", 
                service_name=exc.service_name,
                original_error=str(exc.original_error) if exc.original_error else None)
    
    error_response = ErrorResponse(
        error_code="SERVICE_UNAVAILABLE",
        message=f"The service {exc.service_name} is currently unavailable. Please try again later.",
        details={
            "service": exc.service_name,
            "timestamp": __import__('datetime').datetime.utcnow().isoformat() + "Z"
        }
    )
    
    return JSONResponse(
        status_code=503,
        content=error_response.to_dict()
    )

async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """
    Handle ValidationError exceptions.
    
    Args:
        request (Request): The incoming request
        exc (ValidationError): The exception
        
    Returns:
        JSONResponse: A JSON response with error details
    """
    logger.warning("Validation error", 
                  field=exc.field,
                  validation_message=exc.message)
    
    error_response = ErrorResponse(
        error_code="VALIDATION_ERROR",
        message=f"Invalid data provided for field '{exc.field}': {exc.message}",
        details={
            "field": exc.field,
            "validation_message": exc.message
        }
    )
    
    return JSONResponse(
        status_code=400,
        content=error_response.to_dict()
    )

async def external_api_error_handler(request: Request, exc: ExternalAPIError) -> JSONResponse:
    """
    Handle ExternalAPIError exceptions.
    
    Args:
        request (Request): The incoming request
        exc (ExternalAPIError): The exception
        
    Returns:
        JSONResponse: A JSON response with error details
    """
    logger.error("External API error", 
                api_name=exc.api_name,
                status_code=exc.status_code,
                error_message=exc.message)
    
    error_response = ErrorResponse(
        error_code="EXTERNAL_API_ERROR",
        message=f"Error communicating with {exc.api_name}: {exc.message}",
        details={
            "api": exc.api_name,
            "status_code": exc.status_code
        }
    )
    
    # Map HTTP status codes appropriately
    status_code = 502 if exc.status_code >= 500 else exc.status_code
    
    return JSONResponse(
        status_code=status_code,
        content=error_response.to_dict()
    )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTPException exceptions.
    
    Args:
        request (Request): The incoming request
        exc (HTTPException): The exception
        
    Returns:
        JSONResponse: A JSON response with error details
    """
    logger.warning("HTTP exception", 
                  status_code=exc.status_code,
                  error_detail=exc.detail)
    
    error_response = ErrorResponse(
        error_code="HTTP_ERROR",
        message=exc.detail,
        details={
            "status_code": exc.status_code
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.to_dict()
    )

async def request_validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle RequestValidationError exceptions.
    
    Args:
        request (Request): The incoming request
        exc (RequestValidationError): The exception
        
    Returns:
        JSONResponse: A JSON response with error details
    """
    logger.warning("Request validation error", 
                  errors=str(exc.errors()))
    
    # Extract the first validation error for a user-friendly message
    first_error = exc.errors()[0] if exc.errors() else {}
    field = first_error.get("loc", ["unknown"])[-1] if first_error.get("loc") else "unknown"
    message = first_error.get("msg", "Invalid data provided")
    
    error_response = ErrorResponse(
        error_code="REQUEST_VALIDATION_ERROR",
        message=f"Invalid request data for field '{field}': {message}",
        details={
            "errors": exc.errors()
        }
    )
    
    return JSONResponse(
        status_code=422,
        content=error_response.to_dict()
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle general exceptions.
    
    Args:
        request (Request): The incoming request
        exc (Exception): The exception
        
    Returns:
        JSONResponse: A JSON response with error details
    """
    logger.error("Unhandled exception", 
                exception_type=type(exc).__name__,
                exception_message=str(exc),
                traceback=traceback.format_exc())
    
    error_response = ErrorResponse(
        error_code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred. Please try again later.",
        details={
            "timestamp": __import__('datetime').datetime.utcnow().isoformat() + "Z"
        }
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.to_dict()
    )

# ============================================================================
# SERVICE CLIENT WITH FALLBACK
# HTTP client with automatic fallback and retry mechanisms
# ============================================================================

class ServiceClient:
    """HTTP client with automatic fallback and retry mechanisms."""
    
    def __init__(self, service_name: str, primary_url: str, fallback_url: Optional[str] = None):
        """
        Initialize the service client.
        
        Args:
            service_name (str): The name of the service
            primary_url (str): The primary service URL
            fallback_url (str, optional): The fallback service URL
        """
        self.service_name = service_name
        self.primary_url = primary_url
        self.fallback_url = fallback_url
        self.logger = StructuredLogger(f"service_client.{service_name}")
    
    async def post(self, endpoint: str, json_data: Dict[str, Any], timeout: float = 30.0) -> Dict[str, Any]:
        """
        Make a POST request with automatic fallback.
        
        Args:
            endpoint (str): The endpoint to call
            json_data (Dict[str, Any]): The JSON data to send
            timeout (float): The request timeout in seconds
            
        Returns:
            Dict[str, Any]: The response data
            
        Raises:
            ServiceUnavailableError: If both primary and fallback services fail
        """
        # Try primary service first
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.primary_url}{endpoint}",
                    json=json_data,
                    timeout=timeout
                )
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            self.logger.warning("Primary service request failed", 
                              endpoint=endpoint,
                              error=str(e))
            
            # Try fallback service if available
            if self.fallback_url:
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            f"{self.fallback_url}{endpoint}",
                            json=json_data,
                            timeout=timeout
                        )
                        response.raise_for_status()
                        self.logger.info("Fallback service request succeeded", endpoint=endpoint)
                        return response.json()
                except httpx.RequestError as fallback_error:
                    self.logger.error("Fallback service request failed", 
                                    endpoint=endpoint,
                                    error=str(fallback_error))
                    raise ServiceUnavailableError(self.service_name, fallback_error)
            
            # No fallback available
            raise ServiceUnavailableError(self.service_name, e)
        except httpx.HTTPStatusError as e:
            self.logger.error("Primary service returned HTTP error", 
                            endpoint=endpoint,
                            status_code=e.response.status_code,
                            error=str(e))
            raise ExternalAPIError(self.service_name, e.response.status_code, str(e))
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, timeout: float = 30.0) -> Dict[str, Any]:
        """
        Make a GET request with automatic fallback.
        
        Args:
            endpoint (str): The endpoint to call
            params (Dict[str, Any], optional): The query parameters
            timeout (float): The request timeout in seconds
            
        Returns:
            Dict[str, Any]: The response data
            
        Raises:
            ServiceUnavailableError: If both primary and fallback services fail
        """
        # Try primary service first
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.primary_url}{endpoint}",
                    params=params,
                    timeout=timeout
                )
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            self.logger.warning("Primary service request failed", 
                              endpoint=endpoint,
                              error=str(e))
            
            # Try fallback service if available
            if self.fallback_url:
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(
                            f"{self.fallback_url}{endpoint}",
                            params=params,
                            timeout=timeout
                        )
                        response.raise_for_status()
                        self.logger.info("Fallback service request succeeded", endpoint=endpoint)
                        return response.json()
                except httpx.RequestError as fallback_error:
                    self.logger.error("Fallback service request failed", 
                                    endpoint=endpoint,
                                    error=str(fallback_error))
                    raise ServiceUnavailableError(self.service_name, fallback_error)
            
            # No fallback available
            raise ServiceUnavailableError(self.service_name, e)
        except httpx.HTTPStatusError as e:
            self.logger.error("Primary service returned HTTP error", 
                            endpoint=endpoint,
                            status_code=e.response.status_code,
                            error=str(e))
            raise ExternalAPIError(self.service_name, e.response.status_code, str(e))

# ============================================================================
# UTILITY FUNCTIONS
# Helper functions for common error handling patterns
# ============================================================================

def handle_service_result(result: Dict[str, Any], service_name: str) -> Dict[str, Any]:
    """
    Handle service result with validation.
    
    Args:
        result (Dict[str, Any]): The service result
        service_name (str): The service name for logging
        
    Returns:
        Dict[str, Any]: The validated result
        
    Raises:
        ServiceUnavailableError: If the result indicates a service error
    """
    logger = StructuredLogger(f"service_result.{service_name}")
    
    # Check for common error indicators in the result
    if "error" in result:
        error_msg = result["error"]
        logger.error("Service returned error", 
                    service_name=service_name,
                    error=error_msg)
        raise ServiceUnavailableError(service_name, Exception(error_msg))
    
    # Check for HTTP error status in the result
    if "status_code" in result and result["status_code"] >= 400:
        status_code = result["status_code"]
        error_msg = result.get("message", "Unknown error")
        logger.error("Service returned HTTP error", 
                    service_name=service_name,
                    status_code=status_code,
                    error=error_msg)
        raise ExternalAPIError(service_name, status_code, error_msg)
    
    return result

def create_fallback_response(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a fallback response for when services are unavailable.
    
    Args:
        message (str): The fallback message
        data (Dict[str, Any], optional): Additional data to include
        
    Returns:
        Dict[str, Any]: The fallback response
    """
    response = {
        "message": message,
        "fallback": True
    }
    
    if data:
        response.update(data)
    
    return response