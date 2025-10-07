import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
from fastapi.middleware.cors import CORSMiddleware
import json

from generate_frameworks import generate_framework
import scorer

FRAMEWORK_CACHE: dict[str, str] = {}

app = FastAPI(title="Essay-Scorer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client()


class EssayGradeRequest(BaseModel):
    essay: str
    topic: str


@app.post("/grade-essay")
async def grade_essay(request: EssayGradeRequest):
    """Grade essay efficiently with cached frameworks."""
    topic = request.topic

    if topic in FRAMEWORK_CACHE:
        framework = FRAMEWORK_CACHE[topic]
    else:
        framework = await asyncio.to_thread(generate_framework, topic=topic)
        FRAMEWORK_CACHE[topic] = framework

    grade = await asyncio.to_thread(
        scorer.grade_essay,
        topic=topic,
        essay=request.essay,
        framework=framework,
    )

    return grade.model_dump()


@app.post("/ocr-marathi-essay")
async def ocr_marathi_essay(file: UploadFile = File(...)):
    """Extract Marathi essay topic and content from a PDF."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    pdf_bytes = await file.read()

    prompt = (
        "Read this Marathi PDF carefully. "
        "Extract and clearly identify the essay's topic/title "
        "and the full essay text. "
        "Return your answer strictly in the following JSON format:\n\n"
        '{"topic": "<topic>", "essay": "<essay>"}\n\n'
        "Do not translate to English. Keep everything in Marathi."
    )

    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                prompt,
            ],
        )

        text_response = response.text.strip()

        try:
            result = json.loads(text_response.replace("```json", "").replace("```", ""))
        except json.JSONDecodeError:
            result = {"topic": "अज्ञात विषय", "essay": text_response}

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")
