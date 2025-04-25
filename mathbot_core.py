import os
import wolframalpha
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
wolfram_client = wolframalpha.Client(os.getenv("WOLFRAM_APP_ID"))

MATHBOT_SYSTEM_PROMPT = """
You are MathBot, an expert mathematics assistant. Follow these rules:
1. Solve problems step-by-step with clear explanations
2. Use LaTeX formatting for equations ($...$ delimiters)
3. For verification, cross-check with Wolfram Alpha when needed
4. Format responses in Markdown
"""

def get_mathbot_response(user_input):
    # First try Groq
    groq_response = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": MATHBOT_SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        temperature=0.3,
        max_tokens=1024
    )

    # If verification needed, consult Wolfram Alpha
    if "verify" in user_input.lower():
        try:
            wolfram_res = wolfram_client.query(user_input)
            wolfram_answer = next(wolfram_res.results).text
            return f"{groq_response.choices[0].message.content}\n\n**Wolfram Verification:**\n{wolfram_answer}"
        except:
            return groq_response.choices[0].message.content + "\n\n(Wolfram verification failed)"

    return groq_response.choices[0].message.content
