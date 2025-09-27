#!/usr/bin/env python3
"""
Comprehensive TestSprite test for the MyBrand Job Application Platform
Tests all microservices, backend, and frontend components
"""

import requests
import json
import time
from typing import Dict, List, Any, Tuple, Optional

# Service configurations
SERVICES = {
    "voice_agent": {"port": 8117, "name": "Voice Agent"},
    "skill_gap_analyzer": {"port": 8105, "name": "Skill Gap Analyzer"},
    "resume_builder": {"port": 8106, "name": "Resume Builder"},
    "resume_enhancer": {"port": 8107, "name": "Resume Enhancer"},
    "interview_coach": {"port": 8108, "name": "Interview Coach"},
    "application_filler": {"port": 8109, "name": "Application Filler"},
    "semantic_matcher": {"port": 8110, "name": "Semantic Matcher"},
    "job_recommender": {"port": 8111, "name": "Job Recommender"},
    "mock_interviewer": {"port": 8114, "name": "Mock Interviewer"},
    "diversity_insights": {"port": 8115, "name": "Diversity Insights"},
    "document_summarizer": {"port": 8116, "name": "Document Summarizer"},
    "multi_language": {"port": 8118, "name": "Multi Language"},
    "course_recommender": {"port": 8119, "name": "Course Recommender"}
}

# Test data for each service
TEST_DATA = {
    "voice_agent": {
        "process_command": {
            "command": "help me apply for a software engineering job",
            "user_id": "test_user_123",
            "context": "currently on job search page"
        }
    },
    "skill_gap_analyzer": {
        "analyze": {
            "resume_text": "Experienced Python developer with Django and Flask experience. Skilled in SQL and Docker.",
            "job_description": "Senior Python Developer needed with experience in Django, Flask, SQL, Docker, and Kubernetes."
        }
    },
    "resume_builder": {
        "generate": {
            "data": {
                "personal_info": {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "phone": "(555) 123-4567"
                },
                "experiences": [
                    {
                        "company": "TechCorp",
                        "position": "Software Engineer",
                        "start_date": "2020-01-01",
                        "description": ["Developed web applications using Python and Django"]
                    }
                ],
                "education": [
                    {
                        "institution": "University of Technology",
                        "degree": "B.S. Computer Science",
                        "field_of_study": "Computer Science",
                        "start_date": "2016-09-01",
                        "end_date": "2020-05-01"
                    }
                ],
                "skills": [
                    {"name": "Python", "level": "Advanced"},
                    {"name": "Django", "level": "Intermediate"}
                ]
            }
        }
    }
}

class TestResult:
    def __init__(self, name: str, status: str, duration: float, message: str = ""):
        self.name = name
        self.status = status  # PASS, FAIL, ERROR
        self.duration = duration
        self.message = message

def test_service_health(service_name: str, port: int) -> TestResult:
    """Test if a service is healthy"""
    start_time = time.time()
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        duration = time.time() - start_time
        
        if response.status_code == 200 and response.json().get("status") == "healthy":
            return TestResult(f"{service_name} Health Check", "PASS", duration, "Service is healthy")
        else:
            return TestResult(f"{service_name} Health Check", "FAIL", duration, f"Unexpected response: {response.status_code}")
    except Exception as e:
        duration = time.time() - start_time
        return TestResult(f"{service_name} Health Check", "ERROR", duration, f"Exception: {str(e)}")

