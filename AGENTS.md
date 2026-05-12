# AGENTS.md（共通ルール / Core）

## 目的
- このファイルは、全プロジェクトで常に漏らしてはいけない共通ルールだけを置く。
- 詳細手順、長い運用説明、メモリ運用、記録フォーマット詳細は [AGENTS_DETAIL.md](/D:/program/workspace-meta/AGENTS_DETAIL.md) を参照する。

## 最初に読むもの
1. [SESSION_CORE.md](/D:/program/workspace-meta/SESSION_CORE.md)
2. 対象プロジェクトの `PROJECT.md`
3. 対象プロジェクトの `state_compact.json`
4. 必要なら対象プロジェクトの `RULES.md`

## 条件付きで読むもの
- 横断影響がある、またはその可能性がある:
  [GLOBAL_ACTIVE.md](/D:/program/workspace-meta/GLOBAL_ACTIVE.md)
- 横断変更の履歴や経緯まで必要:
  [GLOBAL_CHANGES.md](/D:/program/workspace-meta/GLOBAL_CHANGES.md)
- 長い運用詳細、メモリ運用、詳細手順が必要:
  [AGENTS_DETAIL.md](/D:/program/workspace-meta/AGENTS_DETAIL.md)

## 絶対ルール
- 回答、記録、確認は日本語で行う。
- 秘密情報の実値を `AGENTS.md` / `PROJECT.md` / `RULES.md` / `docs/*.md` に書かない。
- 本番変更、削除、上書き、認証情報利用、外部公開設定変更は、ユーザー承認なしに実行しない。
- 作業開始の入口は、対象プロジェクト直下の `PROJECT.md` とする。
- 作業状態の主軸は `state_compact.json` とする。
- `state_compact.json` がある場合、`current_status.md` の再読込は不要。
- `work_journal.md` は全文を読まず、必要時のみ末尾を確認する。
- 生ログは原則そのまま渡さず、`summary` / `errors` を優先する。

## 横断影響の判定
- 次のいずれかに触れる場合は、横断影響ありとして [GLOBAL_ACTIVE.md](/D:/program/workspace-meta/GLOBAL_ACTIVE.md) を確認する。
  - ネットワーク、FW、DNS、DHCP、VPN
  - OS 全体設定、共有 Python 環境、共通サーバ
  - 共通認証、共有ストレージ、共通ポート
  - テンプレート、共通スクリプト、複数案件で使う設定
- 影響が不明な場合も横断影響ありとして扱う。

## AI の役割要約
- Codex: 分類、実装、環境検証、実機検証主導
- Claude: 計画、設計、レビュー、静的検証
- Gemini: Web リサーチ、最新仕様確認
- Human: 承認、実機操作補助、最終判断

## Windows 共通ルール
- このワークスペースの標準実行環境は Windows ネイティブとする。WSL は、Human が明示した場合のみ例外として扱う。
- 長い出力、ログ、差分、ビルド結果、テスト結果は、可能なら要約して扱う。
- ローカル LLM が使える環境では、長文の圧縮・分類・候補出しに活用する。既定モデルは `gemma3:12b` を優先し、使えない場合だけ代替手段に切り替える。
- Codex / Claude Code / Gemini に共通で効かせる運用ルールは、この `workspace-meta` 配下に集約する。プロジェクト個別の例外が必要な場合だけ `PROJECT.md` や `RULES.md` に追記する。
- 迷った場合は、まずこの `AGENTS.md` と `SESSION_CORE.md` を優先して読む。

## AI CLI 利用前提
- この環境では `Claude Code CLI` と `Gemini CLI` を実行可能な相談手段として扱う。
- 共通前提と基本ルールは [SESSION_CORE.md](/D:/program/workspace-meta/SESSION_CORE.md) の `環境前提` を参照する。
- 再利用可能な相談手順はスキル `ai-cli-consult` を参照する。

## 継続性のルール
- 作業単位が完了したら `state_compact.json` を更新する。
- 人間向け履歴が必要な変更は `work_journal.md` に追記する。
- プロジェクト固有の決定、設定変更、障害対応、調査結果を後で再利用したい場合は `memory_data/projects/*.json` にも記録する。
- 横断影響が残る変更は `GLOBAL_CHANGES.md` に記録する。

## 詳細の参照先
- 詳細手順と例外規定: [AGENTS_DETAIL.md](/D:/program/workspace-meta/AGENTS_DETAIL.md)
- 現在有効な横断制約: [GLOBAL_ACTIVE.md](/D:/program/workspace-meta/GLOBAL_ACTIVE.md)

## コミット規約
- コミットが必要な作業では、必ず `git-committer` スキルを使う。
- `git commit` を直接実行せず、スキルの手順に従って事前確認と日本語コミットメッセージ生成を行う。
