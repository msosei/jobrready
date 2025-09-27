import requests
import json

# Test data
resume_text = """
John Doe
Software Engineer
Email: john.doe@example.com
Phone: (555) 123-4567

SUMMARY
Experienced software engineer with 5 years of experience in web development, 
specializing in Python and JavaScript. Strong problem-solving skills and 
ability to work in agile environments.

EXPERIENCE
Senior Software Engineer | TechCorp Inc. | Jan 2020 - Present
- Developed RESTful APIs using Python Flask and Django
- Implemented frontend features using React and Redux
- Collaborated with cross-functional teams to deliver high-quality software
- Mentored junior developers and conducted code reviews

Software Engineer | StartupXYZ | Jun 2018 - Dec 2019
- Built full-stack web applications using Node.js and Express
- Created responsive UI components with Vue.js
- Optimized database queries for better performance
- Participated in Agile ceremonies and sprint planning

EDUCATION
B.S. in Computer Science | University of Technology | 2014-2018

SKILLS
Python, JavaScript, React, Node.js, SQL, Git, Docker, AWS
"""

job_description = """
Senior Data Scientist
Company: DataFlow Analytics
Location: Remote

We are looking for a Senior Data Scientist to join our team. In this role, 
you will be responsible for building machine learning models, analyzing 
large datasets, and deriving actionable insights for our clients.

RESPONSIBILITIES
- Design and implement machine learning models
- Analyze large datasets to identify patterns and trends
- Collaborate with engineering teams to deploy models to production
- Create data visualizations and reports for stakeholders
- Stay up-to-date with the latest advancements in data science

REQUIREMENTS
- PhD or Masters in Data Science, Statistics, or related field
- 5+ years of experience in data science
- Proficiency in Python and R
- Experience with machine learning frameworks (TensorFlow, PyTorch)
- Strong knowledge of SQL and data visualization tools
- Experience with cloud platforms (AWS, GCP, Azure)
- Familiarity with big data technologies (Spark, Hadoop)
"""

# Make the request
url = "http://localhost:8105/analyze"
data = {
    "resume_text": resume_text,
    "job_description": job_description
}

try:
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        print("Skill Gap Analysis Results:")
        print(json.dumps(result, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error making request: {e}")