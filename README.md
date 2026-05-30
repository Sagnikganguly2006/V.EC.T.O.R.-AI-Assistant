# V.E.C.T.O.R. 🌐
### Virtual Everyday Companion for Tasks, Organization, and Research
*“The futuristic AI Companion designed to bring Tony Stark’s JARVIS and FRIDAY architecture to your local Windows OS.”*

V.E.C.T.O.R. is an advanced, fully interactive desktop AI operating companion custom-built for Windows environments. Heavily inspired by the iconic **JARVIS** and **FRIDAY** systems from the Marvel Cinematic Universe, it bridges the gap between natural human conversation and deep system automation. By establishing direct hardware bindings with your microphone, speakers, mouse, keyboard, display monitor, local files, and system command shells, V.E.C.T.O.R. acts as an intelligent command terminal. It can execute deep system diagnostics, program full script files, safely manage local directories, and analyze your active display monitor in real-time to assist you with complex development workflows.

---

## 🌌 About V.E.C.T.O.R.

> **V.E.C.T.O.R.** is not just another basic chatbot or standard desktop application. It is a next-generation terminal assistant designed to act as an intelligent bridge between advanced artificial intelligence and your local computer hardware.

Instead of keeping AI trapped inside a standard web browser tab, this framework weaves intelligence directly into the Windows operating system—allowing it to execute deep machine maintenance, write source files, track online data streams, and visually evaluate a monitor layout, all through continuous, zero-delay spoken conversations.

---

### 🧬 The Core Design Philosophy (The JARVIS Blueprint)

The construction of V.E.C.T.O.R. revolves around three fundamental engineering principles:

```
 ┌──────────────────────────┐      ┌──────────────────────────┐      ┌──────────────────────────┐
 │   Voice-First Synergy    │ ───> │ Autonomous Capability    │ ───> │  Guardrail-First Safety  │
 │  Natural spoken loops.   │      │ Native tool integration. │      │   Verbal approval gates. │
 └──────────────────────────┘      └──────────────────────────┘      └──────────────────────────┘
```

#### 1. Voice-First Fluidity
Traditional software interfaces rely heavily on manual mouse clicks or rigid keyboard commands. V.E.C.T.O.R. treats continuous speech as a primary input. It doesn't force a user to wait for slow text responses to type out line-by-line; it streams live sound back and forth seamlessly, making interacting with a computer feel like collaborating with a human teammate.

#### 2. Native Capability Over Passive Conversation
Most digital assistants can only give written instructions on *how* to solve a problem. V.E.C.T.O.R. is engineered to execute the solution itself. Whether it is scanning hardware health metrics, writing functional programming scripts straight to the desktop, or cleaning hidden temporary caches, the system translates conversational goals into real local machine actions.

#### 3. Ironclad Sandboxed Security
Giving an AI system access to system commands requires strict boundaries. V.E.C.T.O.R. balances raw capability with defensive design patterns. By isolating file actions inside strict boundaries and enforcing mandatory verbal validation gates for high-risk tools, the user always maintains absolute physical control over their machine.

---

### 🎨 Visual Identity & Aura

V.E.C.T.O.R. embraces a minimalist, dark-mode terminal environment featuring a custom terracotta-themed block interface. It intentionally avoids cluttered window layouts and flashy decorations, opting instead for a clean, high-impact workspace designed for focused technical productivity. Every boot sequence, diagnostic sheet, and script alert is formatted to display clear information with zero unnecessary noise.

---

## 📊 Key Features & Capabilities Matrix

