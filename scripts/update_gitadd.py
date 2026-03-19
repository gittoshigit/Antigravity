import os
import json

settings_path = os.path.expandvars(r'%APPDATA%\Antigravity\User\settings.json')
with open(settings_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

auto_approve = data.get('chat.tools.terminal.autoApprove', {})

# Exact matches
exact_command_1 = "pwsh -NoProfile -Command \"git add .; git status\""
exact_command_2 = "pwsh -NoProfile -Command \"git add . && git status\""
auto_approve[exact_command_1] = True
auto_approve[exact_command_2] = True
auto_approve["pwsh -NoProfile -Command \"git add .\""] = True

# Add "git add" to regex patterns. 
# Previously we only allowed read-only git commands (status, diff, log, branch, show).
# git add modifies state, so it likely fell through the cracks and was not auto-approved.
auto_approve[r"/^git\s+(status|diff|log|branch|show|add)/"] = True
auto_approve[r"/^pwsh.*?git\s+(status|diff|log|add).*?/"] = True
auto_approve[r"/^powershell.*?git\s+(status|diff|log|add).*?/"] = True

data['chat.tools.terminal.autoApprove'] = auto_approve

with open(settings_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Settings updated")
