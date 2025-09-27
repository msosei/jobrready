"""
Market Salary Predictor Service
Version: 1.0
Purpose: AI microservice to predict fair salary for roles based on location, experience, and market data

This microservice provides functionality to:
1. Predict salaries for job roles based on multiple factors
2. Provide market data for specific locations
3. Analyze current job market trends
4. Offer insights on salary influencing factors
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for the application
# ============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import random

# ============================================================================
# APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata
# ============================================================================

app = FastAPI(
    title="Market Salary Predictor",
    description="AI microservice to predict fair salary for roles based on location, experience, and market data",
    version="1.0.0"
)

# ============================================================================
# DATA MODELS
# Pydantic models for data validation and serialization
# ============================================================================

# ----------------------------------------------------------------------------
# SALARY PREDICTION MODELS
# Models for salary prediction requests and responses
# ----------------------------------------------------------------------------

class SalaryRequest(BaseModel):
    """Request model for salary prediction"""
    job_title: str
    location: str
    experience_years: int
    education_level: str  # "High School", "Bachelor", "Master", "PhD"
    skills: List[str]
    company_size: Optional[str] = None  # "Small", "Medium", "Large"
    industry: Optional[str] = None

class SalaryResponse(BaseModel):
    """Response model for salary prediction results"""
    predicted_salary: Dict[str, Any]  # min, max, median
    salary_range: str
    percentile: str
    factors: List[str]
    market_data: Dict[str, Any]

# ----------------------------------------------------------------------------
# LOCATION DATA MODELS
# Models for location-specific market data requests and responses
# ----------------------------------------------------------------------------

class LocationDataRequest(BaseModel):
    """Request model for location data"""
    location: str

class LocationDataResponse(BaseModel):
    """Response model for location data"""
    cost_of_living_index: float
    average_salary: float
    job_market_competition: str  # "Low", "Medium", "High"

# ----------------------------------------------------------------------------
# MARKET TRENDS MODELS
# Models for market trends and trending roles
# ----------------------------------------------------------------------------

class TrendingRole(BaseModel):
    """Model for trending job roles"""
    title: str
    growth_rate: float
    average_salary: float
    demand_level: str  # "Low", "Medium", "High"

class MarketTrendsResponse(BaseModel):
    """Response model for market trends"""
    trending_roles: List[TrendingRole]
    overall_market_health: str  # "Declining", "Stable", "Growing"
    insights: List[str]

# ============================================================================
# MARKET DATA
# Predefined market data for salary calculations and predictions
# ============================================================================

# ----------------------------------------------------------------------------
# SALARY DATA BY ROLE AND EXPERIENCE
# Comprehensive salary data organized by job title and experience level
# ----------------------------------------------------------------------------

# Salary data by role and experience level (simplified for demo)
salary_data = {
    "software engineer": {
        "0-2": {"min": 60000, "median": 80000, "max": 110000},
        "3-5": {"min": 85000, "median": 110000, "max": 140000},
        "6-10": {"min": 110000, "median": 140000, "max": 180000},
        "10+": {"min": 140000, "median": 180000, "max": 250000}
    },
    "data scientist": {
        "0-2": {"min": 70000, "median": 90000, "max": 120000},
        "3-5": {"min": 95000, "median": 120000, "max": 160000},
        "6-10": {"min": 125000, "median": 160000, "max": 200000},
        "10+": {"min": 160000, "median": 200000, "max": 300000}
    },
    "product manager": {
        "0-2": {"min": 75000, "median": 95000, "max": 130000},
        "3-5": {"min": 100000, "median": 130000, "max": 170000},
        "6-10": {"min": 135000, "median": 170000, "max": 220000},
        "10+": {"min": 175000, "median": 220000, "max": 300000}
    },
    "ux designer": {
        "0-2": {"min": 55000, "median": 70000, "max": 90000},
        "3-5": {"min": 75000, "median": 90000, "max": 120000},
        "6-10": {"min": 95000, "median": 120000, "max": 150000},
        "10+": {"min": 125000, "median": 150000, "max": 200000}
    },
    "marketing manager": {
        "0-2": {"min": 50000, "median": 60000, "max": 80000},
        "3-5": {"min": 65000, "median": 80000, "max": 100000},
        "6-10": {"min": 85000, "median": 100000, "max": 130000},
        "10+": {"min": 110000, "median": 130000, "max": 180000}
    }
}

# ----------------------------------------------------------------------------
# LOCATION-SPECIFIC DATA
# Market data organized by location including cost of living and competition
# ----------------------------------------------------------------------------

# Location data (simplified for demo)
location_data = {
    "san francisco": {"cost_of_living": 1.6, "avg_salary_multiplier": 1.4, "competition": "High"},
    "new york": {"cost_of_living": 1.5, "avg_salary_multiplier": 1.3, "competition": "High"},
    "seattle": {"cost_of_living": 1.4, "avg_salary_multiplier": 1.2, "competition": "High"},
    "austin": {"cost_of_living": 1.2, "avg_salary_multiplier": 1.1, "competition": "Medium"},
    "denver": {"cost_of_living": 1.1, "avg_salary_multiplier": 1.0, "competition": "Medium"},
    "atlanta": {"cost_of_living": 1.0, "avg_salary_multiplier": 0.9, "competition": "Medium"},
    "remote": {"cost_of_living": 1.0, "avg_salary_multiplier": 1.0, "competition": "High"}
}

# ----------------------------------------------------------------------------
# EDUCATION AND SKILL MULTIPLIERS
# Premium multipliers for education levels and in-demand skills
# ----------------------------------------------------------------------------

# Education multipliers
education_multipliers = {
    "High School": 1.0,
    "Bachelor": 1.2,
    "Master": 1.4,
    "PhD": 1.6
}

# Skill premium multipliers
skill_premiums = {
    "python": 1.1,
    "machine learning": 1.3,
    "cloud computing": 1.25,
    "cybersecurity": 1.35,
    "data analysis": 1.2,
    "project management": 1.15,
    "leadership": 1.2,
    "agile": 1.1,
    "devops": 1.3,
    "kubernetes": 1.35
}

# ============================================================================
# CORE FUNCTIONS
# Main functions for salary calculations and market analysis
# ============================================================================

# ----------------------------------------------------------------------------
# EXPERIENCE LEVEL DETERMINATION
# Function to categorize years of experience into experience levels
# ----------------------------------------------------------------------------

def get_experience_level(years: int) -> str:
    """
    Convert years of experience to experience level category
    
    Args:
        years (int): Years of professional experience
        
    Returns:
        str: Experience level category ("0-2", "3-5", "6-10", "10+")
    """
    if years <= 2:
        return "0-2"
    elif years <= 5:
        return "3-5"
    elif years <= 10:
        return "6-10"
    else:
        return "10+"

# ----------------------------------------------------------------------------
# SALARY CALCULATION
# Function to calculate predicted salary based on multiple factors
# ----------------------------------------------------------------------------

def calculate_salary(job_title: str, location: str, experience_years: int, 
                    education_level: str, skills: List[str], company_size: Optional[str] = None) -> Dict[str, Any]:
    """
    Calculate predicted salary based on inputs
    
    Args:
        job_title (str): Job title for salary prediction
        location (str): Geographic location
        experience_years (int): Years of professional experience
        education_level (str): Education level ("High School", "Bachelor", "Master", "PhD")
        skills (List[str]): List of skills
        company_size (Optional[str]): Size of company ("Small", "Medium", "Large")
        
    Returns:
        Dict[str, Any]: Dictionary with min, median, and max salary values
    """
    # Normalize job title for matching
    normalized_title = job_title.lower().strip()
    
    # Get base salary data for the job title
    if normalized_title not in salary_data:
        # Try to find a similar title if exact match not found
        for title in salary_data.keys():
            if title in normalized_title or normalized_title in title:
                normalized_title = title
                break
        else:
            # Default to software engineer if no match found
            normalized_title = "software engineer"
    
    # Determine experience level category
    experience_level = get_experience_level(experience_years)
    base_salary = salary_data[normalized_title][experience_level]
    
    # Apply location multiplier based on geographic market
    location_key = location.lower().strip()
    if location_key not in location_data:
        # Try to find a similar location if exact match not found
        for loc in location_data.keys():
            if loc in location_key or location_key in loc:
                location_key = loc
                break
        else:
            # Default to remote if no match found
            location_key = "remote"
    
    location_info = location_data[location_key]
    location_multiplier = location_info["avg_salary_multiplier"]
    
    # Apply education multiplier based on educational attainment
    education_multiplier = education_multipliers.get(education_level, 1.0)
    
    # Apply skill premium multipliers for in-demand skills
    skill_multiplier = 1.0
    for skill in skills:
        skill_lower = skill.lower()
        if skill_lower in skill_premiums:
            skill_multiplier += (skill_premiums[skill_lower] - 1.0) * 0.5  # Partial premium
    
    # Apply company size adjustment (simplified)
    company_multiplier = 1.0
    if company_size == "Large":
        company_multiplier = 1.1
    elif company_size == "Small":
        company_multiplier = 0.9
    
    # Calculate final salary range with all multipliers applied
    final_min = base_salary["min"] * location_multiplier * education_multiplier * skill_multiplier * company_multiplier
    final_median = base_salary["median"] * location_multiplier * education_multiplier * skill_multiplier * company_multiplier
    final_max = base_salary["max"] * location_multiplier * education_multiplier * skill_multiplier * company_multiplier
    
    return {
        "min": round(final_min, -3),  # Round to nearest thousand
        "median": round(final_median, -3),
        "max": round(final_max, -3)
    }

# ----------------------------------------------------------------------------
# PERCENTILE DETERMINATION
# Function to determine where a salary falls within a range
# ----------------------------------------------------------------------------

def determine_percentile(salary: float, min_sal: float, max_sal: float) -> str:
    """
    Determine where a salary falls in the range
    
    Args:
        salary (float): Salary value to evaluate
        min_sal (float): Minimum salary in range
        max_sal (float): Maximum salary in range
        
    Returns:
        str: Percentile category ("Entry Level", "Market Rate", "Above Market")
    """
    if max_sal == min_sal:
        return "Median"
    
    percentile = (salary - min_sal) / (max_sal - min_sal) * 100
    
    if percentile < 25:
        return "Entry Level"
    elif percentile < 75:
        return "Market Rate"
    else:
        return "Above Market"

# ----------------------------------------------------------------------------
# SALARY FACTOR ANALYSIS
# Function to identify factors that influence salary predictions
# ----------------------------------------------------------------------------

def get_salary_factors(job_title: str, location: str, experience_years: int, 
                      education_level: str, skills: List[str]) -> List[str]:
    """
    Get factors that influence the salary prediction
    
    Args:
        job_title (str): Job title for salary prediction
        location (str): Geographic location
        experience_years (int): Years of professional experience
        education_level (str): Education level
        skills (List[str]): List of skills
        
    Returns:
        List[str]: List of factors that influence the salary
    """
    factors = []
    
    # Experience factor analysis
    if experience_years < 2:
        factors.append("Entry-level position - potential for growth")
    elif experience_years > 10:
        factors.append("Senior-level experience - higher compensation expected")
    
    # Education factor analysis
    if education_level in ["Master", "PhD"]:
        factors.append(f"{education_level} degree - premium compensation")
    
    # Skill factors analysis
    high_value_skills = [skill for skill in skills if skill.lower() in ["machine learning", "cloud computing", "cybersecurity", "devops", "kubernetes"]]
    if high_value_skills:
        factors.append(f"High-value skills: {', '.join(high_value_skills)}")
    
    # Location factor analysis
    location_key = location.lower().strip()
    if location_key in location_data:
        competition = location_data[location_key]["competition"]
        if competition == "High":
            factors.append("Competitive market location")
        elif competition == "Low":
            factors.append("Lower competition location")
    
    return factors

# ============================================================================
# API ENDPOINTS
# HTTP endpoints for the salary predictor service
# ============================================================================

# ----------------------------------------------------------------------------
# HEALTH CHECK ENDPOINT
# Endpoint for checking service health status
# ----------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring service status
    
    Returns:
        dict: Health status information
    """
    return {"status": "healthy"}