| Feature Layer | Core Technology | Primary Function | Safety Status |
| :--- | :--- | :--- | :--- |
| **🎙️ Audio Engine** | Gemini Live Audio WebSockets | Real-time continuous two-way voice streaming | 🟢 Always Safe |
| **💻 Code Builder** | Groq / Llama-3.3-70b API | Autonomous multi-language script writing | 🟢 Code Sandboxed |
| **🛠️ System Admin** | Windows PowerShell / `psutil` | System health diagnostics & process management | 🔴 Requires Confirmation |
| **📁 File Guard** | Path Validation / `pathlib` | local directory read/write/recycle operations | 🟡 Safe Zones Only |
| **👁️ Computer Vision**| Multi-Modal Screen Grabs | Instant monitor capture and visual context analysis | 🟢 Temporary Memory |
| **🌐 Web Grounding**| RSS / DuckDuckGo / YouTube | Scraping live news, weather, and video data | 🟢 Auto Fallback |

---

## 🌟 Detailed Feature-by-Feature Deep Dive

The architecture is built on a fully modular framework where each file represents a distinct functional "sense" or "skill layer."

### 1. `vector_master.py` — The Central Nervous System
* **Gemini Live Audio Connection:** Establishes a real-time, low-latency vocal connection with Google’s advanced AI audio preview networks using active bidirectional web-socket links.
* **Asynchronous Routing Architecture:** Manages internal scheduling pools using simple background timers to simultaneously process incoming microphone input streams, play generated speech responses, watch for typed shell shortcuts, and execute background file scripts.
* **The Automated Morning Briefing:** Upon initialization, it automatically accesses local weather reports, scans global headlines, updates currency/crypto prices, and commands the AI to compile a punchy summary profile. It starts the day explicitly with *"Hello, Sagnik Sir."* to jumpstart your workflow.
* **Claude-Inspired Graphic UI:** Clears the Windows console screen on boot to display a high-fidelity terracotta-colored block banner framework mimicking minimalist developer command-line interfaces.

### 2. `vector_audio.py` — Vocal Sensor Controls
* **Background Standby Engine:** Keeps the software running efficiently in low-power standby mode while monitoring global computer hotkeys via background tracking tools.
* **Hardware Trigger Synced-Loops:** Activates the microphone array immediately upon pressing `ctrl+space`, shifting into high-sensitivity listening registers. Shifting out of listening mode places the core smoothly back into standby, notifying you with a clean console log tracker.
* **Vocal Pacing Constraints:** Uses hardcoded guidelines to ensure all spoken audio uses an authoritative, premium tone that is delivered slowly, deliberately, and with distinct pauses between sentences.

### 3. `vector_controls.py` — Native Hardware and Peripheral Drivers
Divided into two core administrative components to provide deep computer control:
* **VectorHands (System Maintenance Engineering):**
  * *Full Health Diagnostics:* Analyzes core performance indicators, generating metrics for active CPU usage percentage, occupied RAM limits, free disk partition storage space in gigabytes, and active laptop battery statuses (detecting if it is plugged into a wall charging system or running on temporary fuel).
  * *Power Automation Pipelines:* Integrates with native Windows kernel binaries to initiate complete computer shutdowns or clean operating system restarts after executing a protective 5-second console countdown delay.
  * *Background Process Hunting:* Scans running task paths to identify, locate, and terminate memory-clogging background windows or processes (such as tracking files like `mc-fw-host`) and shuts them down using forced kill commands.
  * *PowerShell Optimization Engine:* Programmatically executes localized shell paths to clear temporary storage caches and user cache items while checking your formal Windows Performance Index scores (`WinSPRLevel`) via the Windows Management frameworks.
* **VectorControls (Peripherals and J.A.R.V.I.S. Mimicry Tools):**
  * *Application Workspace Manager:* Spins up native computer programs (web browsers, text tools, media apps) or cleanly closes active windows through close-match application openers.
  * *Hardware Level Injections:* Directs monitor lighting levels and injects multimedia keyboard audio adjustments to turn volume ranges up, down, or mute sound outputs entirely.
  * *Advanced Input Simulators:* Mimics manual user actions such as text-string typewriting with precise delay intervals, programmatic mouse clicks, and multiple concurrent key combinations (hotkeys).
  * *Clipboard Synchronizers:* Accesses the active copy-paste clipboard to read text strings or inject text segments directly into the system clipboard.

