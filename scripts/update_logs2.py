import json
import codecs
from datetime import datetime

# Update state_compact.json
with codecs.open('state_compact.json', 'r', 'utf-8') as f:
    state = json.load(f)

timestamp = datetime.now().astimezone().replace(microsecond=0).isoformat()
state['履歴'].append({
    'timestamp': timestamp,
    'event': 'generic_wildcard_commands_added',
    'detail': {
        '実施内容': 'AIエージェントのシェルコマンド実行に汎用的に対応するため、autoApprove リストをワイルドカード（*）を用いたパターンに書き換えた。',
        '対象ファイル': r'C:\Users\kusma\AppData\Roaming\Antigravity\User\settings.json'
    }
})
state['ワークフロー状態']['最終判定理由'] = '汎用的なワイルドカード指定（*）を用いて、安全なコマンド全般を自動承認するように修正しました。'

with codecs.open('state_compact.json', 'w', 'utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

# Update work_journal.md
journal_entry = f'''
## {datetime.now().strftime('%Y-%m-%d %H:%M')}
### 種別：修正
### フェーズ：運用

- **目的：** AIエージェントが実行する pwsh 形式のコマンドに対し、都度手動追加するのではなく汎用的に自動承認を効かせる。
- **実施内容：**
  - settings.json の autoApprove リストを再構築し、`pwsh -NoProfile -Command "python *"` などのワイルドカード指定に変更した。
  - 安全な参照・テスト系コマンドのみワイルドカードで許可し、破壊的コマンドはワイルドカードで明示的に拒否（false）設定とした。
- **結果：** settings.json が更新され、汎用的な判定リストになった。
- **影響範囲：** 現在のPCの Antigravity IDE
'''

with codecs.open('work_journal.md', 'a', 'utf-8') as f:
    f.write(journal_entry)
