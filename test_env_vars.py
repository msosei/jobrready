#!/usr/bin/env python3
"""
Test script to verify environment variables are properly configured
"""

import os
from pathlib import Path

def check_env_file(filepath, required_vars):
    """Check if environment file exists and contains required variables"""
    if not os.path.exists(filepath):
        print(f"❌ {filepath} does not exist")
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    missing_vars = []
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ {filepath} missing variables: {missing_vars}")
        return False
    
    print(f"✅ {filepath} contains all required variables")
    return True

def main():
    """Main test function"""
    print("Testing environment variable configuration...\n")
    
    # Required environment variables for backend
    backend_required_vars = [
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY", 
        "SUPABASE_SERVICE_ROLE",
        "STRIPE_SECRET_KEY",
        "OPENAI_API_KEY"
    ]
    
    # Required environment variables for frontend
    frontend_required_vars = [
        "VITE_SUPABASE_URL",
        "VITE_SUPABASE_ANON_KEY"
    ]
    
    # Check main .env file
    env_files = [
        {"path": ".env", "vars": backend_required_vars + frontend_required_vars},
        {"path": ".env.local", "vars": backend_required_vars + frontend_required_vars},
        {"path": "config/.env", "vars": backend_required_vars + frontend_required_vars},
        {"path": "frontend/.env.development", "vars": frontend_required_vars}
    ]
    
    all_passed = True
    for env_file in env_files:
        filepath = os.path.join(os.getcwd(), env_file["path"])
        if not check_env_file(filepath, env_file["vars"]):
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("✅ All environment files are properly configured!")
        print("   Remember to replace placeholder values with actual API keys")
        print("   in .env.local or your deployment environment.")
    else:
        print("❌ Some environment files are missing required variables.")
        print("   Please check the files listed above.")
    
    return all_passed

if __name__ == "__main__":
    main()