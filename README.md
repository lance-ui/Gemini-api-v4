# Gemini API Interface

This is a Flask application that interacts with the Google Gemini API, providing endpoints for chat, image analysis, video analysis, and character interactions.

## Features

- **Chat Endpoint**: Interact with the Gemini 1.5 Flash model.
- **Image Analysis**: Analyze images using the Gemini 1.5 Pro model.
- **Video Analysis**: Process videos with the Gemini 1.5 Pro model.
- **Character Chat**: Engage with a custom personality using system prompts.

## Requirements

- Flask
- Google Generative AI SDK
- Requests
- Pillow
- python-dotenv

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/gemini-api-interface.git
   cd gemini-api-interface

2. **install the requirements**
    ```bash
    pip install -r requirements.txt
    
3. **setting environment valuebles**
    - create a '.env' file and paste the following make sure to replace with your actual API key from 
    - https://ai.google.dev/gemini-api/docs?utm_source=gfd&utm_medium=referral&utm_campaign=ai_logo_garden&utm_content
    ```bash
      GEMINI_API_KEY=your_api_key_here
      PORT=5001
  
4. **running the application**
     ```bash
      python app.py
