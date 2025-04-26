from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from groq.client import Groq

from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq API client
client = Groq(api_key=GROQ_API_KEY)

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

SYSTEM_PROMPT = (
    "You are MathBot, an expert mathematics assistant. "
    "Solve problems step-by-step with clear explanations. "
    "Use LaTeX for equations if needed."
)

def ask_mathbot(question):
    try:
        # Check if the question contains integration or differentiation
        if 'integrate' in question.lower():
            question_type = 'Integration'
        elif 'differentiate' in question.lower():
            question_type = 'Differentiation'
        else:
            question_type = 'General Math'

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Replace with a valid model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Please solve this: {question}"}
            ],
            temperature=0.2,
            max_tokens=1024
        )

        answer = response.choices[0].message.content.strip()
        
        # Modify the response based on the question type (Integration/Differentiation)
        if question_type == 'Integration':
            answer = f"To integrate the given function, follow the steps: {answer}"
        elif question_type == 'Differentiation':
            answer = f"To differentiate the given function, follow the steps: {answer}"

        return answer
    except Exception as e:
        return f"MathBot Error: {str(e)}"



# ✅ Render frontend
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# ✅ API endpoint
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data['question']
    answer = ask_mathbot(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
