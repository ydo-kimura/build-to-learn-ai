# Requirements Clarification Questions

AIエージェントおよびフィジカルAI分野への転職に向けた戦略とポートフォリオ作成について、具体的な要件を明確にするための質問です。各質問の `[Answer]:` の後に該当する選択肢のアルファベットを記入してください。

## Question 1: 最優先で取り組みたい活動
言葉以外で実力を示すために、まずどの活動から重点的に始めたいですか？

A) プロダクト・サービス開発（ゼロからの個人開発）
B) 既存OSSへのコントリビュート
C) 技術ブログなどのライティング活動
D) 複数並行して進めたい（全体戦略の策定を優先）
X) その他 (以下に詳細を記述してください)

[Answer]: D

## Question 2: 注力したい技術領域
「AIエージェント」と「フィジカルAI」のうち、より強くアピールしたい、または最初に取り組みたい領域はどちらですか？

A) AIエージェント（LLMを活用した自律型エージェント、ツール利用、RAGなど）
B) フィジカルAI（ロボティクス、エッジデバイスでの推論、ROS連携など）
C) 両方の掛け合わせ（現実世界とインタラクトするAIエージェント）
X) その他 (以下に詳細を記述してください)

[Answer]: X (まずは A。ただ B や C にもおいおい取り組みたい。)

## Question 3: 開発の主な技術スタック（希望）
プロダクト開発やOSS活動を行うにあたり、メインで使用したい言語や技術スタックは何ですか？

A) Pythonメイン（LangChain, LlamaIndex, ROS 2 など）
B) TypeScript/JavaScriptメイン（Next.js, Node.js など）
C) C++/Rustなど（パフォーマンス重視の組み込み・ロボティクス向け）
X) その他 (以下に詳細を記述してください)

[Answer]: X (現状Aが全く取り組めていないのと一番のアピールになるので、Aが最優先。B と Rust も適宜。)

## Question 4: Security Extensions
Should security extension rules be enforced for this project?

A) Yes — enforce all SECURITY rules as blocking constraints (recommended for production-grade applications)
B) No — skip all SECURITY rules (suitable for PoCs, prototypes, and experimental projects)
X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 5: Property-Based Testing Extension
Should property-based testing (PBT) rules be enforced for this project?

A) Yes — enforce all PBT rules as blocking constraints (recommended for projects with business logic, data transformations, serialization, or stateful components)
B) Partial — enforce PBT rules only for pure functions and serialization round-trips (suitable for projects with limited algorithmic complexity)
C) No — skip all PBT rules (suitable for simple CRUD applications, UI-only projects, or thin integration layers with no significant business logic)
X) Other (please describe after [Answer]: tag below)

[Answer]: C