### 4. `vector_builder.py` — The Autonomous Software Engineer
* **Multi-Language Script Generator:** Interfaces with external high-speed computing endpoints to automatically write code files in **Python (.py)**, **C++ (.cpp)**, and **C (.c)** from simple spoken plain-English objectives.
* **Raw Code Stripping Algorithms:** Utilizes clean text filters to clean up incoming language strings, scrubbing markdown code block fences and conversational AI commentary to compile perfectly clean source code.
* **Desktop Automation Compiling:** Programmatically resolves directory links to generate code files and save them straight to your desktop.
* **Technical Project Workflows:** Acts as a specialized project administrator to draft step-by-step engineering plans, development phases, and structural project workflows inside a structured blueprint file layout.

### 5. `vector_files.py` — Sandboxed File Guardian
* **Path-Isolated Storage Arrays:** Implements an alias map tracking simple folder names (`desktop`, `documents`, `downloads`, `project`, `d_drive`) and resolves them into strict, fully qualified absolute file pathways.
* **Local Workspace Operators:** Executes localized file input/output management tasks, allowing the assistant to read internal text data, overwrite records, append real-time telemetry updates, and search active folder items.
* **Recycle Bin Protection:** Prevents catastrophic mistakes by bypassing harsh permanent file-erasing loops, moving targeted items safely to the active Windows Recycle Bin instead.

### 6. `vector_vision.py` — Optical Display Mapping
* **In-Memory Display Grabber:** Captures real-time snapshots of your active primary monitor monitor. The resulting picture data is converted and packed as compressed raw binary bytes inside memory streams. This workflow keeps your physical hard drive completely clean of heavy image file clutter.
* **Multi-Modal Image Evaluation:** Forwards the raw byte packet directly into multi-modal networks, allowing the system to visually inspect user interfaces, review active development environments, evaluate layout designs, and answer contextual screen questions.

### 7. `vector_media.py` — Web Grounding & Online Navigators
* **Grounded Web Search Engines:** Implements online grounding tools to connect text search requests with live search engines, scraping current events and internet articles to answer user prompts with factual up-to-date data.
* **Dual-Tier Resilient Fallbacks:** Features an automated internet safety-net structure. If primary AI web grounding queries experience an account limit or network block, it switches to backup text search engines to gather top website summaries.
* **Instant YouTube Automation:** Translates media commands to instantly open targeted web browser threads, query online media databases, and automatically launch video playbacks on your screen.
* **Audio-to-Text Video Summarizer:** Utilizes background transcription networks to download video subtitles, transforming hours of continuous footage into concise summary paragraphs.

### 8. `vector_fetchers.py` — Global Environmental Sensors
* **Atmospheric Satellite Mapping:** Interfaces with live weather satellite platforms to pull current ambient temperatures, real-feel metrics, weather alerts, and local cloud conditions, using a text fallback tracker if networks are offline.
* **RSS Headline Networks:** Scrapes running news syndication feeds to extract the top three breaking stories happening around the globe.
* **Financial Data Grabbers:** Evaluates current ticker entries via market analytics packages to deliver live valuation pricing for target stocks or cryptocurrency coins.

### 9. `vector_communication.py` — Headless Network Automation
* **Invisible Social Integrations:** Establishes silent web-driver modules in the background to log into channels like WhatsApp Web, scanning for unread updates and flashing sender text notifications to the terminal.
* **Background Email Draft Assemblers:** Formulates complete secure connections with mail servers to audit email states, filter out junk mail keywords, and compile template email responses straight into your drafts folder without launching a standard window interface.

---

## 🧠 Core Engineering Concepts Explained Simply

To understand how V.E.C.T.O.R. functions under the hood, here are the foundational computer science and engineering concepts used throughout the project, explained without complex jargon:

