from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Job Matcher")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MatchRequest(BaseModel):
  resume_json: dict
  jobs: list[dict]

@app.post('/match')
async def match(req: MatchRequest):
  # Dummy scoring: higher score if title contains 'Engineer'
  ranked = [
    { **j, 'score': (100 if 'Engineer' in j.get('title','') else 50) }
    for j in req.jobs
  ]
  ranked.sort(key=lambda x: x['score'], reverse=True)
  return { 'ranked': ranked }


