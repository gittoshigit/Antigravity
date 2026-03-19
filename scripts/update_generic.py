import os
import json
import shutil
from datetime import datetime

settings_path = os.path.expandvars(r'%APPDATA%\Antigravity\User\settings.json')

# Backup
backup_path = f"{settings_path}.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
shutil.copy2(settings_path, backup_path)
print(f"Backed up to {backup_path}")

with open(settings_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build a new generic autoApprove list
auto_approve = {}

# 1. Base exact commands (safe)
base_safe = [
    "git status", "git log", "git diff", "git branch", "git show",
    "ls", "dir", "cat", "type", "echo", "pwd", "cd",
    "python --version", "node --version", "npm --version", "pytest",
    "python -m pytest", "npm test", "npm run test", "npm run build", "npm run lint",
    "Get-Location", "Get-ChildItem", "Get-Content", "Write-Output",
    "Set-Location", "Clear-Host", "Get-Command", "Get-Help", "Test-Path",
    "Select-String", "pwsh --version", "powershell --version"
]
for cmd in base_safe:
    auto_approve[cmd] = True
    auto_approve[f"{cmd}*"] = True # For interactive suffix matching

# 2. Base unsafe commands (block)
base_unsafe = [
    "rm", "del", "rmdir", "rd", "Remove-Item", "npm install", "pip install",
    "winget install", "choco install", "curl", "wget", "Invoke-WebRequest",
    "format", "mkfs"
]
for cmd in base_unsafe:
    auto_approve[cmd] = False
    auto_approve[f"{cmd} *"] = False

# 3. Wrapper wildcards (pwsh & powershell.exe) for AI agent shell execution
wrappers = ['pwsh -NoProfile -Command', 'powershell.exe -NoProfile -Command']

safe_prefixes = [
    "git status*", "git log*", "git diff*", "git branch*", "git show*",
    "ls*", "dir*", "cat*", "type*", "echo*", "pwd*", "cd*",
    "python *", "pytest*", "npm test*", "npm run*", 
    "Get-*", "Test-Path*", "Select-String*", "Write-Output*", "Clear-Host*"
]

unsafe_prefixes = [
    "rm *", "del *", "rmdir *", "rd *", "Remove-Item *",
    "npm install*", "pip install*", "winget install*", "choco install*",
    "curl *", "wget *", "Invoke-WebRequest *", "format *", "mkfs *"
]

for w in wrappers:
    # Add safe globs
    for sp in safe_prefixes:
        auto_approve[f"{w} \"{sp}\""] = True
        auto_approve[f"{w} '{sp}'"] = True
        
    # Add unsafe globs explicitly to block them
    for up in unsafe_prefixes:
        auto_approve[f"{w} \"{up}\""] = False
        auto_approve[f"{w} '{up}'"] = False
        
    # Generic multiple command chains (like git status && git diff)
    auto_approve[f"{w} \"*git status*git diff*\""] = True
    auto_approve[f"{w} \"*git log*\""] = True

data['chat.tools.terminal.autoApprove'] = auto_approve

with open(settings_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Updated settings.json with generic wildcard commands.')
