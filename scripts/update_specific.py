import os
import json

settings_path = os.path.expandvars(r'%APPDATA%\Antigravity\User\settings.json')
with open(settings_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

auto_approve = data.get('chat.tools.terminal.autoApprove', {})
new_commands = {
    'pwsh -NoProfile -Command "python main.py > artifacts/error_log.txt 2>&1"': True,
    'powershell.exe -NoProfile -Command "python main.py > artifacts/error_log.txt 2>&1"': True,
}
auto_approve.update(new_commands)
data['chat.tools.terminal.autoApprove'] = auto_approve

with open(settings_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Updated settings.json with python main.py command')
