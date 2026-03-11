# 設計書：Antigravity IDE ターミナル自動承認設定の導入

---

## 0. 管理情報

| 項目 | 内容 |
|------|------|
| ドキュメントパス | `docs/DESIGN.md` |
| ステータス | **レビュー待ち（実装前承認が必要）** |
| 作成日 | 2026-03-11 |
| 対象プロジェクト | Antigravity |
| 参照資料 | `docs/RESEARCH.yaml` |

### 実装前承認条件

以下の条件をすべて満たした場合のみ、実装（settings.json 変更）を行うこと。

1. 本設計書の内容を人間レビュー担当者が確認し、承認コメントを残していること
2. `autoApprove` に列挙するコマンドリストの内容について、担当者が安全性を確認していること
3. 既存 `settings.json` のバックアップが取得済みであること

## 1. 目的

Google Antigravity IDE において、AIエージェントがターミナルコマンドを実行する際の確認ダイアログを、安全なコマンドに限り省略できるようにする。これにより、確認・参照・テスト系の反復作業における操作コストを削減し、エージェント主導の開発フローを改善する。

## 2. 要求事項

| ID | 要求内容 |
|----|----------|
| REQ-01 | ターミナル自動承認機能を有効化する（`chat.tools.terminal.enableAutoApprove: true`） |
| REQ-02 | 安全な確認・テスト系コマンドのみを自動承認対象とする |
| REQ-03 | 破壊的コマンド・インストール系コマンドは自動承認対象に含めない |
| REQ-04 | 変更後も既存 `settings.json` の他キーをすべて保持すること |
| REQ-05 | 設定変更は `%APPDATA%\Antigravity\User\settings.json` に対して行う |

## 3. 制約

- **プラットフォーム**: Windows 11（`%APPDATA%` パスを使用）
- **IDEベース**: VS Code ベースの Antigravity IDE に限定した設定である
- **破壊的・インストール系コマンドの除外**: `rm`、`del`、`rmdir`、`npm install`、`pip install`、`winget install`、`choco install` 等は自動承認対象に含めてはならない
- **既存設定の保持**: `settings.json` への書き込みは既存キーを上書き・削除しない方法で行うこと（JSON マージ）
- **バックアップ必須**: 変更前に `settings.json` のバックアップを取得すること

## 4. 実装対象

### 4.1 追加・更新するキー

```json
{
  "chat.tools.terminal.enableAutoApprove": true,
  "chat.tools.terminal.autoApprove": {
    "git status": true,
    "git log": true,
    "git diff": true,
    "git branch": true,
    "git show": true,
    "ls": true,
    "dir": true,
    "cat": true,
    "type": true,
    "echo": true,
    "pwd": true,
    "cd": true,
    "python --version": true,
    "node --version": true,
    "npm --version": true,
    "pytest": true,
    "python -m pytest": true,
    "npm test": true,
    "npm run test": true,
    "npm run build": true,
    "npm run lint": true,
    "rm": false,
    "del": false,
    "rmdir": false,
    "rd": false,
    "npm install": false,
    "pip install": false,
    "winget install": false,
    "choco install": false,
    "curl": false,
    "wget": false,
    "Invoke-WebRequest": false,
    "format": false,
    "mkfs": false
  },
  "chat.tools.terminal.outputLocation": "none"
}
```

### 4.2 自動承認対象とする根拠

| コマンド分類 | 自動承認 | 理由 |
|-------------|---------|------|
| git 参照系（status/log/diff/branch/show） | true | 読み取り専用・副作用なし |
| ファイル一覧・内容参照（ls/dir/cat/type） | true | 読み取り専用・副作用なし |
| バージョン確認（--version） | true | 読み取り専用 |
| テスト実行（pytest/npm test） | true | 既存コードの検証のみ |
| ビルド・Lint（npm run build/lint） | true | ファイル生成のみ、破壊的でない |
| ファイル削除（rm/del/rmdir） | false | 破壊的、復元不可のリスク |
| パッケージインストール（npm install 等） | false | 環境変更・セキュリティリスク |
| ネットワーク取得（curl/wget 等） | false | 外部通信・意図しない実行リスク |
| ディスク操作（format/mkfs） | false | 破壊的操作 |

## 5. 非対象

- `settings.json` の他キー（例: `claudeCode.allowDangerouslySkipPermissions` 等）の変更・削除
- Antigravity IDE 本体のアップデートや再インストール
- `chat.tools.terminal.autoApprove` に列挙されていないコマンドのデフォルト動作変更
- ユーザーごとのプロファイル管理（本設定はユーザー全体設定）
- リモートサーバーや WSL 環境向け設定

## 6. 変更対象ファイル

