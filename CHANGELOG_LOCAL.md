# CHANGELOG_LOCAL.md（プロジェクト内の影響台帳）

## 目的
- プロジェクト内で「運用や再現性に影響する変更」を短文で台帳化する。
- `work_journal.md` は近況と次アクションに集中させ、経緯・試行錯誤はフルログへ退避する。
- AIにはこのファイルを丸ごと渡さない。関連エントリのみ抜粋して渡す。

---

## 運用ルール
- 記載は事実のみ（長文禁止・感想・経緯は書かない）。
- 影響がプロジェクト横断（FW/DNS/OS/共有資源）に及ぶ場合は、必ず `<meta>/GLOBAL_CHANGES.md` へも記載する。
- 「次回の更新で反映漏れすると危険」なもの（運用上書き/設定/サービス起動オプション）を優先的に記載する。
- AI情報最小化：このファイル全文をAIに渡す必要はない。必要なエントリのみ渡すこと。

---

## 記載フォーマット（簡潔）

```md
## YYYY-MM-DD
- 種別：運用 / 設定 / コード / DB / ドキュメント / その他
- 変更内容：
- 影響：
- ロールバック：
- 確認方法：
- 関連：
```

---

## 2026-03-11
- 種別：ドキュメント / 初期化
- 変更内容：手動コピー後に `create_project.py` を実行し、状態ファイルを新規プロジェクト向けに初期化
- 影響：当該プロジェクト内
- ロールバック：必要ならテンプレートを再コピーし、再度初期化する
- 確認方法：`state_compact.json` / `current_status.md` / `work_journal.md` の初期状態確認
- 関連：`work_journal.md` 初期化エントリ

## 2026-03-11
- 種別：設定
- 変更内容：`C:\\Users\\kirishima04\\AppData\\Roaming\\Antigravity\\User\\settings.json` に `chat.tools.terminal.*` の自動承認設定を追加
- 影響：Antigravity IDE のターミナル確認ダイアログ挙動
- ロールバック：`settings.json.bak_20260311_160333` を `settings.json` に戻す
- 確認方法：`settings.json` の追加キー確認、および IDE 上で `git status` / `rm` の挙動確認
- 関連：`docs/DESIGN.md` / `docs/PATCH.yaml`

## 2026-03-11
- 種別：設定
- 変更内容：`settings.json` の `autoApprove` リストに PowerShell 系コマンド（`Get-Location`, `Get-ChildItem`, `Get-Content` 等）を追加
- 影響：PowerShell コマンド実行時の確認ダイアログ挙動
- ロールバック：`settings.json.bak_20260311_215128` 等のバックアップから復元
- 確認方法：`settings.json` の `autoApprove` リスト確認
- 関連：`docs/DESIGN.md` / `docs/PATCH.yaml` / `scripts/apply_settings.py`

## 2026-03-21
- 種別：設定
- 変更内容：`C:\\Users\\kusma\\AppData\\Roaming\\Antigravity\\User\\settings.json` の `chat.tools.terminal.autoApprove` に `ssh` 全体をコマンドライン全体一致で許可するルールを追加
- 影響：Antigravity IDE における全 SSH 実行時の確認ダイアログ挙動
- ロールバック：当該 `"/^ssh\\b.*$/"` ルールを削除する
- 確認方法：Antigravity IDE 上で `ssh noteserver-ubuntu "find ~/ffxi_server -name '*.conf'"` などの SSH コマンドを実行して承認要求有無を確認
- 関連：`work_journal.md` / `state_compact.json`

## 2026-05-12
- 種別：ドキュメント / 運用
- 変更内容：共通テンプレートを 2026-04-07 版へ更新。
- 影響：プロジェクトの標準ワークフロー強化。
- ロールバック：git restore で以前の状態に戻す。
- 確認方法：各ファイルの更新内容確認。
- 関連：work_journal.md 2026-05-12
