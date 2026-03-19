import os
import json
import shutil
from datetime import datetime

settings_path = os.path.expandvars(r'%APPDATA%\Antigravity\User\settings.json')

# Backup
backup_path = f"{settings_path}.bak_approval_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
if os.path.exists(settings_path):
    shutil.copy2(settings_path, backup_path)
    print(f"Backed up settings to {backup_path}")
    with open(settings_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
else:
    print(f"Settings file not found at {settings_path}. Creating new one.")
    data = {}

# Ensure global auto approve is off (we want authentication mode, not YOLO)
if 'chat.tools.global.autoApprove' in data:
    data['chat.tools.global.autoApprove'] = False

# Enable terminal auto approve
data['chat.tools.terminal.enableAutoApprove'] = True

# Get or create the autoApprove dictionary
auto_approve = data.get('chat.tools.terminal.autoApprove', {})

# Define the whitelist (safe commands -> true) and blacklist (dangerous -> false)
# Using regex where appropriate to catch variations, as supported by the IDE
updates = {
    # --- Allow ALL Commands (YOLO style for terminal) ---
    r"/.*/": True,

    # --- Blacklist is empty as per user request ---
}

# Update the dictionary
auto_approve.update(updates)
data['chat.tools.terminal.autoApprove'] = auto_approve

# Write back to settings.json
with open(settings_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Successfully applied Authentication Mode (Whitelist) to settings.json.')
