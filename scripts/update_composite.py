import os
import json

settings_path = os.path.expandvars(r'%APPDATA%\Antigravity\User\settings.json')
with open(settings_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

auto_approve = data.get('chat.tools.terminal.autoApprove', {})

# Add the exact command the user reported
exact_command = "pwsh -NoProfile -Command \"git status; echo '---'; git diff; echo '---'; git diff --cached\""
auto_approve[exact_command] = True

# Also add powershell.exe equivalent just in case
exact_command_ps = "powershell.exe -NoProfile -Command \"git status; echo '---'; git diff; echo '---'; git diff --cached\""
auto_approve[exact_command_ps] = True

# Add a more permissive regex that allows any sequence of git status/diff/echo commands
auto_approve[r"/^pwsh.*?(git status|git diff|echo).*?/"] = True
auto_approve[r"/^powershell.*?(git status|git diff|echo).*?/"] = True

data['chat.tools.terminal.autoApprove'] = auto_approve

with open(settings_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Settings updated")
