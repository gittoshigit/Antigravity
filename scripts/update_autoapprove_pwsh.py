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

# Add new pwsh wrapped commands
auto_approve = data.get('chat.tools.terminal.autoApprove', {})
new_commands = {
    'pwsh -NoProfile -Command "git status -uall; git diff"': True,
    'pwsh -NoProfile -Command "git status"': True,
    'pwsh -NoProfile -Command "git diff"': True,
    'pwsh -NoProfile -Command "git log"': True,
    'pwsh -NoProfile -Command "git log -n 3"': True,
    'pwsh -NoProfile -Command "git status && git diff HEAD && git log -n 3"': True,
    'powershell.exe -NoProfile -Command "git status -uall; git diff"': True,
    'powershell.exe -NoProfile -Command "git status"': True,
    'powershell.exe -NoProfile -Command "git diff"': True,
    'powershell.exe -NoProfile -Command "git log"': True,
    'powershell.exe -NoProfile -Command "git status && git diff HEAD && git log -n 3"': True,
}
auto_approve.update(new_commands)
data['chat.tools.terminal.autoApprove'] = auto_approve

with open(settings_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Updated settings.json with pwsh wrapped commands.')
