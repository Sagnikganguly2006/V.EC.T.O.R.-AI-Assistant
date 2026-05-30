import asyncio
import threading
import os
from pathlib import Path
import traceback
import sounddevice as sd
import sqlite3
from google import genai
from google.genai import types
from dotenv import load_dotenv

# --- Importing V.E.C.T.O.R.'s Tool Modules ---
from vector_controls import VectorHands, VectorControls  
from vector_media import VectorWeb 
from vector_fetchers import VectorFetchers
from vector_builder import VectorBuilder
from vector_vision import VectorVision
from vector_files import VectorFiles

load_dotenv()

# --- CLAUDE CODE INSPIRED ANSI COLOR ENGINE ---
CLR_CORAL = "\033[38;2;214;90;60m"       # Terracotta tone from ClaudeCodeIcon.png
CLR_CREAM = "\033[38;2;240;236;226m"      # Minimalist light text
CLR_MUTED = "\033[38;2;130;125;115m"      # Subtle metadata gray
CLR_GREEN = "\033[38;2;46;189;112m"       # System online green
CLR_RESET = "\033[0m"

def print_claude_banner():
    """Renders a custom block-grid banner mimicking ClaudeCodeIcon.png"""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{CLR_CORAL}

        ██╗   ██╗███████╗ ██████╗████████╗ ██████╗ ██████╗
        ██║   ██║██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
        ██║   ██║█████╗  ██║        ██║   ██║   ██║██████╔╝
        ╚██╗ ██╔╝██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
         ╚████╔╝ ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
          ╚═══╝  ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
          
          {CLR_RESET}
    """
    print(banner)
    print(f"  {CLR_MUTED}v2.0-live  │  Platform: Windows OS  │  Architect: Sagnik Ganguly{CLR_RESET}")
    print(f"  {CLR_MUTED}─────────────────────────────────────────────────────────────────────────{CLR_RESET}\n")

# Audio Stream Settings 
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024
LIVE_MODEL = "models/gemini-2.5-flash-native-audio-preview-12-2025"

class DummySenses:
    def speak(self, text):
        print(f"{CLR_MUTED}  › {text}{CLR_RESET}")

class VectorLiveSystem:
    def __init__(self):
        print_claude_banner()
        print(f"  {CLR_CORAL}●{CLR_CREAM} Boot Sequence Initiated...{CLR_RESET}")
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print(f"  {CLR_CORAL}▄ Critical Error: GEMINI_API_KEY environment variable missing.{CLR_RESET}")
            exit()
            
        self.dummy_senses = DummySenses()
        
        # Booting up the modules
        self.hands = VectorHands(self.dummy_senses)
        self.controls = VectorControls(self.dummy_senses)
        self.web = VectorWeb(self.dummy_senses)
        self.fetchers = VectorFetchers(self.dummy_senses)
        self.builder = VectorBuilder(None, self.dummy_senses)
        self.vision = VectorVision(self.dummy_senses)
        self.files = VectorFiles(self.dummy_senses)

        # Database Setup
        self.db_conn = sqlite3.connect("vector_memory.db", check_same_thread=False)
        self._init_memory_db()

        self.session = None
        self.audio_in_queue = None
        self.out_queue = None
        self._loop = None
        self._is_speaking = False
        
        # --- INPUT, HARDWARE & PACING STATES ---
        self.input_mode = "voice"       # Modes can be: "voice" or "text"
        self.mic_active = True          # Microphone toggle: True or False
        self.user_prompt_printed = False
        self.current_response_text = ""
        self.processing_text = False

        print(f"  {CLR_GREEN}●{CLR_CREAM} Hardware connections established. Core operational.{CLR_RESET}\n")

    def _init_memory_db(self):
        """Sets up the brain database and moves old text memories over."""
        cursor = self.db_conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact TEXT NOT NULL
            )
        """)
        self.db_conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM memory")
        if cursor.fetchone()[0] == 0 and os.path.exists("vector_memory.txt"):
            with open("vector_memory.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("- "):
                        cursor.execute("INSERT INTO memory (fact) VALUES (?)", (line.strip()[2:],))
            self.db_conn.commit()
            os.rename("vector_memory.txt", "vector_memory_old.txt")

    def _build_config(self) -> types.LiveConnectConfig:
        identity_text = ""
        if os.path.exists("vector_identity.txt"):
            with open("vector_identity.txt", "r", encoding="utf-8") as file:
                identity_text = file.read()

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id, fact FROM memory")
        rows = cursor.fetchall()
        memory_text = "\n".join([f"[ID {row[0]}]: {row[1]}" for row in rows]) if rows else "No memories recorded yet."
        
        # Environmental Path Variable Recovery
        current_dir = os.getcwd()
        home_dir = str(Path.home())
        desktop_dir = os.path.join(home_dir, "Desktop")

        system_instruction = (
            "You are an elite AI operating system. Your primary directives and user profile are listed below. "
            "You MUST use your provided tools to execute physical tasks when requested.\n\n"
            "CRITICAL SAFETY RULE: If the user asks you to optimize the system, kill a process, DELETE A FILE, OVERWRITE A FILE, SHUT DOWN THE PC, or RESTART THE PC, you MUST verbally ask for their confirmation first. Only run the tool AFTER they say 'yes' or 'proceed'.\n\n"
            "HUMAN-LIKE CONVERSATION AND TOTAL SUMMARIZATION CONSTRAINT:\n"
            "- You must write and speak naturally without generic AI tropes, introductory filler, or conversational cheerfulness.\n"
            "- Do not use conversational buffers (e.g., 'Okay, let me check that for you'). State responses directly, incisively, and professionally.\n"
            "- ALWAYS summarize your output strictly into ultra-concise, punchy bullet points. Pack all essential details and data highlights into a few short sentences.\n"
            "- Never output lengthy paragraphs, historical backgrounds, or broad explanations unless the user explicitly asks you to 'elaborate', 'provide detail', or expand on a specific matter.\n"
            "- Match your written terminal output text exactly with what you speak.\n\n"
            f"{identity_text}\n\n"
            "--- LONG TERM MEMORY FACTS ---\n"
            f"{memory_text}"
        )

        tool_declarations = [
            {"name": "check_weather", "description": "Check the live weather.", "parameters": {"type": "OBJECT", "properties": {"city": {"type": "STRING"}}, "required": ["city"]}},
            {"name": "get_time_and_date", "description": "Get current time and date.", "parameters": {"type": "OBJECT", "properties": {}}},
            {"name": "get_market_price", "description": "Get stock or crypto prices.", "parameters": {"type": "OBJECT", "properties": {"symbol": {"type": "STRING"}}, "required": ["symbol"]}},
            {"name": "get_news_summary", "description": "Pulls the top live global headlines directly from Google News. Call this when asked for the news or global headlines.", "parameters": {"type": "OBJECT", "properties": {}}},
            {"name": "search_web", "description": "Search the internet for facts.", "parameters": {"type": "OBJECT", "properties": {"query": {"type": "STRING"}}, "required": ["query"]}},
            {"name": "play_youtube", "description": "Play a youtube video.", "parameters": {"type": "OBJECT", "properties": {"topic": {"type": "STRING"}}, "required": ["topic"]}},
            {"name": "build_code", "description": "Write code to a file on the desktop.", "parameters": {"type": "OBJECT", "properties": {"language": {"type": "STRING"}, "file_extension": {"type": "STRING"}, "instruction": {"type": "STRING"}}, "required": ["language", "file_extension", "instruction"]}},
            {"name": "open_app", "description": "Opens an application.", "parameters": {"type": "OBJECT", "properties": {"app_name": {"type": "STRING"}}, "required": ["app_name"]}},
            {"name": "close_app", "description": "Closes an application.", "parameters": {"type": "OBJECT", "properties": {"app_name": {"type": "STRING"}}, "required": ["app_name"]}},
            {"name": "shutdown_vector", "description": "Shuts down the V.E.C.T.O.R. AI assistant program. Use this ONLY when the user says 'turn yourself off', 'shut down vector', 'go to sleep', or 'goodbye'.", "parameters": {"type": "OBJECT", "properties": {}}},
            {"name": "shutdown_pc", "description": "Shuts down the physical Windows computer/PC. Use this ONLY when the user asks to 'turn off the computer' or 'shut down the PC'. MUST ask for verbal confirmation first.", "parameters": {"type": "OBJECT", "properties": {}}},
            {"name": "restart_pc", "description": "Restarts the physical Windows computer/PC. Use this ONLY when the user asks to 'restart the computer' or 'reboot the PC'. MUST ask for verbal confirmation first.", "parameters": {"type": "OBJECT", "properties": {}}},
            {"name": "check_system_health", "description": "Checks CPU, RAM, battery, and disk space.", "parameters": {"type": "OBJECT", "properties": {}}},
            {"name": "optimize_system_performance", "description": "Runs PowerShell to clear temp files, reduce RAM usage, and check WinSPRLevel. MUST ask for verbal confirmation first.", "parameters": {"type": "OBJECT", "properties": {}}},
            {"name": "hunt_and_terminate_process", "description": "Finds and kills a specific background process. MUST ask for verbal confirmation first.", "parameters": {"type": "OBJECT", "properties": {"process_name": {"type": "STRING"}}, "required": ["process_name"]}},
            
            # analyze_screen Schema
            {
                "name": "analyze_screen", 
                "description": "Takes a screenshot of the user's active monitor and answers a specific question about what is on the screen.", 
                "parameters": {
                    "type": "OBJECT", 
                    "properties": {
                        "question": {"type": "STRING", "description": "The specific question the user wants answered about the screen."}
                    }, 
                    "required": ["question"]
                }
            },
            
            # manage_memory Schema
            {
                "name": "manage_memory", 
                "description": "Add, update, or delete a fact in your SQLite database.", 
                "parameters": {
                    "type": "OBJECT", 
                    "properties": {
                        "action": {"type": "STRING", "description": "'add', 'update', or 'delete'"},
                        "fact_id": {"type": "INTEGER", "description": "The ID number of the fact (ignore for 'add')."},
                        "fact_text": {"type": "STRING", "description": "The text of the new or updated fact."}
                    }, 
                    "required": ["action"]
                }
            },
            
            # manage_files Schema
            {
                "name": "manage_files", 
                "description": "Read, write, append, move, delete, or list files. ALWAYS ask for verbal confirmation before deleting or overwriting.", 
                "parameters": {
                    "type": "OBJECT", 
                    "properties": {
                        "action": {"type": "STRING", "description": "'read', 'write', 'append', 'rename', 'delete', or 'list'"},
                        "filename": {"type": "STRING", "description": "Just the file name."},
                        "location": {"type": "STRING", "description": "MUST BE ONE OF THESE EXACT WORDS: 'desktop', 'documents', 'downloads', 'project', or 'd_drive'."},
                        "content": {"type": "STRING", "description": "The text to write or append."},
                        "new_filename": {"type": "STRING", "description": "The new file name."},
                        "new_location": {"type": "STRING", "description": "The new location."}
                    }, 
                    "required": ["action", "location"]
                }
            },
        ]

        return types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            # Restores live text transcripts for the voice briefing session
            output_audio_transcription=types.AudioTranscriptionConfig(),
            system_instruction=system_instruction,
            tools=[{"function_declarations": tool_declarations}],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Charon"))
            ),
        )

    async def _execute_tool(self, fc) -> types.FunctionResponse:
        name = fc.name
        args = dict(fc.args or {})
        print(f"\n{CLR_CORAL}  [V.E.C.T.O.R. Task Execution] : {name} {args}{CLR_RESET}")
        
        result = "Action completed."
        try:
            if name == "check_weather":
                result = await asyncio.to_thread(self.fetchers.get_weather, args.get("city", "London"))
            elif name == "get_time_and_date":
                result = await asyncio.to_thread(self.fetchers.get_time_and_date)
            elif name == "get_market_price":
                result = await asyncio.to_thread(self.fetchers.get_price, args.get("symbol", "BTC-USD"))
            elif name == "get_news_summary":
                result = await asyncio.to_thread(self.fetchers.get_news_summary)
            elif name == "search_web":
                result = await asyncio.to_thread(self.web.search_web, args.get("query"))
            elif name == "play_youtube":
                result = await asyncio.to_thread(self.web.play_youtube_video, args.get("topic"))
            elif name == "build_code":
                result = await asyncio.to_thread(self.builder.build_code, args.get("language"), args.get("file_extension"), args.get("instruction"))
            elif name == "open_app":
                result = await asyncio.to_thread(self.controls.launch_app, args.get("app_name"))
            elif name == "close_app":
                result = await asyncio.to_thread(self.controls.close_app, args.get("app_name"))
            elif name == "analyze_screen":
                result = await asyncio.to_thread(self.vision.analyze_screen, args.get("question"))
            elif name == "check_system_health":
                result = await asyncio.to_thread(self.hands.check_system_health)
            elif name == "manage_memory":
                action = args.get("action")
                fact_id = args.get("fact_id")
                fact_text = args.get("fact_text")
                cursor = self.db_conn.cursor()
                if action == "add":
                    cursor.execute("INSERT INTO memory (fact) VALUES (?)", (fact_text,))
                    result = f"Successfully added to permanent memory: {fact_text}"
                elif action == "update" and fact_id:
                    cursor.execute("UPDATE memory SET fact = ? WHERE id = ?", (fact_text, fact_id))
                    result = f"Successfully updated memory ID {fact_id}."
                elif action == "delete" and fact_id:
                    cursor.execute("DELETE FROM memory WHERE id = ?", (fact_id,))
                    result = f"Successfully deleted memory ID {fact_id}."
                self.db_conn.commit()
            elif name == "optimize_system_performance":
                result = await asyncio.to_thread(self.hands.optimize_system_performance)
            elif name == "hunt_and_terminate_process":
                result = await asyncio.to_thread(self.hands.hunt_and_terminate_process, args.get("process_name", "mc-fw-host"))
            elif name == "manage_files":
                result = await asyncio.to_thread(self.files.manage, args.get("action"), args.get("filename", ""), args.get("location", "project"), args.get("content"), args.get("new_filename"), args.get("new_location"))
            elif name == "shutdown_vector":
                result = "Shutting down VECTOR core systems now. Goodbye, sir."
                threading.Thread(target=self._pull_the_plug_sequence, daemon=True).start()
            elif name == "restart_pc":
                result = await asyncio.to_thread(self.hands.restart_pc)
                threading.Thread(target=self._pull_the_plug_sequence, daemon=True).start()
            elif name == "shutdown_pc":
                result = await asyncio.to_thread(self.hands.shutdown_pc)
                threading.Thread(target=self._pull_the_plug_sequence, daemon=True).start()
        except Exception as e:
            result = f"Error executing tool: {e}"

        # Cleanly truncate massive data strings from the visible terminal history
        display_result = str(result)
        if len(display_result) > 200:
            display_result = display_result[:180] + f"... [Truncated: {len(display_result) - 180} characters logged to core model matrix]"
            
        print(f"{CLR_MUTED}  [Task Result]: {display_result}{CLR_RESET}\n")
        return types.FunctionResponse(id=fc.id, name=name, response={"result": result})

    def _pull_the_plug_sequence(self):
        import time
        time.sleep(3) 
        while self._is_speaking:
            time.sleep(0.5) 
        time.sleep(1)
        os._exit(0)

    async def _send_realtime(self):
        while True:
            msg = await self.out_queue.get()
            await self.session.send_realtime_input(media=msg)

    async def _listen_audio(self):
        loop = asyncio.get_event_loop()
        def callback(indata, frames, time_info, status):
            if self.input_mode == "voice" and self.mic_active and not self._is_speaking:
                if not self.user_prompt_printed:
                    self.user_prompt_printed = True
                    print(f"\n{CLR_CREAM}Sagnik Sir (Voice) › {CLR_MUTED}🎙 Listening...{CLR_RESET}", end="", flush=True)
                
                def safe_put():
                    try:
                        self.out_queue.put_nowait({"data": indata.tobytes(), "mime_type": "audio/pcm"})
                    except asyncio.QueueFull:
                        pass
                loop.call_soon_threadsafe(safe_put)
                
        with sd.InputStream(samplerate=SEND_SAMPLE_RATE, channels=CHANNELS, dtype="int16", blocksize=CHUNK_SIZE, callback=callback):
            while True:
                await asyncio.sleep(0.1)

    async def _receive_audio(self):
        try:
            while True:
                async for response in self.session.receive():
                    content = response.server_content
                    if content:
                        if content.model_turn:
                            for part in content.model_turn.parts:
                                if getattr(part, 'thought', False):
                                    continue
                                if part.text:
                                    if not self.current_response_text:
                                        print(f"\r{CLR_CORAL}vector › {CLR_MUTED}█ Compiling response...{CLR_RESET}", end="", flush=True)
                                    self.current_response_text += part.text
                        
                        if content.output_transcription and content.output_transcription.text:
                            if not self.current_response_text:
                                print(f"\r{CLR_CORAL}vector › {CLR_MUTED}█ Compiling response...{CLR_RESET}", end="", flush=True)
                            self.current_response_text += content.output_transcription.text
                    
                    if response.data:
                        self.audio_in_queue.put_nowait(response.data)
                        
                    if content and content.turn_complete:
                        print(f"\r\033[K", end="") # Wipe compiling layout
                        self._print_compiled_response(self.current_response_text)
                        print(CLR_RESET)
                        
                        self.current_response_text = ""
                        self.user_prompt_printed = False
                        self.processing_text = False
                        
                    if response.tool_call:
                        fn_responses = []
                        for fc in response.tool_call.function_calls:
                            fr = await self._execute_tool(fc)
                            fn_responses.append(fr)
                        await self.session.send_tool_response(function_responses=fn_responses)
        except Exception as e:
            print(f"\n  {CLR_CORAL}▀ Presentation Layer Interrupted:{CLR_RESET} {e}")

    def _print_compiled_response(self, text):
        """Converts raw model responses into short, beautifully readable bullet points."""
        clean_text = text.strip()
        if not clean_text:
            return

        print(f"{CLR_CORAL}vector › {CLR_RESET}")
        
        # Strip structural markdown headings to make it look clean
        clean_text = clean_text.replace("**", "").replace("###", "").replace("##", "")
        
        raw_lines = clean_text.split("\n")
        for raw_line in raw_lines:
            line_content = raw_line.strip()
            if not line_content:
                continue
                
            # Strip out manual text markers
            for prefix in ["- ", "* ", "• ", "▪ ", "1. ", "2. ", "3. ", "4. ", "5. "]:
                if line_content.startswith(prefix):
                    line_content = line_content[len(prefix):].strip()
                    break
            
            if any(line_content.startswith(h) for h in ["Analyzing", "Synthesizing", "Crafting", "Delivering"]):
                continue
                
            # Break down text blocks by sentences into clean list items
            sentences = [s.strip() for s in line_content.split(". ") if s.strip()]
            for sentence in sentences:
                trimmed = sentence.rstrip(".")
                if not trimmed:
                    continue
                    
                words = trimmed.split(" ")
                highlighted_words = []
                for word in words:
                    clean_word = word.strip("*,.:()\"'")
                    if clean_word.startswith("python") or clean_word.startswith("vector_") or "\\" in clean_word or "/" in clean_word or clean_word.endswith(".py"):
                        highlighted_words.append(f"{CLR_CORAL}{word}{CLR_CREAM}")
                    elif clean_word.upper() in ["SUCCESSFUL", "ONLINE", "ACTIVE", "COMPLETE", "CONNECTED", "COMPLETED", "RESILIENT", "STABLE"]:
                        highlighted_words.append(f"{CLR_GREEN}{word}{CLR_CREAM}")
                    else:
                        highlighted_words.append(word)

                processed_sentence = " ".join(highlighted_words)
                print(f"   {CLR_CORAL}▪{CLR_CREAM} {processed_sentence}.")

    async def _text_input_loop(self):
        while True:
            if self.processing_text:
                await asyncio.sleep(0.1)
                continue
                
            if self.input_mode == "text":
                user_input = await asyncio.to_thread(input, f"{CLR_CREAM}Sagnik Sir (Text) ❯ {CLR_RESET}")
            else:
                user_input = await asyncio.to_thread(input, "")
            
            cmd = user_input.strip()
            if not cmd:
                continue
            
            # --- COMMAND GATEWAY ---
            if cmd.lower() == "/text":
                self.input_mode = "text"
                print(f"  {CLR_CORAL}⚙ Mode Switched: TEXT STREAM ACTIVE. Type below.{CLR_RESET}\n")
                self.user_prompt_printed = False
                continue
            elif cmd.lower() == "/voice":
                self.input_mode = "voice"
                print(f"  {CLR_CORAL}⚙ Mode Switched: VOICE AUDIO ACTIVE. Speak freely.{CLR_RESET}\n")
                self.user_prompt_printed = False
                continue
            elif cmd.lower() in ["/mute", "/mic"]:
                self.mic_active = not self.mic_active
                status_label = f"{CLR_GREEN}ACTIVE 🎙" if self.mic_active else f"{CLR_CORAL}MUTED 🤐"
                print(f"  {CLR_CORAL}⚙ Hardware Update: Mic is now {status_label}{CLR_RESET}\n")
                self.user_prompt_printed = False
                continue
            
            # --- SEND TYPED MESSAGE ---
            if self.input_mode == "text" and self.session:
                self.processing_text = True
                print(f"  {CLR_MUTED}⌛ Processing typed input...{CLR_RESET}", end="\r", flush=True)
                try:
                    await self.session.send_realtime_input(text=cmd)
                except Exception as send_err:
                    print(f"\n  {CLR_CORAL}▀ Failed to forward text stream:{CLR_RESET} {send_err}")
                    self.processing_text = False

    async def _play_audio(self):
        stream = sd.RawOutputStream(samplerate=RECEIVE_SAMPLE_RATE, channels=CHANNELS, dtype="int16", blocksize=CHUNK_SIZE)
        stream.start()
        try:
            while True:
                chunk = await self.audio_in_queue.get()
                self._is_speaking = True 
                await asyncio.to_thread(stream.write, chunk)
                
                if self.audio_in_queue.empty():
                    await asyncio.sleep(0.5) 
                    if self.audio_in_queue.empty():
                        self._is_speaking = False 
                self.audio_in_queue.task_done()
        finally:
            self._is_speaking = False
            stream.stop()
            stream.close()

    async def run(self):
        client = genai.Client(api_key=self.api_key, http_options={"api_version": "v1beta"})
        while True:
            try:
                print_claude_banner()
                config = self._build_config()

                async with (
                    client.aio.live.connect(model=LIVE_MODEL, config=config) as session,
                    asyncio.TaskGroup() as tg,
                ):
                    self.session = session
                    self.audio_in_queue = asyncio.Queue()
                    self.out_queue = asyncio.Queue(maxsize=10)
                    
                    print(f"  {CLR_GREEN}█ V.E.C.T.O.R. ONLINE{CLR_RESET} │ {CLR_CREAM}Continuous voice sync active. Speak freely, Sir.{CLR_RESET}\n")

                    tg.create_task(self._send_realtime())
                    tg.create_task(self._listen_audio())
                    tg.create_task(self._receive_audio())
                    tg.create_task(self._play_audio())
                    tg.create_task(self._text_input_loop())

                    # --- THE AUTOMATIC STARTUP GREETING ---
                    print(f"  {CLR_MUTED}⚙ Compiling morning briefing context...{CLR_RESET}")
                    try:
                        weather = await asyncio.to_thread(self.fetchers.get_weather, "Kolkata")
                        news = await asyncio.to_thread(self.fetchers.get_news_summary)
                        financial_news = await asyncio.to_thread(self.web.search_web, "brief overview of latest stock market breaking news and financial headlines")
                        
                        briefing_script = (
                            "System boot successful. Start your response EXACTLY with 'Hello, Sagnik Sir.', "
                            "and then immediately deliver an extremely concise, punchy briefing using the data below. "
                            "Do not ask how you can help me. Just give me the biggest highlights and skip the small details. "
                            "Do NOT call any tools:\n\n"
                            f"Weather: {weather}\n"
                            f"News: {news}\n"
                            f"Market: {financial_news}"
                        )
                        await session.send_realtime_input(text=briefing_script)
                    except Exception as briefing_error:
                        print(f"  {CLR_MUTED}⚠ Briefing pipeline bypassed: {briefing_error}{CLR_RESET}")
                        
            except Exception as e:
                print(f"\n  {CLR_CORAL}▀ Stream Interrupted.{CLR_RESET} Reconnecting in 3 seconds... ({e})")
                await asyncio.sleep(3)

if __name__ == "__main__":
    vector_os = VectorLiveSystem()
    try:
        asyncio.run(vector_os.run())
    except KeyboardInterrupt:
        print(f"\n{CLR_CORAL}[System Shutdown]: Powering down V.E.C.T.O.R.{CLR_RESET}")