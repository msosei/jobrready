from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Cover Letter Generator")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
  user_id: str
  job_id: str
  resume_json: dict | None = None
  job_description: str | None = None

@app.post('/generate')
async def generate(req: GenerateRequest):
  # Placeholder response
  text = f"Dear Hiring Manager, I am excited to apply for job {req.job_id}. My experience aligns..."
  return {"cover_letter": text}


