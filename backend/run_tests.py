"""
Test runner script for the MyBrand backend
"""

import subprocess
import sys
import os

def run_tests():
    """Run the test suite"""
    try:
        # Run pytest with coverage
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests",
            "--cov=app",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--verbose",
            "-v"
        ], cwd=os.path.dirname(__file__))
        
        return result.returncode == 0
    except FileNotFoundError:
        print("Error: pytest not found. Please install test dependencies:")
        print("pip install pytest pytest-asyncio pytest-cov httpx respx")
        return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def run_tests_without_coverage():
    """Run the test suite without coverage"""
    try:
        # Run pytest without coverage
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests",
            "--verbose",
            "-v"
        ], cwd=os.path.dirname(__file__))
        
        return result.returncode == 0
    except FileNotFoundError:
        print("Error: pytest not found. Please install test dependencies:")
        print("pip install pytest pytest-asyncio pytest-cov httpx respx")
        return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    print("MyBrand Backend Test Runner")
    print("=" * 40)
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Running in virtual environment")
    else:
        print("Warning: Not running in virtual environment")
    
    # Try to run tests with coverage first
    print("\nRunning tests with coverage...")
    success = run_tests()
    
    if not success:
        print("\nTrying to run tests without coverage...")
        success = run_tests_without_coverage()
    
    if success:
        print("\nAll tests completed successfully!")
        sys.exit(0)
    else:
        print("\nSome tests failed!")
        sys.exit(1)