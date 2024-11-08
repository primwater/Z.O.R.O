import os
from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the API key and Flask app
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
app = Flask(__name__)

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model with instructions for Zoro
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
    system_instruction="""You are Zoro, an AI assistant focused on coding, providing clear answers.
If you include code, wrap it in triple backticks (```).
Only respond with code when the user specifies, and keep your tone helpful and direct.
If you don’t know something, admit it, and stay on topic.""",
)

# Serve the main page
@app.route("/")
def index():
    return send_file("index.html")

# Chat route to handle the conversation
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_input)

    # Format the response to highlight code blocks and add a "Copy Code" button
    formatted_response = format_code_response(response.text)
    
    return jsonify({"response": formatted_response})

# Function to detect and format code sections
def format_code_response(response_text):
    # Split text on code markers, adding styling and the "Copy Code" button
    if "```" in response_text:
        parts = response_text.split("```")
        formatted = ""
        for i, part in enumerate(parts):
            if i % 2 == 1:  # Inside a code block
                language = part.split("\n", 1)[0]
                code = part[len(language):].strip()
                formatted += f'<div class="code-block"><span class="language">{language}</span>' \
                             f'<pre><code>{code}</code></pre>' \
                             '<button onclick="copyCode(this)">Copy Code</button></div>'
            else:
                formatted += f"<p>{part}</p>"
        return formatted
    else:
        return f"<p>{response_text}</p>"

if __name__ == "__main__":
    app.run(debug=True)
