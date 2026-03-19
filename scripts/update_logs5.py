import json
import codecs
from datetime import datetime

# Update work_journal.md
journal_entry = f'''
## {datetime.now().strftime('%Y-%m-%d %H:%M')}
### 種別：修正
### フェーズ：運用

- **目的：** `git add` を含むコマンドがAntigravity IDEで承認待ちになってしまう問題の対応。
- **実施内容：**
  - これまで `git status` や `git diff` といった読み取り専用のGitコマンドのみを正規表現の許可リストに入れていたが、`git add` も自動承認の対象とするため `chat.tools.terminal.autoApprove` の正規表現ルール（例: `"/^pwsh.*?git\\s+(status|diff|log|add).*?/"`）に `add` を追加した。
  - 念のため `git add .; git status` などの完全一致文字列も追加した。
- **結果：** `git add` 系のコマンドも自動承認されるよう設定を反映した。
'''

with codecs.open('work_journal.md', 'a', 'utf-8') as f:
    f.write(journal_entry)
