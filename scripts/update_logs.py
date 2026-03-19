import json
import codecs
from datetime import datetime

# Update state_compact.json
with codecs.open('state_compact.json', 'r', 'utf-8') as f:
    state = json.load(f)

timestamp = datetime.now().astimezone().replace(microsecond=0).isoformat()
state['履歴'].append({
    'timestamp': timestamp,
    'event': 'specific_command_added',
    'detail': {
        '実施内容': 'リダイレクトを含む python main.py コマンドを autoApprove に追加した。',
        '追加コマンド': 'pwsh -NoProfile -Command "python main.py > artifacts/error_log.txt 2>&1"'
    }
})

with codecs.open('state_compact.json', 'w', 'utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

# Update work_journal.md
journal_entry = f'''
## {datetime.now().strftime('%Y-%m-%d %H:%M')}
### 種別：修正
### フェーズ：運用

- **目的：** リダイレクトを含む特定のコマンドが自動承認をすり抜ける問題への対応。
- **実施内容：**
  - `pwsh -NoProfile -Command "python main.py > artifacts/error_log.txt 2>&1"` を `autoApprove` に完全一致で追加した。
- **結果：** `settings.json` が更新された。
- **影響範囲：** 現在のPCの Antigravity IDE
'''

with codecs.open('work_journal.md', 'a', 'utf-8') as f:
    f.write(journal_entry)
