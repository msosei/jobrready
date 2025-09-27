#!/usr/bin/env python3
"""
TestSprite testing script for the MyBrand Job Application Platform frontend
"""

import requests
import json
import time
from typing import Dict, List

class FrontendTestResult:
    def __init__(self, name: str, status: str, duration: float, message: str = ""):
        self.name = name
        self.status = status  # PASS, FAIL, ERROR
        self.duration = duration
        self.message = message

def test_frontend_endpoint(endpoint: str, method: str = "GET") -> FrontendTestResult:
    """Test a specific frontend endpoint"""
    start_time = time.time()
    url = f"http://localhost:5174{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.get(url, timeout=10)  # Default to GET
        
        duration = time.time() - start_time
        
        if response.status_code == 200:
            return FrontendTestResult(f"Frontend {endpoint}", "PASS", duration, "Endpoint responded successfully")
        else:
            return FrontendTestResult(f"Frontend {endpoint}", "FAIL", duration, f"HTTP {response.status_code}: {response.text}")
    except Exception as e:
        duration = time.time() - start_time
        return FrontendTestResult(f"Frontend {endpoint}", "ERROR", duration, f"Exception: {str(e)}")

def run_frontend_tests() -> List[FrontendTestResult]:
    """Run frontend tests using TestSprite approach"""
    results = []
    print("🧪 Testing MyBrand Job Application Platform Frontend with TestSprite")
    print("=" * 70)
    
    # Test endpoints
    endpoints_to_test = [
        ("/", "GET", "Home page"),
        ("/index.html", "GET", "Index HTML file"),
        ("/index.css", "GET", "Main CSS file"),
        ("/src/main.tsx", "GET", "Main TypeScript file"),
        ("/src/App.tsx", "GET", "App component")
    ]
    
    print("Testing Frontend Endpoints")
    print("-" * 30)
    
    for endpoint, method, description in endpoints_to_test:
        result = test_frontend_endpoint(endpoint, method)
        results.append(result)
        status_icon = "✅" if result.status == "PASS" else "❌" if result.status == "FAIL" else "⚠️"
        print(f"  {status_icon} {description}: {result.status} ({result.duration:.2f}s)")
        if result.message and result.status != "PASS":
            print(f"    Message: {result.message}")
    
    return results

def generate_report(results: List[FrontendTestResult]) -> str:
    """Generate a frontend test report"""
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    errors = sum(1 for r in results if r.status == "ERROR")
    total = len(results)
    
    # Calculate total duration
    total_duration = sum(r.duration for r in results)
    
    report = "\n" + "=" * 70
    report += "\nFRONTEND TESTSPRITE TEST REPORT"
    report += "\n" + "=" * 70
    report += f"\nTotal Tests: {total}"
    report += f"\nPassed: {passed}"
    report += f"\nFailed: {failed}"
    report += f"\nErrors: {errors}"
    report += f"\nSuccess Rate: {((passed/total)*100):.1f}%"
    report += f"\nTotal Duration: {total_duration:.2f}s"
    report += "\n" + "=" * 70
    
    # Detailed results
    report += "\n\nDETAILED RESULTS:"
    report += "\n" + "-" * 40
    for result in results:
        status_icon = "✅" if result.status == "PASS" else "❌" if result.status == "FAIL" else "⚠️"
        report += f"\n{status_icon} {result.name}: {result.status} ({result.duration:.2f}s)"
        if result.message and result.status != "PASS":
            report += f"\n    Message: {result.message}"
    
    report += "\n" + "=" * 70
    return report

def main():
    """Main function to run frontend tests with TestSprite"""
    print("MyBrand Job Application Platform - Frontend TestSprite Testing")
    print("=" * 70)
    
    # Run tests
    results = run_frontend_tests()
    
    # Generate and print report
    report = generate_report(results)
    print(report)
    
    # Save report to file
    with open("frontend_testsprite_report.txt", "w") as f:
        f.write(report)
    
    print("\nDetailed report saved to 'frontend_testsprite_report.txt'")
    
    # Summary
    passed = sum(1 for r in results if r.status == "PASS")
    total = len(results)
    print(f"\n🏁 Frontend Test Execution Complete: {passed}/{total} tests passed")

if __name__ == "__main__":
    main()