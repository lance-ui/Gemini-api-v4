from google.generativeai import GenerativeModel
from PIL import Image
import requests
import os
import time
from storage import read_history, save_history

class GeminiHandler:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model = GenerativeModel(model_name)
        
    def text_chat(self, input_text, uid, chat_history=None, system_instruction=None):
        history = read_history(uid, 'character' if system_instruction else 'default')
        history.append({"role": "user", "parts": [input_text]})
        
        model = self.model
        if system_instruction:
            model = GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction
            )
            
        chat = model.start_chat(history=history)
        response = chat.send_message(input_text)
        response_text = response.text.replace("\n", " ")
        
        history.append({"role": "model", "parts": [response_text]})
        save_history(uid, history, 'character' if system_instruction else 'default')
        return response_text

    def process_media(self, prompt, media_url, media_type):
        try:
            if media_type == 'image':
                return self._process_image(prompt, media_url)
            elif media_type == 'video':
                return self._process_video(prompt, media_url)
            else:
                return "Unsupported media type"
        except Exception as e:
            return str(e)

    def _process_image(self, prompt, image_url):
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        model = GenerativeModel("gemini-pro-vision")
        response = model.generate_content([prompt, image])
        return response.text

    def _process_video(self, prompt, video_url):
        response = requests.get(video_url)
        video_content = BytesIO(response.content)
        
        temp_path = "temp_video.mp4"
        with open(temp_path, "wb") as f:
            f.write(video_content.getbuffer())
            
        try:
            model = GenerativeModel("gemini-pro-vision")
            video_file = genai.upload_file(path=temp_path)
            
            while video_file.state.name == "PROCESSING":
                time.sleep(1)
                video_file = genai.get_file(name=video_file.name)
                
            if video_file.state.name == "FAILED":
                return "Video processing failed"
                
            response = model.generate_content([video_file, prompt], request_options={"timeout": 900})
            return response.text
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if video_file:
                genai.delete_file(video_file.name)