# ----------------------------------------------------------------------------
# SALARY PREDICTION ENDPOINT
# Endpoint for predicting salaries based on job and candidate information
# ----------------------------------------------------------------------------

@app.post("/predict", response_model=SalaryResponse)
async def predict_salary(request: SalaryRequest):
    """
    Predict salary for a given role based on various factors
    
    Args:
        request (SalaryRequest): Request containing job and candidate information
        
    Returns:
        SalaryResponse: Predicted salary range and influencing factors
        
    Example:
        POST /predict
        {
            "job_title": "Software Engineer",
            "location": "San Francisco",
            "experience_years": 5,
            "education_level": "Bachelor",
            "skills": ["Python", "Machine Learning"],
            "company_size": "Large"
        }
    """
    try:
        # Calculate predicted salary using all provided factors
        predicted_salary = calculate_salary(
            request.job_title,
            request.location,
            request.experience_years,
            request.education_level,
            request.skills,
            request.company_size
        )
        
        # Determine where the median salary falls in the range
        median_salary = predicted_salary["median"]
        percentile = determine_percentile(
            median_salary, 
            predicted_salary["min"], 
            predicted_salary["max"]
        )
        
        # Format salary range as a readable string
        salary_range = f"${predicted_salary['min']:,} - ${predicted_salary['max']:,}"
        
        # Get factors that influence the salary prediction
        factors = get_salary_factors(
            request.job_title,
            request.location,
            request.experience_years,
            request.education_level,
            request.skills
        )
        
        # Generate additional market data for context
        market_data = {
            "location_competition": location_data.get(request.location.lower(), {}).get("competition", "Unknown"),
            "cost_of_living_factor": location_data.get(request.location.lower(), {}).get("cost_of_living", 1.0),
            "national_average": salary_data.get("software engineer", {}).get("6-10", {}).get("median", 140000)
        }
        
        # Return the complete salary prediction response
        return SalaryResponse(
            predicted_salary=predicted_salary,
            salary_range=salary_range,
            percentile=percentile,
            factors=factors,
            market_data=market_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting salary: {str(e)}")

# ----------------------------------------------------------------------------
# LOCATION DATA ENDPOINT
# Endpoint for retrieving market data for specific locations
# ----------------------------------------------------------------------------

@app.post("/location-data", response_model=LocationDataResponse)
async def get_location_data(request: LocationDataRequest):
    """
    Get market data for a specific location
    
    Args:
        request (LocationDataRequest): Request containing location name
        
    Returns:
        LocationDataResponse: Market data for the specified location
        
    Example:
        POST /location-data
        {
            "location": "San Francisco"
        }
    """
    try:
        # Normalize location key for matching
        location_key = request.location.lower().strip()
        if location_key not in location_data:
            # Try to find a similar location if exact match not found
            for loc in location_data.keys():
                if loc in location_key or location_key in loc:
                    location_key = loc
                    break
            else:
                raise HTTPException(status_code=404, detail="Location not found")
        
        # Retrieve location data
        loc_data = location_data[location_key]
        
        # Return formatted location data response
        return LocationDataResponse(
            cost_of_living_index=loc_data["cost_of_living"],
            average_salary=loc_data["avg_salary_multiplier"] * 100000,  # Base on $100k
            job_market_competition=loc_data["competition"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting location data: {str(e)}")

# ----------------------------------------------------------------------------
# MARKET TRENDS ENDPOINT
# Endpoint for retrieving current job market trends
# ----------------------------------------------------------------------------

@app.get("/market-trends", response_model=MarketTrendsResponse)
async def get_market_trends():
    """
    Get current job market trends
    
    Returns:
        MarketTrendsResponse: Current trending roles and market insights
    """
    try:
        # Generate trending roles with growth rates and salary data
        trending_roles = [
            TrendingRole(
                title="AI/Machine Learning Engineer",
                growth_rate=25.0,
                average_salary=145000,
                demand_level="High"
            ),
            TrendingRole(
                title="Cybersecurity Specialist",
                growth_rate=20.5,
                average_salary=130000,
                demand_level="High"
            ),
            TrendingRole(
                title="Cloud Architect",
                growth_rate=18.0,
                average_salary=150000,
                demand_level="High"
            ),
            TrendingRole(
                title="Data Engineer",
                growth_rate=17.5,
                average_salary=135000,
                demand_level="High"
            ),
            TrendingRole(
                title="DevOps Engineer",
                growth_rate=16.0,
                average_salary=125000,
                demand_level="High"
            )
        ]
        
        # Randomly determine market health for demonstration
        market_health_options = ["Declining", "Stable", "Growing"]
        market_health = random.choice(market_health_options)
        
        # Generate market insights based on current trends
        insights = [
            "Tech roles continue to show strong demand across most regions",
            "Remote work options have expanded the talent pool for employers",
            "Salary growth has stabilized after rapid increases in previous years",
            "Skills in AI, cloud computing, and cybersecurity command premium salaries",
            "Entry-level positions are increasingly competitive due to talent surplus"
        ]
        
        # Return complete market trends response
        return MarketTrendsResponse(
            trending_roles=trending_roles,
            overall_market_health=market_health,
            insights=insights
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting market trends: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8113)