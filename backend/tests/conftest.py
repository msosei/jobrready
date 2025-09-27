"""
Test configuration and fixtures for the MyBrand backend
"""

import sys
import os

# Add the app directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Import pytest if available
try:
    import pytest
except ImportError:
    pytest = None

def pytest_configure(config):
    """Configure pytest settings"""
    if pytest:
        config.addinivalue_line(
            "markers", "asyncio: mark test as async"
        )

# Environment setup for testing
os.environ["TESTING"] = "true"
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_ANON_KEY"] = "test-anon-key"
os.environ["SUPABASE_SERVICE_ROLE"] = "test-service-role-key"
os.environ["OPENAI_API_KEY"] = "test-openai-key"
os.environ["ADZUNA_APP_ID"] = "test-adzuna-app-id"
os.environ["ADZUNA_APP_KEY"] = "test-adzuna-app-key"