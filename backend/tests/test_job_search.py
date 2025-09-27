"""
Test suite for Job Search functionality
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import httpx

from app.main import app
from app.job_search import JobSearchRequest, Job

# Create a test client
client = TestClient(app)

# Sample job data for testing
sample_job = Job(
    id=1,
    title="Software Engineer",
    company="Test Company",
    location="Test Location",
    type="Full-time",
    remote=True,
    urgent=False,
    description="Test job description",
    posted="2023-01-01",
    isNew=True
)

class TestJobSearch:
    """Test cases for job search functionality"""
    
    def test_job_search_request_validation(self):
        """Test JobSearchRequest validation"""
        # Test valid request
        request = JobSearchRequest(
            keyword="developer",
            location="New York",
            limit=10,
            offset=0
        )
        assert request.keyword == "developer"
        assert request.location == "New York"
        assert request.limit == 10
        assert request.offset == 0
    
    def test_job_search_request_validation_edge_cases(self):
        """Test JobSearchRequest validation edge cases"""
        # Test keyword sanitization
        request = JobSearchRequest(keyword="  developer  ")
        assert request.keyword == "developer"
        
        # Test limit bounds
        request = JobSearchRequest(limit=1000)
        assert request.limit == 100
        
        request = JobSearchRequest(limit=-5)
        assert request.limit == 1
        
        # Test offset bounds
        request = JobSearchRequest(offset=-5)
        assert request.offset == 0
    
    @patch("app.job_search.search_jobs_adzuna")
    def test_search_jobs_endpoint_success(self, mock_search):
        """Test successful job search endpoint"""
        # Mock the search function to return sample data
        mock_response = {
            "jobs": [sample_job.dict()],
            "total": 1,
            "hasMore": False
        }
        mock_search.return_value = mock_response
        
        # Make a request to the search endpoint
        response = client.get("/jobs/search?keyword=developer&limit=10")
        
        # Assert the response
        assert response.status_code == 200
        data = response.json()
        assert "jobs" in data
        assert "total" in data
        assert data["total"] == 1
        assert len(data["jobs"]) == 1
    
    @patch("app.job_search.search_jobs_adzuna")
    def test_search_jobs_endpoint_validation_error(self, mock_search):
        """Test job search endpoint with validation error"""
        # Make a request with invalid parameters
        response = client.get("/jobs/search?limit=abc")
        
        # Assert the response (FastAPI will handle validation)
        assert response.status_code == 422
    
    @patch("app.job_search.search_jobs_adzuna")
    def test_search_jobs_endpoint_internal_error(self, mock_search):
        """Test job search endpoint with internal error"""
        # Mock the search function to raise an exception
        mock_search.side_effect = Exception("Internal server error")
        
        # Make a request to the search endpoint
        response = client.get("/jobs/search?keyword=developer")
        
        # Assert the response
        assert response.status_code == 200  # Should fall back to local search
    
    def test_job_model_validation(self):
        """Test Job model validation"""
        # Test valid job model
        job = Job(
            id=1,
            title="Software Engineer",
            company="Test Company",
            location="Test Location",
            type="Full-time",
            remote=True,
            urgent=False,
            description="Test job description",
            posted="2023-01-01",
            isNew=True
        )
        assert job.id == 1
        assert job.title == "Software Engineer"
    
    def test_local_search_functionality(self):
        """Test local search functionality"""
        from app.job_search import search_jobs_locally
        
        # Test search with no filters
        request = JobSearchRequest()
        result = search_jobs_locally(request)
        assert isinstance(result, dict)
        assert "jobs" in result
        assert "total" in result
        assert "hasMore" in result
    
    def test_local_search_with_filters(self):
        """Test local search with filters"""
        from app.job_search import search_jobs_locally
        
        # Test search with keyword filter
        request = JobSearchRequest(keyword="software")
        result = search_jobs_locally(request)
        assert isinstance(result, dict)
        
        # Test search with location filter
        request = JobSearchRequest(location="san francisco")
        result = search_jobs_locally(request)
        assert isinstance(result, dict)
    
    @pytest.mark.asyncio
    async def test_adzuna_search_success(self):
        """Test Adzuna search success"""
        from app.job_search import search_jobs_adzuna
        
        # Mock HTTP response
        mock_response_data = {
            "results": [
                {
                    "id": "1",
                    "title": "Software Engineer",
                    "company": {"display_name": "Test Company"},
                    "location": {"display_name": "Test Location"},
                    "description": "Test job description",
                    "contract_time": "Full-time",
                    "created": "2023-01-01"
                }
            ],
            "count": 1
        }
        
        with patch("httpx.AsyncClient") as mock_client:
            # Configure the mock
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.get.return_value = AsyncMock(
                status_code=200,
                json=AsyncMock(return_value=mock_response_data)
            )
            
            # Test the function
            request = JobSearchRequest(keyword="developer")
            result = await search_jobs_adzuna(request)
            
            # Assert the result
            assert isinstance(result, dict)
            assert "jobs" in result
            assert "total" in result
            assert result["total"] == 1

if __name__ == "__main__":
    pytest.main([__file__])