from fastapi import HTTPException
from typing import List, Optional
from pydantic import BaseModel
import json

class Job(BaseModel):
    id: int
    title: str
    company: str
    location: str
    salary: Optional[str] = None
    type: str
    remote: bool
    urgent: bool
    description: str
    requirements: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    posted: str
    isNew: bool

class JobSearchRequest(BaseModel):
    keyword: Optional[str] = None
    location: Optional[str] = None
    jobType: Optional[str] = None
    company: Optional[str] = None
    remote: Optional[bool] = None
    limit: Optional[int] = 20
    offset: Optional[int] = 0

class JobSearchResponse(BaseModel):
    jobs: List[Job]
    total: int
    hasMore: bool

# Sample job data (in a real application, this would come from a database)
sample_jobs = [
    Job(
        id=1,
        title="Senior Software Engineer",
        company="TechCorp Inc.",
        location="San Francisco, CA",
        salary="$120k - $160k",
        type="Full-time",
        remote=True,
        urgent=False,
        description="Join our team to build scalable web applications using React, Node.js, and cloud technologies. You will work on exciting projects that impact millions of users.",
        requirements=[
            "5+ years of software development experience",
            "Proficiency in React and Node.js",
            "Experience with cloud platforms",
            "Strong problem-solving skills"
        ],
        benefits=[
            "Health insurance",
            "Stock options",
            "Remote work",
            "Unlimited PTO"
        ],
        posted="2 days ago",
        isNew=True
    ),
    Job(
        id=2,
        title="Data Scientist",
        company="DataFlow Analytics",
        location="Remote",
        salary="$110k - $140k",
        type="Full-time",
        remote=True,
        urgent=True,
        description="Work with machine learning models and big data to derive actionable insights for our clients. You will be responsible for building predictive models and data pipelines.",
        requirements=[
            "PhD or Masters in Data Science/Statistics",
            "Experience with Python and R",
            "Machine learning expertise",
            "SQL proficiency"
        ],
        benefits=[
            "Flexible hours",
            "Learning budget",
            "Health benefits",
            "Work from anywhere"
        ],
        posted="1 day ago",
        isNew=True
    ),
    Job(
        id=3,
        title="UX Designer",
        company="Design Studio",
        location="New York, NY",
        salary="$80k - $110k",
        type="Full-time",
        remote=False,
        urgent=False,
        description="Create beautiful and intuitive user experiences for our digital products. You will work closely with product managers and developers to bring designs to life.",
        requirements=[
            "3+ years of UX design experience",
            "Proficiency in Figma and Sketch",
            "User research skills",
            "Portfolio of design work"
        ],
        benefits=[
            "Creative environment",
            "Design tools budget",
            "Health insurance",
            "Professional development"
        ],
        posted="3 days ago",
        isNew=True
    )
]

def search_jobs(request: JobSearchRequest) -> JobSearchResponse:
    # Filter jobs based on search criteria
    filtered_jobs = sample_jobs.copy()
    
    if request.keyword:
        keyword = request.keyword.lower()
        filtered_jobs = [
            job for job in filtered_jobs
            if (keyword in job.title.lower() or 
                keyword in job.company.lower() or 
                keyword in job.description.lower())
        ]
    
    if request.location:
        location = request.location.lower()
        filtered_jobs = [
            job for job in filtered_jobs
            if location in job.location.lower()
        ]
    
    if request.jobType:
        filtered_jobs = [
            job for job in filtered_jobs
            if job.type.lower() == request.jobType.lower()
        ]
    
    if request.company:
        company = request.company.lower()
        filtered_jobs = [
            job for job in filtered_jobs
            if company in job.company.lower()
        ]
    
    if request.remote is not None:
        filtered_jobs = [
            job for job in filtered_jobs
            if job.remote == request.remote
        ]
    
    # Calculate total and pagination
    total = len(filtered_jobs)
    
    # Handle optional offset and limit with default values
    offset = request.offset or 0
    limit = request.limit or 20
    
    hasMore = offset + limit < total
    
    # Apply pagination
    paginated_jobs = filtered_jobs[offset:offset + limit]
    
    return JobSearchResponse(
        jobs=paginated_jobs,
        total=total,
        hasMore=hasMore
    )