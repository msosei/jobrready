#!/usr/bin/env python3
"""
Test script for all premium features
"""

import requests
import json
import time

# Service URLs (using localhost for testing)
SERVICES = {
    "mock_interviewer": "http://localhost:8114",
    "diversity_insights": "http://localhost:8115",
    "document_summarizer": "http://localhost:8116",
    "voice_agent": "http://localhost:8117",
    "multi_language": "http://localhost:8118",
    "course_recommender": "http://localhost:8119"
}

def test_service_health(service_name, url):
    """Test the health endpoint of a service"""
    print(f"Testing {service_name}...")
    
    try:
        response = requests.get(f"{url}/health")
        if response.status_code == 200:
            print(f"  ✓ {service_name} health check: PASSED")
            return True
        else:
            print(f"  ✗ {service_name} health check: FAILED (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"  ✗ {service_name} health check: FAILED ({e})")
        return False

def test_mock_interviewer(url):
    """Test the mock interviewer service"""
    print("Testing Mock Interviewer functionality...")
    
    try:
        # Test start interview
        interview_data = {
            "job_title": "Software Engineer",
            "industry": "Technology",
            "experience_level": "Mid-level",
            "interview_type": "Technical",
            "skills": ["Python", "Docker", "AWS"]
        }
        
        response = requests.post(f"{url}/start-interview", json=interview_data)
        if response.status_code == 200:
            print("  ✓ Mock Interviewer start interview: PASSED")
            return True
        else:
            print(f"  ✗ Mock Interviewer start interview: FAILED (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"  ✗ Mock Interviewer start interview: FAILED ({e})")
        return False

def test_diversity_insights(url):
    """Test the diversity insights service"""
    print("Testing Diversity Insights functionality...")
    
    try:
        # Test job analysis
        job_data = {
            "job_title": "Software Engineer",
            "company_name": "TechCorp",
            "job_description": "We are looking for a rockstar developer with 5+ years experience",
            "company_description": "Equal opportunity employer"
        }
        
        response = requests.post(f"{url}/analyze-job", json=job_data)
        if response.status_code == 200:
            print("  ✓ Diversity Insights job analysis: PASSED")
            return True
        else:
            print(f"  ✗ Diversity Insights job analysis: FAILED (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"  ✗ Diversity Insights job analysis: FAILED ({e})")
        return False

def test_document_summarizer(url):
    """Test the document summarizer service"""
    print("Testing Document Summarizer functionality...")
    
    try:
        # Test document summarization
        doc_data = {
            "document_text": "Experienced software engineer with 5 years of Python development experience.",
            "document_type": "resume",
            "summary_length": "medium"
        }
        
        response = requests.post(f"{url}/summarize", json=doc_data)
        if response.status_code == 200:
            print("  ✓ Document Summarizer summarization: PASSED")
            return True
        else:
            print(f"  ✗ Document Summarizer summarization: FAILED (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"  ✗ Document Summarizer summarization: FAILED ({e})")
        return False

def test_voice_agent(url):
    """Test the voice agent service"""
    print("Testing Voice Agent functionality...")
    
    try:
        # Test voice command processing
        command_data = {
            "command": "Help me with my resume",
            "user_id": "user123"
        }
        
        response = requests.post(f"{url}/process-command", json=command_data)
        if response.status_code == 200:
            print("  ✓ Voice Agent command processing: PASSED")
            return True
        else:
            print(f"  ✗ Voice Agent command processing: FAILED (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"  ✗ Voice Agent command processing: FAILED ({e})")
        return False

def test_multi_language(url):
    """Test the multi-language service"""
    print("Testing Multi-Language functionality...")
    
    try:
        # Test language translation
        translation_data = {
            "text": "Software Engineer",
            "source_language": "en",
            "target_language": "es"
        }
        
        response = requests.post(f"{url}/translate", json=translation_data)
        if response.status_code == 200:
            print("  ✓ Multi-Language translation: PASSED")
            return True
        else:
            print(f"  ✗ Multi-Language translation: FAILED (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"  ✗ Multi-Language translation: FAILED ({e})")
        return False

def test_course_recommender(url):
    """Test the course recommender service"""
    print("Testing Course Recommender functionality...")
    
    try:
        # Test skill assessment
        assessment_data = {
            "current_skills": ["Python", "SQL"],
            "target_role": "Data Scientist",
            "experience_level": "Entry-level"
        }
        
        response = requests.post(f"{url}/assess-skills", json=assessment_data)
        if response.status_code == 200:
            print("  ✓ Course Recommender skill assessment: PASSED")
            return True
        else:
            print(f"  ✗ Course Recommender skill assessment: FAILED (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"  ✗ Course Recommender skill assessment: FAILED ({e})")
        return False

def main():
    print("Testing All Premium Features...")
    print("=" * 50)
    
    # Test health endpoints for all services
    health_results = []
    for service_name, url in SERVICES.items():
        result = test_service_health(service_name, url)
        health_results.append(result)
        time.sleep(0.5)  # Small delay between requests
    
    print("\nTesting functionality for each service...")
    print("-" * 40)
    
    # Test functionality for each service
    functionality_results = []
    
    functionality_results.append(test_mock_interviewer(SERVICES["mock_interviewer"]))
    time.sleep(0.5)
    
    functionality_results.append(test_diversity_insights(SERVICES["diversity_insights"]))
    time.sleep(0.5)
    
    functionality_results.append(test_document_summarizer(SERVICES["document_summarizer"]))
    time.sleep(0.5)
    
    functionality_results.append(test_voice_agent(SERVICES["voice_agent"]))
    time.sleep(0.5)
    
    functionality_results.append(test_multi_language(SERVICES["multi_language"]))
    time.sleep(0.5)
    
    functionality_results.append(test_course_recommender(SERVICES["course_recommender"]))
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    health_passed = sum(health_results)
    health_total = len(health_results)
    functionality_passed = sum(functionality_results)
    functionality_total = len(functionality_results)
    
    print(f"Health Checks: {health_passed}/{health_total} passed")
    print(f"Functionality Tests: {functionality_passed}/{functionality_total} passed")
    
    if health_passed == health_total and functionality_passed == functionality_total:
        print("\n🎉 All tests passed! Premium features are ready to use.")
    else:
        print("\n⚠️  Some tests failed. Please check the services.")

if __name__ == "__main__":
    main()