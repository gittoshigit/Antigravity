import os
import json
import re
from datetime import datetime
import shutil

settings_path = os.path.expandvars(r"%APPDATA%\Antigravity\User\settings.json")

# Backup
backup_path = f"{settings_path}.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
shutil.copy2(settings_path, backup_path)
print(f"Backed up to {backup_path}")

# Read and fix trailing comma if exists
with open(settings_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove trailing commas before closing braces
content = re.sub(r',\s*}', '}', content)

try:
    data = json.loads(content)
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")
    exit(1)

# Add new keys
data["chat.tools.terminal.enableAutoApprove"] = True
data["chat.tools.terminal.autoApprove"] = {
    "git status": True, "git log": True, "git diff": True, "git branch": True, "git show": True,
    "ls": True, "dir": True, "cat": True, "type": True, "echo": True, "pwd": True, "cd": True,
    "python --version": True, "node --version": True, "npm --version": True, "pytest": True,
    "python -m pytest": True, "npm test": True, "npm run test": True, "npm run build": True, "npm run lint": True,
    "Get-Location": True, "Get-ChildItem": True, "Get-Content": True, "Write-Output": True,
    "Set-Location": True, "Clear-Host": True, "Get-Command": True, "Get-Help": True, "Test-Path": True,
    "Select-String": True, "pwsh --version": True, "powershell --version": True,
    "rm": False, "del": False, "rmdir": False, "rd": False, "Remove-Item": False, "npm install": False, "pip install": False,
    "winget install": False, "choco install": False, "curl": False, "wget": False, "Invoke-WebRequest": False,
    "format": False, "mkfs": False
}
data["chat.tools.terminal.outputLocation"] = "none"

# Write back
with open(settings_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Settings successfully applied.")
