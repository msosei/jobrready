"""
Shared Utilities Module for MyBrand Job Application Platform
Version: v2
Purpose: Common utility functions and helpers used across the application
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for utility functions
# ============================================================================

import re
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
import hashlib
import secrets

# ============================================================================
# LOGGING CONFIGURATION
# Set up logging for utility functions
# ============================================================================

logger = logging.getLogger(__name__)

# ============================================================================
# INPUT VALIDATION UTILITIES
# Functions for validating and sanitizing user input
# ============================================================================

def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent XSS and other injection attacks.
    
    Args:
        text (str): The text to sanitize
        
    Returns:
        str: The sanitized text with potentially dangerous characters escaped
    """
    if not text:
        return ""
    
    # Remove or escape potentially dangerous HTML characters
    sanitized = text.replace("<", "&lt;").replace(">", "&gt;")
    
    # Remove potentially dangerous SQL characters (basic protection)
    sanitized = re.sub(r"[';\"\\]", "", sanitized)
    
    return sanitized

def validate_email(email: str) -> bool:
    """
    Validate email format using regex.
    
    Args:
        email (str): The email to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone (str): The phone number to validate
        
    Returns:
        bool: True if phone number is valid, False otherwise
    """
    if not phone:
        return False
    
    # Remove common separators and check if remaining characters are digits
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15

# ============================================================================
# STRING UTILITIES
# Functions for string manipulation and processing
# ============================================================================

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length with a suffix.
    
    Args:
        text (str): The text to truncate
        max_length (int): Maximum length of the text (default: 100)
        suffix (str): Suffix to append if text is truncated (default: "...")
        
    Returns:
        str: The truncated text
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def generate_slug(text: str) -> str:
    """
    Generate a URL-friendly slug from text.
    
    Args:
        text (str): The text to convert to a slug
        
    Returns:
        str: The generated slug
    """
    if not text:
        return ""
    
    # Convert to lowercase and replace spaces/special characters with hyphens
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', text.lower())
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug

# ============================================================================
# SECURITY UTILITIES
# Functions for security-related operations
# ============================================================================

def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256 with a salt.
    
    Args:
        password (str): The password to hash
        
    Returns:
        str: The hashed password
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Generate a random salt
    salt = secrets.token_hex(16)
    
    # Hash the password with the salt
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    
    # Return salt and hash combined
    return f"{salt}${hashed}"

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
    parts = hashed.split('$')
    if len(parts) != 2:
        return False
    
    salt, stored_hash = parts
    
    # Hash the provided password with the stored salt
    computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    
    # Compare hashes
    return computed_hash == stored_hash

def generate_token(length: int = 32) -> str:
    """
    Generate a secure random token.
    
    Args:
        length (int): Length of the token (default: 32)
        
    Returns:
        str: The generated token
    """
    return secrets.token_urlsafe(length)

# ============================================================================
# DATE/TIME UTILITIES
# Functions for date and time operations
# ============================================================================

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime object as a string.
    
    Args:
        dt (datetime): The datetime to format
        format_str (str): The format string (default: "%Y-%m-%d %H:%M:%S")
        
    Returns:
        str: The formatted datetime string
    """
    if not dt:
        return ""
    
    return dt.strftime(format_str)

def days_since(date: datetime) -> int:
    """
    Calculate the number of days since a given date.
    
    Args:
        date (datetime): The date to calculate from
        
    Returns:
        int: Number of days since the given date
    """
    if not date:
        return 0
    
    delta = datetime.now() - date
    return delta.days

# ============================================================================
# DATA PROCESSING UTILITIES
# Functions for processing and transforming data
# ============================================================================

def remove_duplicates(items: List[Any]) -> List[Any]:
    """
    Remove duplicates from a list while preserving order.
    
    Args:
        items (List[Any]): The list to remove duplicates from
        
    Returns:
        List[Any]: The list with duplicates removed
    """
    if not items:
        return []
    
    seen = set()
    result = []
    
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    return result

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """
    Flatten a nested dictionary.
    
    Args:
        d (Dict[str, Any]): The dictionary to flatten
        parent_key (str): The parent key for nested items (default: '')
        sep (str): The separator for nested keys (default: '_')
        
    Returns:
        Dict[str, Any]: The flattened dictionary
    """
    if not d:
        return {}
    
    items = []
    
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    
    return dict(items)