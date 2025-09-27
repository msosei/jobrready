#!/usr/bin/env python3
"""
TestSprite Backend Testing Script
Tests the backend service including additional endpoints
"""

import os
import sys
import time
import subprocess
import requests
import threading
from typing import Dict, List, Any
from dotenv import load_dotenv

class TestSpriteBackendTester:
    """TestSprite implementation for backend testing"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv(os.path.join(os.getcwd(), "backend", ".env"))
        
        self.backend_url = "http://localhost:8000"
        self.test_results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": []
        }
        self.backend_process = None
    
    def start_backend_service(self) -> bool:
        """Start the backend service"""
        try:
            print("🔧 Starting backend service...")
            
            # Change to backend directory
            backend_dir = os.path.join(os.getcwd(), "backend")
            
            # Start backend in a separate process
            print("🚀 Launching backend service...")
            self.backend_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "app.main:app", 
                "--host", "0.0.0.0", 
                "--port", "8000"
            ], cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for service to start
            time.sleep(3)
            
            # Check if service is running
            try:
                response = requests.get(f"{self.backend_url}/health", timeout=5)
                if response.status_code == 200:
                    print("✅ Backend service started successfully")
                    return True
                else:
                    print("❌ Backend service failed to start")
                    # Print error output
                    stdout, stderr = self.backend_process.communicate(timeout=1)
                    print(f"Backend stdout: {stdout.decode()}")
                    print(f"Backend stderr: {stderr.decode()}")
                    return False
            except Exception as e:
                print(f"❌ Backend service health check failed: {str(e)}")
                # Print error output
                try:
                    stdout, stderr = self.backend_process.communicate(timeout=1)
                    print(f"Backend stdout: {stdout.decode()}")
                    print(f"Backend stderr: {stderr.decode()}")
                except:
                    pass
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend service: {str(e)}")
            return False
    
    def stop_backend_service(self):
        """Stop the backend service"""
        try:
            if self.backend_process:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
            print("🛑 Backend service stopped")
        except Exception as e:
            print(f"⚠️  Warning when stopping backend: {str(e)}")
    
    def test_health_endpoint(self) -> bool:
        """Test the health check endpoint"""
        self.test_results["total_tests"] += 1
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200 and response.json().get("status") == "healthy":
                print("✅ Health endpoint test passed")
                self.test_results["passed"] += 1
                return True
            else:
                print("❌ Health endpoint test failed")
                self.test_results["failed"] += 1
                return False
        except Exception as e:
            error_msg = f"Health endpoint test error: {str(e)}"
            print(f"❌ {error_msg}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(error_msg)
            return False
    
    def test_root_endpoint(self) -> bool:
        """Test the root endpoint"""
        self.test_results["total_tests"] += 1
        try:
            response = requests.get(self.backend_url, timeout=5)
            if response.status_code == 200 and "message" in response.json():
                print("✅ Root endpoint test passed")
                self.test_results["passed"] += 1
                return True
            else:
                print("❌ Root endpoint test failed")
                self.test_results["failed"] += 1
                return False
        except Exception as e:
            error_msg = f"Root endpoint test error: {str(e)}"
            print(f"❌ {error_msg}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(error_msg)
            return False
    
    def test_notification_endpoint(self) -> bool:
        """Test the notification endpoint"""
        self.test_results["total_tests"] += 1
        try:
            # Test sending a notification
            response = requests.post(
                f"{self.backend_url}/notifications/send",
                json={
                    "user_id": "test_user",
                    "notification_type": "test",
                    "title": "Test Notification",
                    "message": "This is a test notification"
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("success") is True:
                    print("✅ Notification endpoint test passed")
                    self.test_results["passed"] += 1
                    return True
                else:
                    print("❌ Notification endpoint test failed: unexpected response")
                    self.test_results["failed"] += 1
                    return False
            else:
                print(f"❌ Notification endpoint test failed with status {response.status_code}")
                self.test_results["failed"] += 1
                return False
        except Exception as e:
            error_msg = f"Notification endpoint test error: {str(e)}"
            print(f"❌ {error_msg}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(error_msg)
            return False
    
    def test_skill_gap_endpoint(self) -> bool:
        """Test the skill gap analysis endpoint"""
        self.test_results["total_tests"] += 1
        try:
            # Test skill gap analysis (should return 503 since microservice is not running)
            response = requests.post(
                f"{self.backend_url}/ai/skill-gap/analyze",
                json={
                    "resume_text": "Python, JavaScript, React",
                    "job_description": "Python, Django, FastAPI"
                },
                timeout=10
            )
            # We expect either 200 (if service is mocked) or 503 (service unavailable)
            if response.status_code in [200, 503]:
                print("✅ Skill gap endpoint test passed")
                self.test_results["passed"] += 1
                return True
            else:
                print(f"❌ Skill gap endpoint test failed with status {response.status_code}")
                self.test_results["failed"] += 1
                return False
        except Exception as e:
            error_msg = f"Skill gap endpoint test error: {str(e)}"
            print(f"❌ {error_msg}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(error_msg)
            return False
    
    def test_job_matcher_endpoint(self) -> bool:
        """Test the job matcher endpoint"""
        self.test_results["total_tests"] += 1
        try:
            # Test job matcher (should return 503 since microservice is not running)
            response = requests.post(
                f"{self.backend_url}/ai/job-matcher/match",
                json={
                    "candidate": {
                        "skills": ["Python", "JavaScript"],
                        "experience": ["3 years"],
                        "education": ["BSc Computer Science"],
                        "career_goals": ["Senior Developer"],
                        "preferred_locations": ["Remote"],
                        "job_types": ["Full-time"]
                    },
                    "jobs": []
                },
                timeout=10
            )
            # We expect either 200 (if service is mocked) or 503 (service unavailable)
            if response.status_code in [200, 503]:
                print("✅ Job matcher endpoint test passed")
                self.test_results["passed"] += 1
                return True
            else:
                print(f"❌ Job matcher endpoint test failed with status {response.status_code}")
                self.test_results["failed"] += 1
                return False
        except Exception as e:
            error_msg = f"Job matcher endpoint test error: {str(e)}"
            print(f"❌ {error_msg}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(error_msg)
            return False
    
    def test_cors_preflight(self) -> bool:
        """Test CORS preflight OPTIONS request"""
        self.test_results["total_tests"] += 1
        try:
            # Test CORS preflight request
            response = requests.options(
                f"{self.backend_url}/health",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "GET",
                    "Access-Control-Request-Headers": "X-Requested-With"
                },
                timeout=5
            )
            # Check if CORS headers are present in the response
            cors_headers = [
                'access-control-allow-origin',
                'access-control-allow-methods',
                'access-control-allow-headers'
            ]
            has_cors_headers = all(header in response.headers for header in cors_headers)
            
            if response.status_code == 200 and has_cors_headers:
                print("✅ CORS preflight test passed")
                self.test_results["passed"] += 1
                return True
            else:
                print(f"❌ CORS preflight test failed with status {response.status_code}")
                if not has_cors_headers:
                    missing = [h for h in cors_headers if h not in response.headers]
                    print(f"   Missing CORS headers: {missing}")
                self.test_results["failed"] += 1
                return False
        except Exception as e:
            error_msg = f"CORS preflight test error: {str(e)}"
            print(f"❌ {error_msg}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(error_msg)
            return False
    
    def test_environment_variables(self) -> bool:
        """Test that environment variables are properly loaded"""
        self.test_results["total_tests"] += 1
        try:
            # Check if required environment variables are set
            required_vars = ["SUPABASE_URL", "SUPABASE_ANON_KEY"]
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            
            if not missing_vars:
                print("✅ Environment variables test passed")
                self.test_results["passed"] += 1
                return True
            else:
                print(f"❌ Environment variables test failed: missing {missing_vars}")
                self.test_results["failed"] += 1
                return False
        except Exception as e:
            error_msg = f"Environment variables test error: {str(e)}"
            print(f"❌ {error_msg}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(error_msg)
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all backend tests"""
        print("🧪 Starting Extended TestSprite Backend Testing")
        print("=" * 50)
        
        # Start backend service
        if not self.start_backend_service():
            print("❌ Failed to start backend service. Cannot run tests.")
            return self.test_results
        
        try:
            # Run individual tests
            self.test_health_endpoint()
            self.test_root_endpoint()
            self.test_notification_endpoint()
            self.test_skill_gap_endpoint()
            self.test_job_matcher_endpoint()
            self.test_cors_preflight()
            self.test_environment_variables()
            
        finally:
            # Stop backend service
            self.stop_backend_service()
        
        return self.test_results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a test report"""
        report = []
        report.append("TestSprite Extended Backend Testing Report")
        report.append("=" * 45)
        report.append(f"Total Tests: {results['total_tests']}")
        report.append(f"Passed: {results['passed']}")
        report.append(f"Failed: {results['failed']}")
        
        if results['total_tests'] > 0:
            success_rate = (results['passed'] / results['total_tests']) * 100
            report.append(f"Success Rate: {success_rate:.1f}%")
        
        if results['errors']:
            report.append("\nErrors:")
            for error in results['errors']:
                report.append(f"  - {error}")
        
        return "\n".join(report)

def main():
    """Main function to run the TestSprite backend tests"""
    tester = TestSpriteBackendTester()
    results = tester.run_all_tests()
    report = tester.generate_report(results)
    
    print("\n" + "=" * 50)
    print(report)
    
    # Save report to file
    with open("backend_testsprite_report.txt", "w") as f:
        f.write(report)
    
    print(f"\n📋 Detailed report saved to backend_testsprite_report.txt")
    
    # Return exit code based on test results
    if results['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()