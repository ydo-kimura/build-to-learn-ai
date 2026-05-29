# Business Rules & Constraints: Unit 1

## 技術的制約 (Technical Constraints)
- **環境**: Jupyter Notebook (`.ipynb`) を使用して実装する。
- **ライブラリ**: `scikit-learn` (モデル構築・前処理・評価), `pandas` (データ操作), `matplotlib`/`seaborn` (可視化) を使用する。
- **前処理の必須要件**: RidgeおよびLasso回帰を用いるため、特徴量のスケールを揃えること（標準化: Standardization）を必須とする。これを怠ると、スケールの大きい特徴量に対して正則化ペナルティが不当に強く働いてしまうため。

## 評価ルール (Evaluation Rules)
- **精度評価**: 
  - **RMSE (Root Mean Squared Error)**: 予測誤差の絶対的な大きさを、目的変数と同じ単位で把握するために使用する。
  - **$R^2$ Score (決定係数)**: モデルがデータの分散をどれだけ説明できているかを相対的 (0.0〜1.0) に評価する。
- **解釈性の評価**:
  - 各モデルの係数 (Coefficients) を抽出し、L1正則化（Lasso）によってどの変数がゼロに圧縮（特徴量選択）されたかを明示的に確認しなければならない。

## ワークフロールール (Workflow Rules)
1. **フェーズ1 (AIとのペアプロ)**: AIがCalifornia Housingデータセットを用いた実装を提供・解説し、ユーザーはそれを実行・調整して理解を深める。
2. **フェーズ2 (自己実践)**: Notebookの後半に「自己実践課題 (Assignment)」のセクションを設け、ユーザーが独力でDiabetesデータセットに対して同じパイプラインを適用する。
