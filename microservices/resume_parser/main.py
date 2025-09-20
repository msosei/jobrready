from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Resume Parser")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/parse')
async def parse(file: UploadFile = File(...)):
    # Placeholder: return dummy parsed content
    contents = await file.read()
    return {
        'skills': ['JavaScript', 'Python', 'React'],
        'experience': [{'company': 'Acme', 'role': 'Engineer'}],
        'education': [{'school': 'University', 'degree': 'BS'}],
        'bytes': len(contents),
    }


