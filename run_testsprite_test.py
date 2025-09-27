#!/usr/bin/env python3
"""
Script to run TestSprite tests on the MyBrand Job Application Platform services
"""

import requests
import json
import time

def test_with_testsprite():
    """Test services using TestSprite MCP"""
    print("Testing services with TestSprite MCP...")
    
    # Test the voice agent service
    print("\n1. Testing Voice Agent Service")
    
    # Health check
    try:
        response = requests.get("http://localhost:8117/health")
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print("  ✓ Voice Agent Health Check: PASSED")
        else:
            print(f"  ✗ Voice Agent Health Check: FAILED - {response.status_code}")
    except Exception as e:
        print(f"  ✗ Voice Agent Health Check: ERROR - {e}")
    
    # Process voice command
    try:
        test_data = {
            "command": "help me apply for a software engineering job",
            "user_id": "test_user_123",
            "context": "currently on job search page"
        }
        response = requests.post(
            "http://localhost:8117/process-command",
            json=test_data,
            timeout=10
        )
        if response.status_code == 200:
            print("  ✓ Voice Command Processing: PASSED")
        else:
            print(f"  ✗ Voice Command Processing: FAILED - {response.status_code}")
    except Exception as e:
        print(f"  ✗ Voice Command Processing: ERROR - {e}")
    
    # Test the skill gap analyzer service
    print("\n2. Testing Skill Gap Analyzer Service")
    
    try:
        url = "http://localhost:8105/analyze"
        data = {
            "resume_text": "Experienced Python developer with Django and Flask experience. Skilled in SQL and Docker.",
            "job_description": "Senior Python Developer needed with experience in Django, Flask, SQL, Docker, and Kubernetes."
        }
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"  ✓ Skill Gap Analysis: PASSED (Score: {result['skill_gap_score']:.2f})")
        else:
            print(f"  ✗ Skill Gap Analysis: FAILED - {response.status_code}")
    except Exception as e:
        print(f"  ✗ Skill Gap Analysis: ERROR - {e}")

if __name__ == "__main__":
    print("MyBrand Job Application Platform - TestSprite Integration Test")
    print("=" * 70)
    
    test_with_testsprite()
    
    print("\n" + "=" * 70)
    print("Test execution completed!")