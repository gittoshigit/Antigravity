import json
import codecs
from datetime import datetime

# Update work_journal.md
journal_entry = f'''
## {datetime.now().strftime('%Y-%m-%d %H:%M')}
### 種別：修正
### フェーズ：運用

- **目的：** `git commit` を含むコマンドがAntigravity IDEで承認待ちになってしまう問題の対応。
- **実施内容：**
  - これまで状態変更を伴うため除外していた `git commit` を、ユーザーの利便性向上のため `chat.tools.terminal.autoApprove` の正規表現ルール（例: `"/^pwsh.*?git\\s+(status|diff|log|add|commit).*?/"`）に追加した。
  - `git add work_journal.md CHANGELOG_LOCAL.md state_compact.json && git commit -F _tmp\\commit_msg.txt` などの完全一致文字列も追加した。
- **結果：** `git commit` 系のコマンドも自動承認されるよう設定を反映した。
'''

with codecs.open('work_journal.md', 'a', 'utf-8') as f:
    f.write(journal_entry)
