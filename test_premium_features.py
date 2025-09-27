#!/usr/bin/env python3
"""
Test script for premium features
"""

import requests
import json
import time

# Service URLs (using localhost for testing)
MOCK_INTERVIEWER_URL = "http://localhost:8114"
DIVERSITY_INSIGHTS_URL = "http://localhost:8115"
DOCUMENT_SUMMARIZER_URL = "http://localhost:8116"

def test_mock_interviewer():
    """Test the mock interviewer service"""
    print("Testing Mock Interviewer Service...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{MOCK_INTERVIEWER_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test start interview
    interview_data = {
        "job_title": "Software Engineer",
        "industry": "Technology",
        "experience_level": "Mid-level",
        "interview_type": "Technical",
        "skills": ["Python", "Docker", "AWS"]
    }
    
    try:
        response = requests.post(f"{MOCK_INTERVIEWER_URL}/start-interview", json=interview_data)
        print(f"Start interview: {response.status_code}")
        if response.status_code == 200:
            print(f"First question: {response.json()}")
    except Exception as e:
        print(f"Start interview failed: {e}")

def test_diversity_insights():
    """Test the diversity insights service"""
    print("\nTesting Diversity Insights Service...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{DIVERSITY_INSIGHTS_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test job analysis
    job_data = {
        "job_title": "Software Engineer",
        "company_name": "TechCorp",
        "job_description": "We are looking for a rockstar developer with 5+ years experience",
        "company_description": "Equal opportunity employer"
    }
    
    try:
        response = requests.post(f"{DIVERSITY_INSIGHTS_URL}/analyze-job", json=job_data)
        print(f"Job analysis: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Diversity score: {result['diversity_score']}")
            print(f"Inclusion score: {result['inclusion_score']}")
            print(f"Detected bias: {result['detected_bias']}")
    except Exception as e:
        print(f"Job analysis failed: {e}")

def test_document_summarizer():
    """Test the document summarizer service"""
    print("\nTesting Document Summarizer Service...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{DOCUMENT_SUMMARIZER_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test document summarization
    doc_data = {
        "document_text": "Experienced software engineer with 5 years of Python development experience. Developed scalable web applications using Django and Flask. Proficient in AWS and Docker. Led a team of 3 developers on a project that improved system performance by 40%.",
        "document_type": "resume",
        "summary_length": "medium"
    }
    
    try:
        response = requests.post(f"{DOCUMENT_SUMMARIZER_URL}/summarize", json=doc_data)
        print(f"Document summarization: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Summary: {result['summary']}")
            print(f"Key points: {len(result['key_points'])}")
    except Exception as e:
        print(f"Document summarization failed: {e}")

if __name__ == "__main__":
    print("Testing Premium Features...")
    print("=" * 50)
    
    test_mock_interviewer()
    test_diversity_insights()
    test_document_summarizer()
    
    print("\n" + "=" * 50)
    print("Testing complete!")