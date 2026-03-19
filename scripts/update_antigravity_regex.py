import os
import json
import shutil
from datetime import datetime

settings_path = os.path.expandvars(r'%APPDATA%\Antigravity\User\settings.json')

# Backup
backup_path = f"{settings_path}.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
shutil.copy2(settings_path, backup_path)

with open(settings_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# The new auto_approve list based on documentation (regex support)
auto_approve = data.get('chat.tools.terminal.autoApprove', {})

# Commands from Qiita article / homepage
commands = [
    "ls", "pwd", "git status", "git diff", "git log", "git branch", "git show",
    "npm test", "pnpm test", "yarn test", "cargo test", "go test ./...", "pytest",
    "npm run build", "npm run lint", "cat", "echo", "cd", "python --version", "node --version",
    "Get-Location", "Get-ChildItem", "Get-Content"
]

# Add exact matches
for cmd in commands:
    auto_approve[cmd] = True

# Add Regex matches to handle arguments, redirects, and pwsh wrapping
regex_patterns = [
    r"/^git\s+(status|diff|log|branch|show)/",
    r"/^ls(\s|$)/",
    r"/^pwd(\s|$)/",
    r"/^npm\s+(test|run)/",
    r"/^pnpm\s+(test|run)/",
    r"/^yarn\s+(test|run)/",
    r"/^cargo\s+test/",
    r"/^go\s+test/",
    r"/^pytest/",
    r"/^python\s+/",
    r"/^pwsh.*?git\s+(status|diff|log)/",
    r"/^powershell.*?git\s+(status|diff|log)/",
    r"/^pwsh.*?python\s+/",
    r"/^pwsh.*?pytest/",
    r"/^pwsh.*?npm\s+/"
]

for pattern in regex_patterns:
    auto_approve[pattern] = True

# Explicitly deny destructive commands
auto_approve[r"/^(rm|del|rmdir|rd|Remove-Item)\s+/"] = False
auto_approve[r"/^pwsh.*?(rm|del|rmdir|rd|Remove-Item)\s+/"] = False

data['chat.tools.terminal.autoApprove'] = auto_approve
data['chat.tools.terminal.enableAutoApprove'] = True

with open(settings_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Settings updated with regex patterns and homepage commands")