def test_service_endpoint(service_name: str, port: int, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> TestResult:
    """Test a specific endpoint of a service"""
    start_time = time.time()
    url = f"http://localhost:{port}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            duration = time.time() - start_time
            return TestResult(f"{service_name} {endpoint}", "ERROR", duration, f"Unsupported method: {method}")
        
        duration = time.time() - start_time
        
        if response.status_code == 200:
            return TestResult(f"{service_name} {endpoint}", "PASS", duration, "Endpoint responded successfully")
        else:
            return TestResult(f"{service_name} {endpoint}", "FAIL", duration, f"HTTP {response.status_code}: {response.text}")
    except Exception as e:
        duration = time.time() - start_time
        return TestResult(f"{service_name} {endpoint}", "ERROR", duration, f"Exception: {str(e)}")

def run_comprehensive_tests() -> List[TestResult]:
    """Run comprehensive tests on all services"""
    results = []
    print("Starting comprehensive TestSprite tests...")
    print("=" * 60)
    
    # Test health checks for all services
    print("\n1. Testing Health Checks for All Services")
    print("-" * 40)
    
    for service_name, config in SERVICES.items():
        result = test_service_health(service_name, config["port"])
        results.append(result)
        status_icon = "✓" if result.status == "PASS" else "✗" if result.status == "FAIL" else "⚠"
        print(f"  {status_icon} {result.name}: {result.status} ({result.duration:.2f}s)")
        if result.message and result.status != "PASS":
            print(f"    Message: {result.message}")
    
    # Test specific endpoints for key services
    print("\n2. Testing Key Service Endpoints")
    print("-" * 40)
    
    # Test voice agent process command
    result = test_service_endpoint(
        "Voice Agent", 
        SERVICES["voice_agent"]["port"], 
        "/process-command", 
        "POST", 
        TEST_DATA["voice_agent"]["process_command"]
    )
    results.append(result)
    status_icon = "✓" if result.status == "PASS" else "✗" if result.status == "FAIL" else "⚠"
    print(f"  {status_icon} {result.name}: {result.status} ({result.duration:.2f}s)")
    
    # Test skill gap analyzer
    result = test_service_endpoint(
        "Skill Gap Analyzer", 
        SERVICES["skill_gap_analyzer"]["port"], 
        "/analyze", 
        "POST", 
        TEST_DATA["skill_gap_analyzer"]["analyze"]
    )
    results.append(result)
    status_icon = "✓" if result.status == "PASS" else "✗" if result.status == "FAIL" else "⚠"
    print(f"  {status_icon} {result.name}: {result.status} ({result.duration:.2f}s)")
    
    # Test resume builder
    result = test_service_endpoint(
        "Resume Builder", 
        SERVICES["resume_builder"]["port"], 
        "/generate", 
        "POST", 
        TEST_DATA["resume_builder"]["generate"]
    )
    results.append(result)
    status_icon = "✓" if result.status == "PASS" else "✗" if result.status == "FAIL" else "⚠"
    print(f"  {status_icon} {result.name}: {result.status} ({result.duration:.2f}s)")
    
    return results

def generate_report(results: List[TestResult]) -> str:
    """Generate a comprehensive test report"""
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    errors = sum(1 for r in results if r.status == "ERROR")
    total = len(results)
    
    # Calculate total duration
    total_duration = sum(r.duration for r in results)
    
    report = "\n" + "=" * 60
    report += "\nCOMPREHENSIVE TESTSPRITE TEST REPORT"
    report += "\n" + "=" * 60
    report += f"\nTotal Tests: {total}"
    report += f"\nPassed: {passed}"
    report += f"\nFailed: {failed}"
    report += f"\nErrors: {errors}"
    report += f"\nSuccess Rate: {((passed/total)*100):.1f}%"
    report += f"\nTotal Duration: {total_duration:.2f}s"
    report += "\n" + "=" * 60
    
    # Detailed results
    report += "\n\nDETAILED RESULTS:"
    report += "\n" + "-" * 40
    for result in results:
        status_icon = "✓" if result.status == "PASS" else "✗" if result.status == "FAIL" else "⚠"
        report += f"\n{status_icon} {result.name}: {result.status} ({result.duration:.2f}s)"
        if result.message and result.status != "PASS":
            report += f"\n    Message: {result.message}"
    
    report += "\n" + "=" * 60
    return report

def main():
    """Main function to run comprehensive TestSprite tests"""
    print("MyBrand Job Application Platform - Comprehensive TestSprite Testing")
    print("=" * 70)
    
    # Run tests
    results = run_comprehensive_tests()
    
    # Generate and print report
    report = generate_report(results)
    print(report)
    
    # Save report to file
    with open("comprehensive_testsprite_report.txt", "w") as f:
        f.write(report)
    
    print("\nDetailed report saved to 'comprehensive_testsprite_report.txt'")
    
    # Summary
    passed = sum(1 for r in results if r.status == "PASS")
    total = len(results)
    print(f"\n🏁 Test Execution Complete: {passed}/{total} tests passed")

if __name__ == "__main__":
    main()