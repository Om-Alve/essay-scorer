from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

import httpx
from generate_frameworks import generate_framework
import scorer

FRAMEWORK_CACHE: dict[str, str] = {}

app = FastAPI(title="Essay-Scorer")

client = genai.Client()


class EssayGradeRequest(BaseModel):
    essay: str
    topic: str


@app.post("/grade-essay")
def grade_essay(request: EssayGradeRequest):
    if request.topic in FRAMEWORK_CACHE.keys():
        framework = FRAMEWORK_CACHE[request.topic]
    else:
        framework = generate_framework(topic=request.topic)

    grade = scorer.grade_essay(
        topic=request.topic, essay=request.essay, framework=framework
    )

    return grade.model_dump()


@app.post("/ocr-marathi-essay")
async def ocr_marathi_essay(file: UploadFile = File(...)):
    """
    Accepts a Marathi essay PDF and extracts:
      - The essay's topic/title
      - The full essay text
    Returns JSON: {"topic": "<topic>", "essay": "<essay>"}
    """

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    try:
        pdf_bytes = await file.read()

        prompt = (
            "Read this Marathi PDF carefully. "
            "Extract and clearly identify the essay's topic/title "
            "and the full essay text. "
            "Return your answer strictly in the following JSON format:\n\n"
            "{\"topic\": \"<topic>\", \"essay\": \"<essay>\"}\n\n"
            "Do not translate to English. Keep everything in Marathi."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                prompt
            ]
        )

        text_response = response.text.strip()

        import json

        try:
            result = json.loads(text_response.replace("```json", "").replace("```", ""))
        except json.JSONDecodeError:
            result = {"topic": "अज्ञात विषय", "essay": text_response}

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")