### 1. Asynchronous Multi-Tasking Loop (`asyncio`)
* **The Concept:** Traditional computer programs are "synchronous," meaning they can only do one thing at a time. If a program is downloading a large file, the whole user interface freezes until the download finishes. V.E.C.T.O.R. uses *Asynchronous Programming*.
* **How it works here:** Think of the assistant as a professional multi-tasking chef in a kitchen. Instead of standing completely still and staring at water waiting for it to boil, the chef cuts vegetables, preheats the oven, and checks a recipe at the exact same time. The `asyncio` system lets V.E.C.T.O.R. continuously stream audio from your microphone, play speech back through your speakers, listen for typed terminal commands, and run background scripts simultaneously without ever freezing.

### 2. Real-Time Bidirectional Streaming (WebSockets)
* **The Concept:** Most internet operations use standard HTTP requests, which work like sending letters through the mail: you send a request, wait, and get a reply back. V.E.C.T.O.R. utilizes a *WebSocket* connection for its voice feature.
* **How it works here:** WebSockets work exactly like an open, live phone call. Once the connection is built between V.E.C.T.O.R. and the AI network servers, data flows back and forth continuously in tiny fragments. This lets the assistant hear your words and interrupt its own speaking instantly if you start talking over it, resulting in natural conversation without frustrating delays.

### 3. Path-Isolation and Directory Sandboxing
* **The Concept:** When an AI tool is given the power to read or delete files on a computer, there is a risk it could misunderstand a command and modify critical operating system files. To stop this, V.E.C.T.O.R. uses *Path Sandboxing* via the `pathlib` utility.
* **How it works here:** The program creates a strict "Safe Zone" filter. When you ask it to view or delete a file, the system instantly calculates the exact, absolute path of that file. If the file lives outside your designated safe folders (like the Desktop or Documents), the system flags it as an illegal operation and locks it down. It acts like a security guard drawing a physical line that the assistant is barred from crossing.

### 4. In-Memory Binary Serialization (`io.BytesIO`)
* **The Concept:** Usually, when a program takes a screenshot, it has to save that picture onto your computer's hard drive as a `.png` or `.jpg` file, and then open it back up to read it. Doing this constantly wastes time and clutters your computer with junk files.
* **How it works here:** V.E.C.T.O.R. captures your monitor screen and transforms the picture directly into raw binary numbers (zeros and ones) stored temporarily inside your computer's RAM (volatile memory). This is called *In-Memory Serialization*. The AI looks at this direct memory stream to see what is on your screen and discards it instantly when done, meaning no actual image files are ever written to your physical storage.

### 5. Resilient Failover & Graceful Degradation
* **The Concept:** External internet systems and APIs go down or become busy all the time. A fragile application will crash immediately if a server fails to respond. V.E.C.T.O.R. is engineered around the principle of *Graceful Degradation*.
* **How it works here:** The project implements automated redundancy safety nets. For instance, if the primary high-end search engine fails or hits a rate limit, the program doesn't give up. It instantly catches the error behind the scenes and switches to an alternate public web scraper tool. You still get your answer seamlessly, and the system stays fully stable.

### 6. Fuzzy String Matching
* **The Concept:** Computers are usually unforgiving—if you tell them to open a program named "Google Chrome" but you type "chrome" or make a typo, a standard system will fail to find it. V.E.C.T.O.R. utilizes *Fuzzy Matching* logic.
* **How it works here:** When you speak or type a command to open or close an application, the assistant analyzes the text pattern and scores it against all your installed programs. It calculates a similarity percentage, meaning it can confidently launch the correct tool even if you misspell it, stutter, or use short nicknames.

---

## 🛠️ Combined Setup & Installation Guide

Run this single, unified code block in your Windows command prompt (`cmd`) to download the files, install every package dependency, create your environment config file, and boot the core framework:

