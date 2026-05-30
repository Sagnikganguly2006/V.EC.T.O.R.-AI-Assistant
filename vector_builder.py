import os
import re
from pathlib import Path
from groq import Groq

class VectorBuilder:
    def __init__(self, core_brain=None, senses_module=None):
        self.senses = senses_module
        # Automatically finds your Desktop folder
        self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # Connect to Groq using the key from your .env file
        self.api_key = os.getenv("GROQ_API_KEY")

    def clean_output(self, raw_text):
        """Removes extra formatting so the code can run perfectly."""
        text = re.sub(r"^```[a-zA-Z]*\n", "", raw_text, flags=re.MULTILINE)
        text = re.sub(r"```$", "", text, flags=re.MULTILINE)
        return text.strip()

    def save_to_desktop(self, filename, content):
        """Creates the file and saves it directly to your desktop."""
        full_path = os.path.join(self.desktop_path, filename)
        try:
            with open(full_path, "w", encoding="utf-8") as file:
                file.write(content)
            return True
        except Exception as e:
            print(f"[Save Error]: {e}")
            return False

    def build_code(self, language, file_extension, instruction):
        """Connects to Groq to write real, working code instantly."""
        ext = file_extension if file_extension.startswith(".") else f".{file_extension}"
        filename = f"vector_generated{ext}"
        
        if self.senses:
            self.senses.speak(f"Routing to Groq Heavyweight Brain. Initiating {language} development...")
            
        if not self.api_key:
            return "My Groq coding brain is offline. Please check the API key."

        try:
            client = Groq(api_key=self.api_key)
            prompt = (
                f"You are V.E.C.T.O.R., an elite AI software engineer. "
                f"Write a complete, working script in {language} for the following request: {instruction}\n"
                f"CRITICAL RULE: Output ONLY the raw code. Do not include any conversational text."
            )

            # Send the request to Groq's fast Llama model
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile", 
            )
            
            final_code = self.clean_output(response.choices[0].message.content)
            
            if self.save_to_desktop(filename, final_code):
                if self.senses:
                    self.senses.speak(f"Development complete, sir. {filename} has been saved to your desktop.")
                return f"Successfully generated and saved {language} code."
            else:
                return "I encountered an error while trying to save the file."
                
        except Exception as e:
            print(f"[Builder Error]: {e}")
            return "I encountered an error while trying to write the code."

    def plan_project(self, project_topic):
        """Connects to Groq to create a step-by-step project plan."""
        clean_topic = project_topic.replace(' ', '_').replace('/', '_')
        filename = f"{clean_topic}_Plan.txt"
        
        if self.senses:
            self.senses.speak(f"Analyzing parameters and drafting engineering workflow for {project_topic}...")
            
        if not self.api_key:
            return "My Groq planning brain is offline. Please check the API key."

        try:
            client = Groq(api_key=self.api_key)
            prompt = (
                f"You are V.E.C.T.O.R., an elite AI project manager. "
                f"Create a highly detailed, step-by-step engineering workflow and project plan for: {project_topic}. "
                f"Format it beautifully as a text document."
            )

            # Send the request to Groq
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            
            workflow = response.choices[0].message.content
            
            if self.save_to_desktop(filename, workflow):
                if self.senses:
                    self.senses.speak(f"The project workflow is ready. I have placed the blueprint on your desktop as {filename}.")
                return f"Successfully generated workflow for {project_topic}."
            else:
                return "I apologize, but I could not save the blueprint."
                
        except Exception as e:
            print(f"[Planner Error]: {e}")
            return "I encountered an error while trying to draft the plan."

    def process_build_command(self, command):
        command_lower = command.lower()
        if "python" in command_lower or ".py" in command_lower:
            self.build_code("Python", ".py", command)
        elif "c++" in command_lower or ".cpp" in command_lower:
            self.build_code("C++", ".cpp", command)
        elif " c " in command_lower or ".c" in command_lower:
            self.build_code("C", ".c", command)
        elif "plan" in command_lower or "workflow" in command_lower:
            self.plan_project("New_Engineering_Project")