from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client inside function to avoid startup errors
_client = None

def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is not set. "
                "Please configure it in your Render dashboard under Environment variables."
            )
        _client = genai.Client(api_key=api_key)
    return _client

def generate_image(text, save_path):
    """
    Generate an image using Gemini's 'gemini-2.0-flash-preview-image-generation' model
    and save it to `save_path`. Returns the saved image path if successful, else None.
    """
    client = _get_client()
    prompt = (f"Hi, can you create a professional 3D-styled image for a PowerPoint presentation "
              f"on the topic: {text}. Do not include the text in the image. Generate an image which is similar to that. It can be technology or whatever niche the text belongs to, but keep it relevant. Do not write anything on the image")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(f"[INFO] Text response: {part.text}")
            elif part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                image.save(save_path)
                return save_path

        print("[WARN] No image data found in response.")
        return None

    except Exception as e:
        print(f"[ERROR] Image generation failed: {e}")
        return None
