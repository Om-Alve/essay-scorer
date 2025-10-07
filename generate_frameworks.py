import time
from openai import OpenAI
from dotenv import load_dotenv
from generate_essays import essay_topics

_ = load_dotenv()

client = OpenAI(base_url="https://api.groq.com/openai/v1")

FRAMEWORK_GENERATION_PROMPT = """
You are an expert Marathi teacher and essay evaluator.

Your task is to take an essay topic as input and generate a *framework* for grading essays on that topic.

A *framework* means:
- A structured outline of the key points, ideas, or arguments that a good essay on this topic should include.
- Criteria to evaluate language, grammar, structure, creativity, and content relevance.
- A short example structure (e.g., Introduction, Body, Conclusion) customized for the topic.

Output format:
1. **Overview of the Topic**
2. **Key Points or Subtopics**
3. **Language and Expression Guidelines**
4. **Cultural or Moral Insights (if applicable)**
5. **Evaluation Criteria**

Generate the framework in **Marathi**.
"""


def generate_framework(topic: str) -> str:
    try:
        resp = client.chat.completions.create(
            messages=[
                {"role": "system", "content": FRAMEWORK_GENERATION_PROMPT},
                {"role": "user", "content": f"TOPIC: {topic}"},
            ],
            model="moonshotai/kimi-k2-instruct-0905",
        )
        framework = resp.choices[0].message.content
        if not framework:
            framework = "Couldn't generate a framework."
    except Exception as e:
        framework = f"Couldn't generate a framework."
        print(f"Couldn't generate a framework due to error: {e}")
    return framework


def main():
    for topic in essay_topics:
        framework = generate_framework(topic)
        with open(f"frameworks/{topic}.txt", "w") as f:
            _ = f.write(framework)
        time.sleep(0.5)
        print(f"Framework generated for topic: {topic}")


if __name__ == "__main__":
    main()
