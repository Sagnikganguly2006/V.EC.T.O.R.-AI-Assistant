import os
import pywhatkit
from ddgs import DDGS
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai

class VectorWeb:
    def __init__(self, senses_module):
        self.senses = senses_module
        
        # We grab the API key from your hidden .env file
        self.api_key = os.getenv("GEMINI_API_KEY")

    def _gemini_search(self, query):
        """Primary Search: Uses Google's native Search engine through the AI."""
        client = genai.Client(api_key=self.api_key)
        
        # By adding {"google_search": {}}, we give the AI live internet access
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query,
            config={"tools": [{"google_search": {}}]},
        )
        
        text = ""
        for part in response.candidates[0].content.parts:
            if hasattr(part, "text") and part.text:
                text += part.text
                
        if not text.strip():
            raise ValueError("The AI returned an empty response.")
            
        return text.strip()

    def _ddg_fallback(self, query):
        """Backup Search: Grabs a detailed list of top results if the AI is busy."""
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=4):
                results.append(r)
        
        if not results:
            return "I could not find any clear answers on the web."
            
        lines = [f"Here are the top results for '{query}':"]
        for r in results:
            if r.get("body"):
                lines.append(f"• {r['body']}")
                
        return "\n".join(lines)

    def search_web(self, query):
        """The master search function that controls both methods."""
        if self.senses:
            self.senses.speak(f"Searching the global network for: {query}")
            
        try:
            # 1. Try the highly advanced AI web search first
            if self.api_key:
                print("[V.E.C.T.O.R. System Log]: Attempting advanced AI web search...")
                return self._gemini_search(query)
        except Exception as e:
            print(f"[V.E.C.T.O.R. System Log]: AI search encountered an issue. Switching to backup... ({e})")
            
        try:
            # 2. If it fails, instantly use the backup list
            return self._ddg_fallback(query)
        except Exception:
            return "My web search modules are currently experiencing an error."

    def play_youtube_video(self, video_topic):
        """Finds and immediately plays a video on your screen."""
        if self.senses:
            self.senses.speak(f"Pulling up a YouTube video about {video_topic} right now.")
            
        pywhatkit.playonyt(video_topic)
        return "Video playback started."

    def summarize_video(self, video_id):
        """Reads the hidden subtitles of a video to tell you what it is about."""
        if self.senses:
            self.senses.speak("Extracting the video transcript. Please wait...")
        
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join([piece['text'] for piece in transcript_list])
            
            short_summary = full_text[:300] + "..."
            return f"Here is a summary of the video: {short_summary}"
            
        except Exception:
            return "I am sorry, but this video does not have readable subtitles."

    def process_web_command(self, command):
        """The traffic cop for text commands (kept safe for backwards compatibility)."""
        command_lower = command.lower()
        
        if "play" in command_lower and "youtube" in command_lower:
            topic = command_lower.replace("play youtube", "").strip()
            self.play_youtube_video(topic)
            
        elif "summarize video" in command_lower:
            result = self.summarize_video("dQw4w9WgXcQ") 
            if self.senses:
                self.senses.speak(result)
                
        elif "search" in command_lower or "what is" in command_lower or "who is" in command_lower:
            result = self.search_web(command)
            if self.senses:
                self.senses.speak(result)