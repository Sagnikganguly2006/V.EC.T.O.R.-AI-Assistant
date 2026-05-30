import os
import shutil
import subprocess
from pathlib import Path

class VectorFiles:
    def __init__(self, senses_module):
        self.senses = senses_module
        
        self.home = Path.home()
        
        # --- SMART FOLDERS (Bulletproof Location Aliases) ---
        self.locations = {
            "desktop": (self.home / "Desktop").resolve(),
            "documents": (self.home / "Documents").resolve(),
            "downloads": (self.home / "Downloads").resolve(),
            "project": Path.cwd().resolve(),
            "d_drive": Path("D:/").resolve()
        }
        
        # Safe zones are automatically generated from the locations above
        self.safe_zones = list(self.locations.values())

    def _is_safe(self, target_path):
        """Checks if a file path is inside one of the allowed Safe Zones."""
        try:
            target = Path(target_path).resolve()
            for zone in self.safe_zones:
                if target == zone or zone in target.parents:
                    return True
            return False
        except Exception:
            return False

    def manage(self, action, filename="", location="project", content=None, new_filename=None, new_location=None):
        """The master function using Smart Folders to avoid typos."""
        
        # 1. Look up the true path based on the simple alias (e.g., "desktop")
        base_dir = self.locations.get(location.lower())
        if not base_dir:
            return f"Error: '{location}' is an invalid alias. Use desktop, documents, downloads, project, or d_drive."
        
        # 2. Safely combine the true path with the filename
        target = (base_dir / (filename or "")).resolve()

        if not self._is_safe(target):
            if self.senses: self.senses.speak("Access denied. That location is outside my safe zones.")
            return f"Access Denied: {target} is outside of V.E.C.T.O.R.'s Safe Zones."

        try:
            if action == "read":
                if not target.exists(): return f"File {filename} does not exist in {location}."
                with open(target, 'r', encoding='utf-8') as f:
                    return f"File Contents:\n{f.read()}"
                    
            elif action == "write":
                target.parent.mkdir(parents=True, exist_ok=True) # Create subfolders if needed
                with open(target, 'w', encoding='utf-8') as f:
                    f.write(content or "")
                return f"Successfully overwritten {target.name} in the {location} folder."
                
            elif action == "append":
                if not target.exists(): return "File does not exist. Use write first."
                with open(target, 'a', encoding='utf-8') as f:
                    f.write("\n" + (content or ""))
                return f"Successfully added text to {target.name}."
                
            elif action == "rename" or action == "move":
                if not new_filename: return "New filename not provided."
                dest_dir = self.locations.get((new_location or location).lower())
                new_target = (dest_dir / new_filename).resolve()
                
                if not self._is_safe(new_target): return "Access Denied: Target destination is outside Safe Zones."
                
                new_target.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(target), str(new_target))
                return f"Successfully moved to {new_target.name}."
                
            elif action == "list":
                if not target.is_dir(): return "Path is not a folder."
                items = [f.name for f in target.iterdir()]
                return f"Contents of {location}: {', '.join(items) if items else 'Empty folder'}"
                
            elif action == "delete":
                if not target.exists(): return "File or Folder does not exist."
                ps_script = f"Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile('{target}', 'OnlyErrorDialogs', 'SendToRecycleBin')"
                subprocess.run(["powershell", "-Command", ps_script], capture_output=True)
                
                if self.senses: self.senses.speak(f"Item neutralized. {target.name} has been moved to the recycle bin.")
                return f"Successfully moved {target.name} to the Recycle Bin."
                
            else:
                return "Invalid file action."
                
        except Exception as e:
            return f"File operation failed: {e}"