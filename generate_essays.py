from typing import Literal
from openai import OpenAI
from dotenv import load_dotenv

_ = load_dotenv()

PROMPT = """
You are a student. Write an essay in Marathi on the given topic.  
The essay quality should be **{quality}**, where the possible values are:

- **poor** → Simple sentences, limited vocabulary, and basic grammar. The essay may have some spelling or grammatical mistakes and minimal structure.
- **moderate** → Fairly structured essay with understandable flow. Uses common Marathi vocabulary and mostly correct grammar, with a few minor errors.
- **good** → Well-organized and coherent essay with rich vocabulary, correct grammar, and clear expression of ideas. Demonstrates good understanding of the topic.

Ensure the tone, vocabulary, and overall writing style match the specified quality level.
"""

client = OpenAI(base_url="https://api.groq.com/openai/v1")

essay_topics = [
    "माझे आवडते पुस्तक",
    "माझा आदर्श व्यक्ती",
    "शिक्षकांचे महत्व",
    "माझे गाव",
    "पर्यावरण संवर्धन",
    "माझे शाळेचे जीवन",
    "संगणकाचे महत्व",
    "भारताची संस्कृती",
    "माझा आवडता खेळ",
    "पाणी वाचवा, जीवन वाचवा",
    "इंटरनेटचे फायदे व तोटे",
    "स्त्री शिक्षणाचे महत्व",
    "माझा सर्वोत्तम मित्र",
    "माझे स्वप्नातील भारत",
    "स्वच्छ भारत अभियान",
    "मोबाईलचा वापर – वरदान की शाप",
    "विज्ञान आणि मानव जीवन",
    "आई – एक प्रेरणा",
    "वेळेचे महत्व",
    "प्रदूषण – कारणे व उपाय",
]


def get_essay_from_topic(
    topic: str, quality: Literal["poor", "moderate", "good"]
) -> str:
    try:
        resp = client.chat.completions.create(
            messages=[
                {"role": "system", "content": PROMPT.format(quality=quality)},
                {"role": "user", "content": f"TOPIC: {topic}"},
            ],
            model="moonshotai/kimi-k2-instruct-0905",
        )
        essay = resp.choices[0].message.content
        if not essay:
            essay = "Couldn't generate an essay."
    except Exception as e:
        essay = "Couldn't generate an essay."
        print(f"Couldn't generate an essay due to error: {e}")
    return essay


if __name__ == "__main__":
    for topic in essay_topics:
        for quality in ["poor", "moderate", "good"]:
            essay = get_essay_from_topic(essay_topics[0], quality)
            with open(f"essays/{quality}-{topic}.txt", "w") as f:
                _ = f.write(essay)
            print(f"Wrote a {quality} quality essay for the topic {topic}")
