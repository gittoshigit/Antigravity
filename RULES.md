# RULES.md（プロジェクト固有ルール）

> **このファイルの位置づけ：** AGENTS.md の思想を前提とし、このプロジェクトだけの固有ルールを記載する。
> AGENTS.md と重複するルールは書かない。

---

## プロジェクトの目的
-

---

## 前提環境・構成
- 対象ディレクトリ：
- 使用言語・ツール：
- 実行環境（ローカル / サーバ / 本番 等）：

---

## このプロジェクト特有の重要ルール
- Codex は進行役であっても、自身の担当成果物以外を確定成果物として作成・更新してはならない。
- `state_compact.json` の `現在ステップ` と `現在の担当エージェント` が示す担当範囲を優先し、担当外フェーズの成果物編集を禁止する。
- 次工程へ進む前に、前工程の成果物作成者と承認状態を確認し、条件未達なら停止して Human に報告する。
- 編集前には「現在フェーズ」「担当エージェント」「これから更新するファイルが担当範囲内か」を必ず確認し、1つでも外れたら編集しない。

---

## 禁止事項（このプロジェクト特有）
- Codex が `docs/DESIGN.md` を正式成果物として新規作成・更新すること
- Claude による設計書未作成の状態で、Codex が `state_compact.json` を `design completed` として進めること
- `承認.設計承認 = false` のまま Codex が実装ファイルや `docs/PATCH.yaml` の作成に着手すること
- フェーズ境界を越える編集を、Human への確認なしで行うこと

---

## マルチAIエージェントの役割分担と指示（このプロジェクト固有）

本プロジェクトでは、Codex を進行役とする自動オーケストレーション方式で開発を行う。
各AIエージェントは自身の役割の範囲外の作業を行わず、成果物の契約に従って受け渡しすること。

* **Gemini CLI (Research)**
    * **役割:** 事実調査、前提確認、関連情報の収集、要件の論点整理。
    * **指示:** `PROJECT.md` を起点に必要情報を読み込み、設計に渡すための調査結果を `docs/RESEARCH.yaml` に作成・更新すること。独自の設計確定や実装は行わない。
* **Claude (Planning / Design)**
    * **役割:** `docs/RESEARCH.yaml` に基づく計画策定、要件整理、設計書作成、実装方針の明確化。
    * **指示:** 作業後は `docs/DESIGN.md`（設計書）を作成・更新すること。設計段階では実装コードの直接編集は行わない。
* **Codex CLI (Implementation)**
    * **役割:** `docs/DESIGN.md` に基づくコード実装、変更ファイルの整理、実行手順の明記。
    * **指示:** 独自の仕様変更は禁止。作業後は `docs/PATCH.yaml` を作成・更新し、実装内容と未対応事項を明記すること（YAML形式）。
* **Claude Code (Patch Verification)**
    * **役割:** テスト、動作確認、エラーログ解析、PASS/FAIL判定、戻し先の明示。
    * **指示:** `docs/DESIGN.md` と `docs/PATCH.yaml` を読み込み、検証後は `docs/VERIFY.md` を作成・更新すること。仕様変更や本実装の追加は原則行わず、修正提案に留めること。
* **Human / としあきさん (Final Approval)**
    * **役割:** 実機検証、AIの無限ループ監視、承認境界の判断、最終承認。

### 推奨実行形態
- 標準運用では、**Codex 本体がオーケストレーターを兼ねる**。
- Human は要件や補足情報を Codex に渡し、Codex が必要な調査・設計・実装・検証の順序を判断する。
- Gemini による調査が必要な場合は、Codex が不足論点を明示して `docs/RESEARCH.yaml` の整備を促す。
- Codex は Claude CLI を使って `docs/DESIGN.md` と `docs/VERIFY.md` を生成または更新し、自身は実装と `docs/PATCH.yaml` 更新を直接担当する。
- `orchestrator.py` は使用しない。状態遷移の管理責任は `state_compact.json` を更新する Codex が持つ。

### docs 契約（固定）
- `docs/RESEARCH.yaml` の必須キー: purpose / facts / unresolved / design_handoff（YAML形式・AI間受け渡し専用）
- `docs/DESIGN.md` の必須章: 管理情報 / 目的 / 要求事項 / 制約 / 実装対象 / 非対象 / 変更対象ファイル / 実装手順 / テスト観点 / リスク / codexへの実装指示
- `docs/PATCH.yaml` の必須キー: design_id / result / reason / summary / changed_files / verify_request（YAML形式・AI間受け渡し専用）
- `docs/VERIFY.md` の必須章: 管理情報 / 検証対象 / 検証結果 / PASS / FAIL 判定 / 発見した問題 / 原因推定 / 戻し先 / 修正提案 / 再検証条件
- `docs/VERIFY.md` の管理情報には、`判定コード` / `失敗分類` / `戻し先コード` を必須とする

### 秘密情報と承認境界
- 実パスワード・APIキー・秘密鍵・接続文字列の実値は `SECRETS_LOCAL.md` または `.env` にのみ置く。
- 各AIの参照範囲は `ACCESS_POLICY.md` に従う。
- 本番変更、削除、上書き、認証情報利用、外部公開設定変更は、ユーザー承認がある場合のみ実行する。

---

## フェーズ固定型運用ルール（AI最適化）

### 基本方針
- **1セッション = 1フェーズ**を原則とする。
- フェーズは `PROJECT.md` の「現在の作業フェーズ」で宣言し、セッション中は変更しない。
- フェーズを跨ぐ作業が発生した場合は、一旦作業を止めてユーザーに確認する。

