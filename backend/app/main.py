from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx
from .job_search import JobSearchRequest, search_jobs
from .notifications import router as notifications_router

APP_URL = os.getenv("APP_URL", "http://localhost:3000")
API_URL = os.getenv("API_URL", "http://localhost:8000")

app = FastAPI(title="MyBrand Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[APP_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the notifications router
app.include_router(notifications_router)


class JobSearchQuery(BaseModel):
    query: str | None = None
    page: int = 1


@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/resume/upload")
async def resume_upload(file: UploadFile = File(...)):
    # Forward to resume parser microservice (placeholder)
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            files = {"file": (file.filename, await file.read(), file.content_type or "application/octet-stream")}
            r = await client.post("http://localhost:8101/parse", files=files)
            r.raise_for_status()
            parsed = r.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "uploaded", "parsed": parsed}


@app.post("/jobs/search")
async def jobs_search(request: JobSearchRequest):
    try:
        result = search_jobs(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ApplyRequest(BaseModel):
    job_id: str
    user_id: str


@app.post("/applications/apply")
async def applications_apply(req: ApplyRequest):
    # First tailor the application using Q microservice
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            tailor_res = await client.post("http://localhost:3000/api/ai/tailor-application", 
                json={"jobId": req.job_id, "userId": req.user_id})
            tailor_data = tailor_res.json()
    except Exception as e:
        # Fallback to basic application if tailoring fails
        tailor_data = {"tailoredResume": None, "tailoredCoverLetter": None}
    
    # Enqueue via worker API or Redis (placeholder)
    return {
        "enqueued": True, 
        "job_id": req.job_id,
        "tailored": tailor_data.get("tailoredResume") is not None
    }


class CoverLetterRequest(BaseModel):
    user_id: str
    job_id: str
    resume_json: dict | None = None
    job_description: str | None = None


@app.post("/ai/cover-letter")
async def ai_cover_letter(req: CoverLetterRequest):
    # Forward to microservice (placeholder)
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post("http://localhost:8103/generate", json=req.model_dump())
        r.raise_for_status()
        data = r.json()
    return data


@app.get("/analytics/usage")
async def analytics_usage(user_id: str):
    # Placeholder usage
    return {"user_id": user_id, "applications_sent": 12, "cover_letters_generated": 7, "ai_requests": 32}


class SubscribeRequest(BaseModel):
    user_id: str
    plan_type: str


@app.post("/billing/subscribe")
async def billing_subscribe(req: SubscribeRequest):
    # Placeholder Stripe integration
    return {"user_id": req.user_id, "plan_type": req.plan_type, "status": "created"}


