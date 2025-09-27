import requests
import json
import time

# Base URLs for services
SERVICES = {
    "skill_gap_analyzer": "http://localhost:8105",
    "resume_builder": "http://localhost:8106",
    "resume_enhancer": "http://localhost:8107",
    "interview_coach": "http://localhost:8108",
    "application_filler": "http://localhost:8109",
    "semantic_matcher": "http://localhost:8110",
    "job_recommender": "http://localhost:8111"
}

def test_skill_gap_analyzer():
    print("Testing Skill Gap Analyzer...")
    url = f"{SERVICES['skill_gap_analyzer']}/analyze"
    
    data = {
        "resume_text": "Experienced Python developer with Django and Flask experience. Skilled in SQL and Docker.",
        "job_description": "Senior Python Developer needed with experience in Django, Flask, SQL, Docker, and Kubernetes."
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"  ✓ Success - Skill gap score: {result['skill_gap_score']:.2f}")
            return True
        else:
            print(f"  ✗ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        return False

def test_resume_builder():
    print("Testing Resume Builder...")
    url = f"{SERVICES['resume_builder']}/generate"
    
    data = {
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
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print("  ✓ Success - Resume generated")
            return True
        else:
            print(f"  ✗ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        return False

def test_resume_enhancer():
    print("Testing Resume Enhancer...")
    url = f"{SERVICES['resume_enhancer']}/enhance"
    
    data = {
        "resume_text": "John Doe\nSoftware Engineer\nExperience:\n- Developed applications\nEducation:\n- B.S. Computer Science"
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"  ✓ Success - ATS score: {result['ats_score']:.2f}")
            return True
        else:
            print(f"  ✗ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        return False

def test_interview_coach():
    print("Testing Interview Coach...")
    url = f"{SERVICES['interview_coach']}/generate-questions"
    
    data = {
        "resume_text": "Python developer with 3 years experience in Django and Flask",
        "job_description": "Senior Python Developer position requiring Django and Flask expertise",
        "question_types": ["technical", "behavioral"]
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"  ✓ Success - Generated {len(result['questions'])} questions")
            return True
        else:
            print(f"  ✗ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        return False

def test_application_filler():
    print("Testing Application Filler...")
    url = f"{SERVICES['application_filler']}/auto-fill"
    
    data = {
        "resume_text": "John Doe\nEmail: john.doe@example.com\nPhone: (555) 123-4567\nExperience: Python Developer at TechCorp",
        "form_fields": [
            {"name": "name", "label": "Full Name", "type": "text", "required": True},
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "phone", "label": "Phone", "type": "phone", "required": False}
        ]
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"  ✓ Success - Filled {len(result['filled_data'])} fields")
            return True
        else:
            print(f"  ✗ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        return False

def test_semantic_matcher():
    print("Testing Semantic Matcher...")
    url = f"{SERVICES['semantic_matcher']}/match"
    
    data = {
        "candidate": {
            "skills": ["Python", "Django", "SQL"],
            "experience": ["Web development", "Database design"],
            "education": ["B.S. Computer Science"],
            "career_goals": ["Senior Developer"],
            "preferred_locations": ["Remote"],
            "job_types": ["Full-time"]
        },
        "jobs": [
            {
                "id": "1",
                "title": "Python Developer",
                "company": "TechCorp",
                "description": "Develop web applications using Python and Django",
                "requirements": ["Python", "Django", "SQL"],
                "location": "Remote",
                "type": "Full-time"
            }
        ]
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"  ✓ Success - Found {len(result['matches'])} matches")
            return True
        else:
            print(f"  ✗ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        return False

def test_job_recommender():
    print("Testing Job Recommender...")
    url = f"{SERVICES['job_recommender']}/recommend"
    
    data = {
        "user_id": "user123",
        "career_trajectory": {
            "current_role": "Software Engineer",
            "years_experience": 3,
            "skills": ["Python", "Django", "SQL"],
            "career_goals": ["Senior Developer"],
            "past_roles": []
        },
        "preferences": {
            "preferred_roles": ["Developer", "Engineer"],
            "preferred_industries": ["Technology"],
            "preferred_locations": ["Remote"],
            "job_types": ["Full-time"],
            "experience_level": "mid"
        },
        "activity_history": [],
        "job_pool": [
            {
                "id": "1",
                "title": "Senior Python Developer",
                "company": "TechCorp",
                "location": "Remote",
                "type": "Full-time",
                "description": "Lead development of web applications",
                "requirements": ["Python", "Django", "Leadership"],
                "posted_date": "2023-01-01",
                "is_remote": True,
                "industry": "Technology",
                "experience_level": "senior"
            }
        ]
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"  ✓ Success - Generated {len(result['recommendations'])} recommendations")
            return True
        else:
            print(f"  ✗ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        return False

def main():
    print("Testing all AI microservices...\n")
    
    # Test each service
    tests = [
        test_skill_gap_analyzer,
        test_resume_builder,
        test_resume_enhancer,
        test_interview_coach,
        test_application_filler,
        test_semantic_matcher,
        test_job_recommender
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            # Small delay between tests
            time.sleep(1)
        except Exception as e:
            print(f"Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"❌ {total - passed} tests failed")
    
    return passed == total

if __name__ == "__main__":
    main()