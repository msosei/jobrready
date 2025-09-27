"""
Security Module for MyBrand Job Application Platform
Version: v2
Purpose: Implements security best practices, input validation, and vulnerability protection
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for security functionality
# ============================================================================

import re
import html
import hashlib
import secrets
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import jwt
from functools import wraps

# Local imports
from .logging_config import StructuredLogger
from .config import app_settings

# Create a structured logger for this module
logger = StructuredLogger(__name__)

# ============================================================================
# INPUT VALIDATION AND SANITIZATION
# Functions for validating and sanitizing user input to prevent injection attacks
# ============================================================================

class InputValidator:
    """Input validation and sanitization utilities."""
    
    # Regular expressions for validation
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PHONE_REGEX = re.compile(r'^\+?1?-?\.?\s?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})$')
    URL_REGEX = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 1000) -> str:
        """
        Sanitize a string by escaping HTML characters and limiting length.
        
        Args:
            text (str): The text to sanitize
            max_length (int): Maximum length of the text (default: 1000)
            
        Returns:
            str: The sanitized text
        """
        if not text:
            return ""
        
        # Escape HTML characters to prevent XSS
        sanitized = html.escape(text)
        
        # Limit length to prevent DoS attacks
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email (str): The email to validate
            
        Returns:
            bool: True if email is valid, False otherwise
        """
        if not email or len(email) > 254:  # RFC 5321 limit
            return False
        
        return bool(InputValidator.EMAIL_REGEX.match(email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate phone number format.
        
        Args:
            phone (str): The phone number to validate
            
        Returns:
            bool: True if phone number is valid, False otherwise
        """
        if not phone or len(phone) > 20:  # Reasonable limit
            return False
        
        return bool(InputValidator.PHONE_REGEX.match(phone))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format.
        
        Args:
            url (str): The URL to validate
            
        Returns:
            bool: True if URL is valid, False otherwise
        """
        if not url or len(url) > 2048:  # Reasonable limit
            return False
        
        return bool(InputValidator.URL_REGEX.match(url))
    
    @staticmethod
    def sanitize_json(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively sanitize JSON data.
        
        Args:
            data (Dict[str, Any]): The JSON data to sanitize
            
        Returns:
            Dict[str, Any]: The sanitized JSON data
        """
        if not isinstance(data, dict):
            return data
        
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized[key] = InputValidator.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[key] = InputValidator.sanitize_json(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    InputValidator.sanitize_json(item) if isinstance(item, dict) 
                    else InputValidator.sanitize_string(item) if isinstance(item, str)
                    else item for item in value
                ]
            else:
                sanitized[key] = value
        
        return sanitized

# ============================================================================
# AUTHENTICATION AND AUTHORIZATION
# Functions for JWT token management and access control
# ============================================================================

class JWTManager:
    """JWT token management utilities."""
    
    @staticmethod
    def generate_token(payload: Dict[str, Any], expires_in: int = 3600) -> str:
        """
        Generate a JWT token.
        
        Args:
            payload (Dict[str, Any]): The payload to encode
            expires_in (int): Token expiration time in seconds (default: 1 hour)
            
        Returns:
            str: The generated JWT token
        """
        # Add expiration time to payload
        payload["exp"] = datetime.utcnow() + timedelta(seconds=expires_in)
        payload["iat"] = datetime.utcnow()
        
        # Generate token
        token = jwt.encode(payload, app_settings.jwt_secret, algorithm="HS256")
        return token
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify a JWT token.
        
        Args:
            token (str): The token to verify
            
        Returns:
            Optional[Dict[str, Any]]: The decoded payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, app_settings.jwt_secret, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning("Invalid JWT token", error=str(e))
            return None
    
    @staticmethod
    def refresh_token(old_token: str, expires_in: int = 3600) -> Optional[str]:
        """
        Refresh a JWT token.
        
        Args:
            old_token (str): The token to refresh
            expires_in (int): New token expiration time in seconds (default: 1 hour)
            
        Returns:
            Optional[str]: The refreshed token if valid, None otherwise
        """
        payload = JWTManager.verify_token(old_token)
        if not payload:
            return None
        
        # Remove expiration claims for refresh
        payload.pop("exp", None)
        payload.pop("iat", None)
        
        return JWTManager.generate_token(payload, expires_in)

# ============================================================================
# RATE LIMITING
# Functions for implementing rate limiting to prevent abuse
# ============================================================================

class RateLimiter:
    """Rate limiting utilities."""
    
    def __init__(self):
        """Initialize the rate limiter."""
        self.requests = {}  # In production, use Redis or similar
    
    def is_allowed(self, identifier: str, max_requests: int = 100, window: int = 3600) -> bool:
        """
        Check if a request is allowed based on rate limiting.
        
        Args:
            identifier (str): Unique identifier for the client (e.g., IP address)
            max_requests (int): Maximum requests allowed in the window (default: 100)
            window (int): Time window in seconds (default: 3600 seconds/1 hour)
            
        Returns:
            bool: True if request is allowed, False otherwise
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window)
        
        # Clean old requests
        if identifier in self.requests:
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > window_start
            ]
        else:
            self.requests[identifier] = []
        
        # Check if under limit
        if len(self.requests[identifier]) < max_requests:
            self.requests[identifier].append(now)
            return True
        
        return False

# ============================================================================
# SECURITY HEADERS
# Functions for adding security headers to HTTP responses
# ============================================================================

def add_security_headers(response_headers: Dict[str, str]) -> Dict[str, str]:
    """
    Add security headers to HTTP responses.
    
    Args:
        response_headers (Dict[str, str]): Existing response headers
        
    Returns:
        Dict[str, str]: Response headers with security headers added
    """
    security_headers = {
        # Prevent XSS attacks
        "X-XSS-Protection": "1; mode=block",
        
        # Prevent MIME type sniffing
        "X-Content-Type-Options": "nosniff",
        
        # Control frame embedding
        "X-Frame-Options": "DENY",
        
        # Control referrer information
        "Referrer-Policy": "strict-origin-when-cross-origin",
        
        # Content Security Policy
        "Content-Security-Policy": (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        ),
        
        # Strict Transport Security
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        
        # Permissions Policy
        "Permissions-Policy": (
            "geolocation=(), "
            "microphone=(), "
            "camera=(), "
            "payment=(), "
            "usb=()"
        )
    }
    
    # Update response headers with security headers
    response_headers.update(security_headers)
    return response_headers

# ============================================================================
# PASSWORD SECURITY
# Functions for secure password handling
# ============================================================================

class PasswordManager:
    """Password security utilities."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using a salt.
        
        Args:
            password (str): The password to hash
            
        Returns:
            str: The hashed password
        """
        # Generate a salt
        salt = secrets.token_hex(16)
        
        # Hash the password with the salt
        pwdhash = hashlib.pbkdf2_hmac('sha256', 
                                      password.encode('utf-8'), 
                                      salt.encode('ascii'), 
                                      100000)  # 100,000 iterations
        pwdhash_hex = pwdhash.hex()
        
        # Return salt and hash combined
        return f"{salt}${pwdhash_hex}"
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password (str): The password to verify
            hashed (str): The stored hash
            
        Returns:
            bool: True if password matches, False otherwise
        """
        if not password or not hashed:
            return False
        
        # Split the hash to get salt and hash
        try:
            salt, stored_hash = hashed.split('$')
        except ValueError:
            return False
        
        # Hash the provided password with the stored salt
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                      password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)  # 100,000 iterations
        pwdhash_hex = pwdhash.hex()
        
        # Compare hashes
        return pwdhash_hex == stored_hash

# ============================================================================
# VULNERABILITY SCANNING
# Functions for scanning dependencies and code for vulnerabilities
# ============================================================================

class VulnerabilityScanner:
    """Vulnerability scanning utilities."""
    
    @staticmethod
    def check_dependencies() -> List[Dict[str, Any]]:
        """
        Check dependencies for known vulnerabilities.
        
        In a real implementation, this would integrate with vulnerability
        databases like CVE or use tools like safety or bandit.
        
        Returns:
            List[Dict[str, Any]]: List of vulnerability findings
        """
        # This is a placeholder implementation
        # In production, integrate with actual vulnerability scanning tools
        logger.info("Dependency vulnerability scan would be performed here")
        
        # Example findings format
        findings = [
            {
                "package": "example-package",
                "version": "1.0.0",
                "vulnerability": "CVE-2023-12345",
                "severity": "HIGH",
                "description": "Example vulnerability description",
                "remediation": "Upgrade to version 1.2.0 or later"
            }
        ]
        
        return findings
    
    @staticmethod
    def scan_code_for_vulnerabilities() -> List[Dict[str, Any]]:
        """
        Scan code for common security vulnerabilities.
        
        In a real implementation, this would use static analysis tools
        like bandit for Python code.
        
        Returns:
            List[Dict[str, Any]]: List of vulnerability findings
        """
        # This is a placeholder implementation
        # In production, integrate with actual code scanning tools
        logger.info("Code vulnerability scan would be performed here")
        
        # Example findings format
        findings = [
            {
                "file": "example.py",
                "line": 42,
                "vulnerability": "SQL Injection",
                "severity": "CRITICAL",
                "description": "Potential SQL injection vulnerability detected",
                "remediation": "Use parameterized queries instead of string formatting"
            }
        ]
        
        return findings

# ============================================================================
# SECURITY DECORATORS
# Decorators for adding security checks to functions
# ============================================================================

def require_auth(f):
    """
    Decorator to require authentication for a function.
    
    Args:
        f: The function to decorate
        
    Returns:
        The decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # In a real implementation, check for valid authentication token
        # This is a simplified example
        logger.debug("Authentication required for function", function=f.__name__)
        return f(*args, **kwargs)
    
    return decorated_function

def rate_limit(max_requests: int = 100, window: int = 3600):
    """
    Decorator to apply rate limiting to a function.
    
    Args:
        max_requests (int): Maximum requests allowed in the window
        window (int): Time window in seconds
        
    Returns:
        The decorated function
    """
    def decorator(f):
        limiter = RateLimiter()
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # In a real implementation, get client identifier (e.g., IP address)
            # This is a simplified example
            client_id = "default_client"
            
            if not limiter.is_allowed(client_id, max_requests, window):
                logger.warning("Rate limit exceeded", client_id=client_id)
                raise Exception("Rate limit exceeded")
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator

# ============================================================================
# UTILITY FUNCTIONS
# Helper functions for common security operations
# ============================================================================

def generate_secure_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token.
    
    Args:
        length (int): Length of the token (default: 32)
        
    Returns:
        str: The generated secure token
    """
    return secrets.token_urlsafe(length)

def mask_sensitive_data(data: str, show_last: int = 4) -> str:
    """
    Mask sensitive data (e.g., for logging).
    
    Args:
        data (str): The data to mask
        show_last (int): Number of characters to show at the end (default: 4)
        
    Returns:
        str: The masked data
    """
    if not data:
        return ""
    
    if len(data) <= show_last:
        return "*" * len(data)
    
    return "*" * (len(data) - show_last) + data[-show_last:]