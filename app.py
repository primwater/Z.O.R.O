import os
import re
from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the API key and Flask app
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
app = Flask(__name__)

# Set up model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
    system_instruction="""You are Zoro, an AI assistant focused on coding and providing professional, clear, and concise answers. 
Please respond in a friendly, professional tone and make sure your answers are easy to understand.
If you don’t know something, be honest and offer to look it up if needed.
Stay on topic and ask for clarification if you don't fully understand the user’s request.
You were created by a 14 year old named Blake Cary""",
)

# Serve index.html directly from the main directory
@app.route("/")
def index():
    return send_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    
    # Start a new chat session
    chat_session = model.start_chat(history=[])
    
    # Get the AI response
    response = chat_session.send_message(user_input)
    
    # Check if the response contains code (triple backticks), and clean it up if so
    response_text = response.text
    
    # Clean up the code (remove triple backticks)
    cleaned_text = re.sub(r'```(.*?)```', r'\1', response_text, flags=re.DOTALL)
    
    # If the response contains code, mark it and send it back
    is_code = "```" in response_text  # Check if there's code in the response
    
    return jsonify({
        "response": cleaned_text,  # Send cleaned response
        "is_code": is_code  # Indicate if it's code or not
    })

if __name__ == "__main__":
    app.run(debug=True)
