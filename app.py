from flask import Flask, request, jsonify, render_template
from gemini.client import configure_genai
from gemini.models import GeminiHandler
from gemini.storage import read_history, save_history
from dotenv import load_dotenv
import os

load_dotenv()
configure_genai()

app = Flask(__name__)
gemini_handler = GeminiHandler()

@app.route("/")
def default():
    return render_template('index.html')

@app.route("/gemini")
def main():
    input_text = request.args.get("query")
    uuid = request.args.get("uid")
    
    if not input_text or not uuid:
        return jsonify({"error": "Missing query or uid parameter"}), 400
        
    try:
        response = gemini_handler.text_chat(input_text, uuid)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/gemini/vision")
def vision():
    prompt = request.args.get("query")
    media_url = request.args.get("url")
    media_type = request.args.get("type")
    
    if not all([prompt, media_url, media_type]):
        return jsonify({"error": "Missing parameters"}), 400
        
    try:
        response = gemini_handler.process_media(prompt, media_url, media_type)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/gemini/character")
def character_chat():
    input_text = request.args.get("query")
    uuid = request.args.get("uid")
    instructions = request.args.get("systemPrompt")
    
    if not all([input_text, uuid, instructions]):
        return jsonify({"error": "Missing parameters"}), 400
        
    try:
        response = gemini_handler.text_chat(
            input_text,
            uuid,
            system_instruction=instructions
        )
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)