| ファイルパス | 変更種別 | 備考 |
|-------------|---------|------|
| `%APPDATA%\Antigravity\User\settings.json` | キー追加（マージ） | 既存キーは保持すること |

## 7. 実装手順

1. **バックアップ取得**（手動・人間が実施すること）
   ```
   %APPDATA%\Antigravity\User\settings.json
   → settings.json.bak として同ディレクトリにコピー
   ```

2. **現在の settings.json を読み込む**
   - ファイル全体を読み込み、既存のキー一覧を確認する

3. **対象キーの存在確認**
   - `chat.tools.terminal.enableAutoApprove` が未設定であることを確認する
   - `chat.tools.terminal.autoApprove` が未設定であることを確認する

4. **キーの追加（マージ）**
   - 「4.1 追加・更新するキー」の内容を既存 JSON にマージする
   - 既存キーは一切削除・上書きしないこと

5. **保存**
   - UTF-8（BOM なし）で保存する
   - JSON として構文エラーがないことを検証してから保存する

6. **動作確認**（後述テスト観点を参照）

## 8. テスト観点

| ID | テスト内容 | 合格条件 |
|----|-----------|---------|
| T-01 | `settings.json` が有効な JSON であること | `JSON.parse` またはエディタの構文チェックでエラーなし |
| T-02 | 既存キーが保持されていること | 変更前後のキー一覧を diff で比較し、削除・変更がないこと |
| T-03 | `enableAutoApprove` が `true` に設定されていること | キーの値を目視確認 |
| T-04 | `autoApprove` リストに破壊的コマンドが `false` で登録されていること | `rm`/`del`/`npm install` 等が `false` であることを確認 |
| T-05 | Antigravity IDE 再起動後に設定が反映されること | IDE を再起動し、ターミナルで `git status` を実行して確認ダイアログが表示されないこと |
| T-06 | `rm` コマンド実行時に確認ダイアログが表示されること | エージェントから `rm` を発行し、承認ダイアログが出ることを確認 |

## 9. リスク

| リスク | 深刻度 | 対策 |
|--------|--------|------|
| `autoApprove: true` のコマンドがスクリプト経由で悪用される | 中 | 承認対象は読み取り・検証系のみに限定。定期的に見直す |
| JSON 書き込みミスによる settings.json の破損 | 高 | 事前バックアップ必須。書き込み前に構文チェックを実施 |
| 想定外のコマンドが自動承認される（コマンド名の前方一致等） | 中 | IDE の一致方式を事前に確認し、必要に応じて完全一致設定を使用 |
| settings.json の他キー消失 | 高 | JSON マージによる追加のみを行い、既存キーを保持する実装とする |
| IDE バージョンアップによるキー名変更 | 低 | アップデート時に設定キーの変更有無を確認する運用を設ける |

## 10. codexへの実装指示

以下の指示を Codex（または実装エージェント）に渡すこと。**人間レビュー・承認完了後に実行すること。**

### 実装タスク

**前提条件の確認**
- 実装前に人間レビュー担当者の承認が得られていることを確認すること
- `settings.json` のバックアップが取得済みであることを確認すること

**実装内容**

1. `%APPDATA%\Antigravity\User\settings.json` を読み込む
2. 既存の JSON オブジェクトに、以下のキーをマージ（追加）する。既存のキーは一切変更・削除しないこと

```json
{
  "chat.tools.terminal.enableAutoApprove": true,
  "chat.tools.terminal.autoApprove": {
    "git status": true,
    "git log": true,
    "git diff": true,
    "git branch": true,
    "git show": true,
    "ls": true,
    "dir": true,
    "cat": true,
    "type": true,
    "echo": true,
    "pwd": true,
    "cd": true,
    "python --version": true,
    "node --version": true,
    "npm --version": true,
    "pytest": true,
    "python -m pytest": true,
    "npm test": true,
    "npm run test": true,
    "npm run build": true,
    "npm run lint": true,
    "rm": false,
    "del": false,
    "rmdir": false,
    "rd": false,
    "npm install": false,
    "pip install": false,
    "winget install": false,
    "choco install": false,
    "curl": false,
    "wget": false,
    "Invoke-WebRequest": false,
    "format": false,
    "mkfs": false
  },
  "chat.tools.terminal.outputLocation": "none"
}
```

3. マージ後の JSON が構文的に正しいことを確認する
4. UTF-8（BOM なし）で `settings.json` に上書き保存する
5. 保存後、既存キーが保持されていることを diff で確認し、結果を報告する

**禁止事項**
- 既存キーの削除・変更
- `npm install`、`pip install`、`winget install` 等のインストール系コマンドの実行
- `rm`、`del`、`format` 等の破壊的コマンドの実行
- バックアップなしでの上書き
