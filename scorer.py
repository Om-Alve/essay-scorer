import glob
from typing import Literal
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class Grade(BaseModel):
    grade: Literal["A", "B", "C"] = Field(description="Grade of the essay")
    feedback: list[str] = Field(description="Feedback to improve the essay")


_ = load_dotenv()
client = OpenAI(base_url="https://api.groq.com/openai/v1")

ESSAY_GRADER_PROMPT = """
You are an expert Marathi essay grader and teacher.

Your task is to evaluate a student's Marathi essay based on:
1. General writing quality:
   - Grammar and spelling accuracy
   - Vocabulary richness and appropriateness
   - Structure and coherence of ideas
   - Relevance to the topic
   - Clarity and expression of thought

2. The topic-specific framework provided (it describes what an ideal essay on this topic should include).

Assign a **grade**:
- **A** → Excellent essay: insightful, well-structured, fluent Marathi, and aligns well with the framework.
- **B** → Average essay: understandable and relevant but may have some grammatical, structural, or alignment issues.
- **C** → Below average: unclear, off-topic, or frequent grammatical mistakes.

Also provide **specific, actionable feedback points** in English.

Your response must be valid JSON strictly following this schema:
{
  "grade": "A" | "B" | "C",
  "feedback": ["point 1", "point 2", ...]
}
"""


def grade_essay(topic: str, essay: str, framework: str) -> Grade:
    """Grades a Marathi essay using the topic-specific framework."""
    try:
        resp = client.beta.chat.completions.parse(
            model="moonshotai/kimi-k2-instruct-0905",
            response_format=Grade,
            messages=[
                {"role": "system", "content": ESSAY_GRADER_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"TOPIC: {topic}\n\n"
                        f"FRAMEWORK:\n{framework}\n\n"
                        f"ESSAY:\n{essay}\n\n"
                        "Evaluate the essay using both the general criteria and the framework."
                    ),
                },
            ],
        )

        grade = resp.choices[0].message.parsed if resp.choices[0].message else None
        if not grade:
            grade = Grade(grade="C", feedback=["Could not parse grading response."])
    except Exception as e:
        print(f"Couldn't grade essay '{topic}' due to error: {e}")
        grade = Grade(grade="C", feedback=["Error occurred during grading."])
    return grade


if __name__ == "__main__":
    essay_files = glob.glob("essays/*.txt")
    for essay_file in essay_files:
        essay_file_norm = essay_file.split("/")[-1].rsplit(".", 1)[0]
        try:
            quality, topic = essay_file_norm.split("-", 1)
        except ValueError:
            print(f"Skipping malformed filename: {essay_file}")
            continue

        framework_path = f"frameworks/{topic}.txt"
        if not framework_path:
            print(f"⚠️ No framework found for topic: {topic}")
            continue

        with open(essay_file, "r", encoding="utf-8") as f:
            essay = f.read()

        with open(framework_path, "r", encoding="utf-8") as f:
            framework = f.read()

        grade = grade_essay(topic, essay, framework)
        print(f"📝 Topic: {topic} | Quality: {quality} | Grade: {grade.grade}")
        for fb in grade.feedback:
            print(f"   - {fb}")
        print("----")
