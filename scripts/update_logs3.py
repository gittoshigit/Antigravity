import json
import codecs
from datetime import datetime

# Update state_compact.json
with codecs.open('state_compact.json', 'r', 'utf-8') as f:
    state = json.load(f)

timestamp = datetime.now().astimezone().replace(microsecond=0).isoformat()
state['履歴'].append({
    'timestamp': timestamp,
    'event': 'antigravity_ide_regex_commands_added',
    'detail': {
        '実施内容': 'Antigravity IDE の settings.json に対し、残りのコマンドと正規表現ベースのルールを追加した。'
    }
})

with codecs.open('state_compact.json', 'w', 'utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

# Update work_journal.md
journal_entry = f'''
## {datetime.now().strftime('%Y-%m-%d %H:%M')}
### 種別：修正
### フェーズ：運用

- **目的：** Qiita記事等の情報源に基づき、Antigravity IDE上で残りのテスト系・確認系コマンドを自動承認に追加する。
- **実施内容：**
  - settings.json の chat.tools.terminal.autoApprove に対し、記事で紹介されていた pnpm test, yarn test, cargo test, go test ./... などを追加した。
  - IDE側の仕様（VS Codeベース）に合わせ、引数やリダイレクトを許容する正規表現フォーマット（`"/^git\\s+status/" : true` 形式）を追加設定した。
- **結果：** IDE側でも柔軟なコマンド承認が通るよう設定を反映した。
'''

with codecs.open('work_journal.md', 'a', 'utf-8') as f:
    f.write(journal_entry)