```bash
# 1. Clone the repository and enter the project folder
git clone [https://github.com/your-username/VECTOR.git](https://github.com/your-username/VECTOR.git)
cd VECTOR

# 2. Install all hardware wrappers, audio streaming drivers, and AI SDK packages
pip install google-genai groq psutil pyautogui pyperclip screen-brightness-control AppOpener yfinance requests sounddevice pillow duckduckgo_search youtube_transcript_api selenium python-dotenv pywhatkit pynput

# 3. Create your secret configuration environment file
echo. > .env

# 4. Launch V.E.C.T.O.R.'s main controller interface
python vector_master.py
```

### 🔑 Final Step: Add Your Secret Keys
Before executing the last startup script, open the newly created `.env` file in Notepad or any code text editor, paste the template configuration below, and swap the placeholder strings out for your unique authorization keys:

```env
GROQ_API_KEY=your_secret_groq_api_key_here
GEMINI_API_KEY=your_secret_gemini_api_key_here
OPENWEATHER_API_KEY=your_secret_openweather_api_key_here
```

---

🚀 Instant One-Click Desktop Deployment
To access your environment with one click from your screen just like the Stark Mainframe, create a shortcut script named Launch_VECTOR.bat on your desktop and paste the following directory launcher inside it:
```Code Snippet
@echo off
title V.E.C.T.O.R. Mainframe
cd /d "C:\paste_your_path"
python vector_master.py
pause
```



## 🎮 Interface Controls & Safety Systems

### Live Terminal Command Switches
While the application loop is fully active in your terminal, click inside the window to execute quick keyboard instructions:
* `/text` — Disables microphone tracking loops and puts the system into text stream mode (manually type instructions).
* `/voice` — Instantly reactivates full hardware microphone scanning for real-time live vocal synchronization.
* `/mute` or `/mic` — Toggles your local microphone sensor state on or off immediately when you need quick room privacy.

### 🔒 Strict Verbal Approval Guards
To ensure you remain in total control of your computer, V.E.C.T.O.R. implements a strict **Safety Protocol**. It is programmatically blocked from finishing any high-risk system command without your explicit permission. If you command it to:
1. Erase files, wipe directories, or overwrite existing information.
2. Run deep performance optimizations or wipe temporary cache lines.
3. Force-close or terminate active background system processes.
4. Shut down or restart the physical computer hardware.

The system will automatically halt, speak out loud to you, and request confirmation. The entire execution path will be safely bypassed unless you give an explicit answer like **"yes"** or **"proceed"**.

---

## 📂 Detailed File Directory Map

```bash
Project-VECTOR/
│
├── vector_master.py        # Central nervous system. Handles asyncio loops, audio queues, and routers.
├── vector_audio.py         # Vocal controls. Handles standby states and microphone listening triggers.
├── vector_controls.py      # Physical hands. Runs diagnostic checks, controls processes, and simulates inputs.
├── vector_builder.py       # Coding and planning brain. Writes raw source files and technical plans.
├── vector_files.py         # Local workspace manager. Controls sandboxed file reads and recycle paths.
├── vector_vision.py        # Optical recognition eye. Grabs memory snapshots for visual analysis.
├── vector_media.py         # Web browser networker. Coordinates web searches and YouTube integrations.
├── vector_fetchers.py      # Information sensors. Tracks live weather, market trackers, and RSS feeds.
├── vector_communication.py # Hidden network driver. Manages background web-drivers and mail endpoints.
│
├── vector_identity.txt     # Profile parameters. Establishes the premium tone and slow pacing rules.
├── vector_memory.db        # Persistent SQLite storage data layer that tracks long-term memories.
└── .env                    # Secure hidden workspace file mapping private API keys.
```

---

## 👥 System Metadata and Credits
* **Architect / Core Programmer:** Sagnik Ganguly
* **Development Platform Target:** Windows OS Infrastructure (10/11 x64 architecture)
* **Underlying AI Infrastructure:** Gemini 2.5 Flash Native Live Audio Preview, Gemini 2.5 Flash & Llama-3.3-70b-Versatile
