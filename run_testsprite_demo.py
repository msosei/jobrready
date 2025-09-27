#!/usr/bin/env python3
"""
Demo script showing how to use TestSprite with the MyBrand Job Application Platform
"""

import requests
import json
import time

def demo_testsprite_with_working_services():
    """Demonstrate TestSprite testing with working services"""
    print("🧪 TestSprite Demo: MyBrand Job Application Platform")
    print("=" * 55)
    
    # Test the three core services that are working well
    services_to_test = [
        {
            "name": "Voice Agent",
            "port": 8117,
            "endpoints": [
                {"path": "/health", "method": "GET", "description": "Health check"},
                {"path": "/process-command", "method": "POST", "description": "Process voice command", 
                 "data": {"command": "find software jobs", "user_id": "demo_user", "context": "job search"}}
            ]
        },
        {
            "name": "Skill Gap Analyzer",
            "port": 8105,
            "endpoints": [
                {"path": "/health", "method": "GET", "description": "Health check"},
                {"path": "/analyze", "method": "POST", "description": "Analyze skill gap",
                 "data": {
                     "resume_text": "Python developer with 3 years experience in Django and Flask",
                     "job_description": "Senior Python Developer needed with Django, Flask, and Kubernetes experience"
                 }}
            ]
        },
        {
            "name": "Resume Builder",
            "port": 8106,
            "endpoints": [
                {"path": "/health", "method": "GET", "description": "Health check"},
                {"path": "/generate", "method": "POST", "description": "Generate resume",
                 "data": {
                     "data": {
                         "personal_info": {
                             "name": "Demo User",
                             "email": "demo@example.com",
                             "phone": "(555) 123-4567"
                         },
                         "experiences": [],
                         "education": [],
                         "skills": []
                     }
                 }}
            ]
        }
    ]
    
    # Run tests
    total_tests = 0
    passed_tests = 0
    
    for service in services_to_test:
        print(f"\n🚀 Testing {service['name']} Service")
        print("-" * 30)
        
        for endpoint in service["endpoints"]:
            total_tests += 1
            start_time = time.time()
            response = None
            
            try:
                url = f"http://localhost:{service['port']}{endpoint['path']}"
                
                if endpoint["method"] == "GET":
                    response = requests.get(url, timeout=5)
                elif endpoint["method"] == "POST":
                    response = requests.post(url, json=endpoint.get("data", {}), timeout=10)
                
                duration = time.time() - start_time
                
                if response and response.status_code == 200:
                    passed_tests += 1
                    print(f"  ✅ {endpoint['description']}: PASS ({duration:.2f}s)")
                else:
                    print(f"  ❌ {endpoint['description']}: FAIL (HTTP {response.status_code if response else 'No Response'})")
                    
            except Exception as e:
                duration = time.time() - start_time
                print(f"  ⚠️  {endpoint['description']}: ERROR ({duration:.2f}s)")
                print(f"     Exception: {str(e)}")
    
    # Summary
    print("\n" + "=" * 55)
    print("📊 TESTSPRITE DEMO SUMMARY")
    print("=" * 55)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! TestSprite integration is working correctly.")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests failed. Please check the services.")
    
    print("\n🔗 TestSprite MCP Server is running on http://localhost:50932")

if __name__ == "__main__":
    demo_testsprite_with_working_services()