# Unit 1: Linear & Regularized Regression - Functional Design Plan

## 実行計画 (Execution Plan)
- [x] Q1〜Q3への回答の分析と曖昧さの解消
- [x] ビジネスロジックとユースケースの定義 (`business-logic-model.md`)
- [x] 分析プロセスと評価ルール（制約）の定義 (`business-rules.md`)
- [x] データ構造（データセット）の定義 (`domain-entities.md`)

## ユーザーへの確認事項 (Clarification Questions)

**Q1: データセットの選定について**
線形回帰のPoCとしてどのデータセットを使用したいですか？（Scikit-learn標準のCalifornia Housing Datasetが回帰の標準的なベンチマークとして推奨されます）
A. California Housing Dataset（カリフォルニアの住宅価格予測）
B. Diabetes Dataset（糖尿病の進行度予測）
C. その他（具体的に指定してください）
[Answer]: A を説明に使い実践し、B は独力で実装するのに利用。

**Q2: 実装のフォーマットについて**
コードの実装と検証はどの形式で行うのがご希望ですか？
A. Jupyter Notebook (`.ipynb`) - グラフの描画や学習過程をステップバイステップで確認しやすく、学習用のPoCに最適（推奨）
B. 標準的なPythonスクリプト (`.py`) - `src/` や `tests/` などのディレクトリを切ってモジュールとして実装
[Answer]: A

**Q3: 評価指標と可視化について**
実装時に出力・確認したい項目はどれですか？（デフォルトは「全て」を推奨します）
A. 評価指標（RMSE, R2スコアなど）の計算と出力
B. 実測値と予測値の散布図（Matplotlibでの可視化）
C. 線形回帰、Ridge、Lassoの各モデルの「重み（係数）」の比較グラフ（正則化の効果を視覚的に確認するため）
D. 全て
[Answer]: D

