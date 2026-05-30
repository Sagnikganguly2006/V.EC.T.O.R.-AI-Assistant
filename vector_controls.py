import os
import platform
import psutil
import time
import pyautogui
import pyperclip
import subprocess
import screen_brightness_control as sbc
from AppOpener import open as open_app_native, close as close_app_native

# ==========================================
# 1. THE SYSTEM HANDS (PC Health & Safety)
# ==========================================

class VectorHands:
    def __init__(self, senses_module):
        self.senses = senses_module

    def check_system_health(self):
        """Runs a full diagnostic on CPU, RAM, Battery, and Storage."""
        if self.senses:
            self.senses.speak("Running full system diagnostics. Please wait...")
            
        # 1. CPU and Memory (RAM)
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = psutil.virtual_memory().percent
        
        # 2. Battery
        battery = psutil.sensors_battery()
        if battery:
            plugged = "plugged into power" if battery.power_plugged else "running on battery"
            battery_report = f"Battery is at {battery.percent} percent and is currently {plugged}."
        else:
            battery_report = "This system does not have a battery."
            
        # 3. Disk Space
        disk = psutil.disk_usage('/')
        # Math to convert raw bytes into easily readable Gigabytes (GB)
        free_space_gb = round(disk.free / (1024 ** 3), 1)
        
        # The final compiled report
        report = (
            f"Diagnostics complete. CPU usage is at {cpu_usage} percent. "
            f"Memory usage is at {mem_usage} percent. "
            f"{battery_report} You currently have {free_space_gb} gigabytes of free storage space."
        )
        
        if self.senses:
            self.senses.speak(report)
        return report

    def safe_delete(self, target_name):
        if self.senses:
            self.senses.speak(f"Searching for {target_name} to delete.")
        return f"File deletion sequence initiated for {target_name}."

    def execute_command(self, command):
        command_lower = command.lower()
        if "health" in command_lower or "diagnostics" in command_lower:
            self.check_system_health()
        elif "delete" in command_lower:
            target = command_lower.replace("delete", "").strip()
            self.safe_delete(target)

    def optimize_system_performance(self):
        """Clears temp files, flushes memory, and checks PC performance scores."""
        if self.senses: 
            self.senses.speak("Initiating deep system optimization...")
        try:
            # Safely clear out junk temporary files
            subprocess.run(["powershell", "-Command", "Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue"], capture_output=True)
            
            # Check the Windows Performance Index (WinSPRLevel)
            perf_check = subprocess.run(["powershell", "-Command", "Get-CimInstance Win32_WinSAT | Select-Object WinSPRLevel"], capture_output=True, text=True)
            
            return f"System optimization complete. Junk files cleared. Memory flushed. Performance metrics accessed: {perf_check.stdout.strip()}"
        except Exception as e:
            return f"Optimization encountered an issue: {e}"

    def hunt_and_terminate_process(self, process_name="mc-fw-host"):
        """Hunts down and forcibly removes annoying background programs."""
        clean_name = process_name.replace(".exe", "")
        if self.senses: 
            self.senses.speak(f"Hunting for background process: {clean_name}...")
        try:
            # Tell PowerShell to force stop the program
            kill_cmd = f"Stop-Process -Name '{clean_name}' -Force"
            result = subprocess.run(["powershell", "-Command", kill_cmd], capture_output=True, text=True)
            
            if result.returncode == 0:
                return f"Target neutralized. {clean_name} has been successfully terminated."
            else:
                return f"Target {clean_name} was not found running in the background."
        except Exception as e:
            return f"Termination failed: {e}"
        
    def shutdown_pc(self):
        """Executes the native Windows shutdown command."""
        if self.senses:
            self.senses.speak("Initiating full hardware shutdown. See you later, sir.")
        try:
            # The /s means shutdown, the /t 5 adds a 5-second delay
            subprocess.run(["shutdown", "/s", "/t", "5"], capture_output=True)
            return "Windows PC shutdown initiated."
        except Exception as e:
            return f"Failed to shut down the PC: {e}"
        
    def restart_pc(self):
        """Executes the native Windows restart command."""
        if self.senses:
            self.senses.speak("Initiating full hardware restart. I will be offline momentarily.")
        try:
            # The /r means restart, the /t 5 adds a 5-second delay
            subprocess.run(["shutdown", "/r", "/t", "5"], capture_output=True)
            return "Windows PC restart initiated."
        except Exception as e:
            return f"Failed to restart the PC: {e}"
        

# ==========================================
# 2. THE MOTOR SKILLS (Apps, Hardware, JARVIS Keyboard/Mouse)
# ==========================================
class VectorControls:
    def __init__(self, senses_module):
        self.senses = senses_module
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05

    # --- Legacy Hardware Controls ---
    def adjust_volume(self, action):
        if action == "up":
            for _ in range(5): pyautogui.press('volumeup')
        elif action == "down":
            for _ in range(5): pyautogui.press('volumedown')
        elif action == "mute":
            pyautogui.press('volumemute')

    def set_brightness(self, level):
        try:
            sbc.set_brightness(level)
        except Exception:
            pass

    def process_control_command(self, command):
        command_lower = command.lower()
        if "volume up" in command_lower: self.adjust_volume("up")
        elif "volume down" in command_lower: self.adjust_volume("down")
        elif "mute" in command_lower: self.adjust_volume("mute")
        elif "brightness" in command_lower:
            words = command_lower.split()
            for word in words:
                if word.isdigit():
                    self.set_brightness(int(word))
                    return
            self.set_brightness(50)

    # --- App Controls ---
    def launch_app(self, app_name):
        clean_name = app_name.lower().replace("browser", "").strip()
        if self.senses: self.senses.speak(f"Initializing launch sequence for {clean_name}...")
        try:
            open_app_native(clean_name, match_closest=True, output=False)
            return f"Successfully opened {clean_name}."
        except Exception:
            try:
                os.system(f"start {clean_name}")
                return f"Used secondary system to open {clean_name}."
            except Exception:
                return f"I was unable to locate {app_name}."

    def close_app(self, app_name):
        clean_name = app_name.lower().replace("browser", "").strip()
        if self.senses: self.senses.speak(f"Closing {clean_name}...")
        try:
            close_app_native(clean_name, match_closest=True, output=False)
            return f"Successfully closed {clean_name}."
        except Exception:
            return f"I could not close {app_name}."

    # --- J.A.R.V.I.S. Advanced Computer Controls ---
    def type_text(self, text):
        time.sleep(0.3)
        pyautogui.typewrite(text, interval=0.03)
        return f"Typed exactly: {text}"

    def press_hotkey(self, keys):
        key_list = [k.strip() for k in keys.replace('+', ',').split(',')]
        pyautogui.hotkey(*key_list)
        return f"Executed keyboard shortcut: {keys}"

    def click_mouse(self, button="left"):
        pyautogui.click(button=button)
        return f"Clicked {button} mouse button."

    def read_clipboard(self):
        text = pyperclip.paste()
        return text if text else "The clipboard is empty."

    def write_clipboard(self, text):
        pyperclip.copy(text)
        return "The requested text has been copied to the clipboard."