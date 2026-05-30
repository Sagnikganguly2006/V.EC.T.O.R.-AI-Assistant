import os
import io
from PIL import ImageGrab
from google import genai
from google.genai import types

class VectorVision:
    def __init__(self, senses_module):
        self.senses = senses_module
        
        # We grab the API key from your hidden .env file
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)

    def capture_screen(self):
        """Takes a lightning-fast snapshot of your primary monitor."""
        if self.senses:
            self.senses.speak("Scanning active monitor...")
            
        try:
            # Takes the screenshot
            screenshot = ImageGrab.grab()
            
            # Converts the image into raw data (bytes) in memory so we don't clog up your hard drive
            img_byte_arr = io.BytesIO()
            screenshot.save(img_byte_arr, format='JPEG', quality=75)
            img_byte_arr = img_byte_arr.getvalue()
            
            return img_byte_arr
            
        except Exception as e:
            print(f"[Optic Sensor Error]: {e}")
            return None

    def analyze_screen(self, question):
        """Takes a screenshot and asks the Heavyweight Brain to analyze it."""
        image_bytes = self.capture_screen()
        
        if not image_bytes:
            return "I am unable to access my optical sensors at this time."
            
        if self.senses:
            self.senses.speak("Processing visual data...")

        try:
            # We tell Gemini to look at the image bytes and answer your specific question
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
                    question
                ]
            )
            return response.text
            
        except Exception as e:
            print(f"[Brain Error]: {e}")
            return "I encountered an error while trying to process the visual data."