### フェーズ定義
| フェーズ | AIが行うこと | AIが行わないこと |
|----------|-------------|-----------------|
| 調査 | 情報収集・分析・報告 | コード変更・設定変更 |
| 実装 | コード生成・ファイル作成 | 本番環境への適用 |
| 修正 | バグ修正・設定修正 | 新機能の追加 |
| 検証 | テスト実行・結果確認 | 本番への反映 |
| 運用 | 監視・定期メンテ | 大規模な変更 |

---

## AI情報最小化ルール（このプロジェクト固有の補足）

### ログ渡しのルール
- AIには **`artifacts/summary.txt` / `artifacts/errors.txt` のみ**を渡す。生ログ・フルログは渡さない。
- ログ収集には `collectdiag` スキルを使用する（生ログを直接貼り付けない）。
- コンテキスト再送信禁止：一度渡した情報は再送しない。変更差分のみ伝える。

### 状態管理のルール
- `state_compact.json` を状態の主軸とする。
- `state_compact.json` がある場合、`current_status.md` の再読み込みは不要。
- AI切り替え・スレッド切り替え時は `state_compact.json` を最初に渡す。
- `state_compact.json` はメモではなく状態機械として扱い、`現在ステップ` / `次ステップ` / `失敗分類` / `再実行可否` を更新する。
- Codex 主導の自動オーケストレーション運用時も、`現在の担当エージェント` と `次のアクション` を必ず最新化する。

### FAIL分類と戻し先ルール
| 失敗分類 | 意味 | 戻し先 |
|----------|------|--------|
| `design` | 調査不足・設計矛盾・前提未定義 | Gemini または Claude |
| `implementation` | 実装不足・コード不備・PATCH不整合 | Codex |
| `environment` | 環境依存・外部サービス・権限不足 | Human |
| `approval` | 承認待ち・判断待ち | Human |
| `unknown` | 自動判定不能 | Human |
| `none` | 問題なし | None |

### 再実行ルール
- `失敗分類=implementation` かつ `再実行可否=true` の場合のみ、Codex への再実行候補とする。
- `失敗分類=design` は Gemini の再設計完了まで次フェーズへ進めない。
- `失敗分類=environment` または `approval` は Human 判断が入るまで自動再試行しない。
- `max_step_count` を超える連続試行は禁止し、Human に停止報告する。

---

## ログ・運用ルール

| ファイル | 用途 | 更新タイミング |
|----------|------|----------------|
| `state_compact.json` | AI向け最小状態（主軸） | 作業単位完了ごと |
| `current_status.md` | 人間向け現状サマリー（上書き） | 状態変化時 |
| `work_journal.md` | 人間向け作業ログ（追記専用） | 作業単位完了ごと |
| `CHANGELOG_LOCAL.md` | 影響が残る変更の台帳（追記） | 設定/運用変更時 |
| `<meta>/GLOBAL_CHANGES.md` | 横断影響ログ | 横断影響が生じた時 |

### どこに書くか（判断ルール）
- AIへの状態引き継ぎ：`state_compact.json`
- 人間向けの現状確認・更新：`current_status.md`
- 直近の作業状況・次アクション：`work_journal.md`
- 影響が残る変更（再現性/ロールバック必要）：`CHANGELOG_LOCAL.md`
- 環境全体に影響（FW/DNS/OS/共有資源）：`<meta>/GLOBAL_CHANGES.md`

---

## 成果物漏れ防止ルール（このプロジェクト固有）
- 設計フェーズを完了する場合、`docs/RESEARCH.yaml` / `docs/DESIGN.md` の作成または更新を必須とする。
- 実装フェーズを完了する場合、`docs/PATCH.yaml` の作成または更新を必須とする。
- 検証フェーズを完了する場合、`docs/VERIFY.md` の作成または更新を必須とする。
- `docs/PATCH.yaml` には、対象設計ID、変更ファイル、検証依頼を必ず含める。
- 実装完了報告の前に、`state_compact.json` と `work_journal.md` を必ず更新する。

### Codex オーケストレーション時の承認ルール
- Human から Codex へ要件、調査結果、または「この設計で進めてよい」という承認が渡された場合、Codex はそれを次フェーズ着手の入力として扱ってよい。
- ただし、本番反映、削除、上書き、認証情報利用、外部公開設定変更は従来どおり Human の明示承認が必要とする。
- Claude CLI は設計と検証の補助に使ってよいが、最終的なコード編集責任は Codex が持つ。

### フェーズ境界ゲート
- Research 完了時点で `docs/RESEARCH.yaml` が揃っていても、Codex は `docs/DESIGN.md` を書かず、Claude へ渡す入力整理までで停止する。
- Design 完了と見なせる条件は、`docs/DESIGN.md` が存在し、作成者が Claude であり、Human が設計承認した場合に限る。
- 上記条件が満たされるまで、Codex は実装着手、`docs/PATCH.yaml` 更新、`state_compact.json` の implementation 進行を行わない。
- Verify 完了前に、Codex は `docs/VERIFY.md` を確定成果物として作成・更新しない。

### 編集前チェック
- 1. `state_compact.json` の `現在ステップ` を確認する
- 2. `state_compact.json` の `現在の担当エージェント` を確認する
- 3. 更新対象ファイルが自分の担当成果物か確認する
- 4. 必要な承認フラグが true か確認する
- 5. 1つでも満たさない場合は編集せず停止し、Human に確認する
