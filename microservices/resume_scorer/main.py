from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Resume Scorer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScoreRequest(BaseModel):
  resume_json: dict
  job_description: str

@app.post('/score')
async def score(req: ScoreRequest):
  # Dummy score implementation
  score = 80 if 'Engineer' in req.job_description else 60
  suggestions = ["Add quantified achievements", "Include relevant keywords"]
  return {"score": score, "suggestions": suggestions}


