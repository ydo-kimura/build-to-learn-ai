# Business Logic Model: Unit 1 (Linear & Regularized Regression)

## ユースケース (Use Cases)
1. **カリフォルニア住宅価格の予測 (デモンストレーション)**
   - 教師データとしてCalifornia Housing Datasetを用い、各種回帰モデルを構築する。
   - モデルの挙動（特に正則化による重みの変化）を視覚的に理解する。
2. **糖尿病進行度の予測 (自己実践課題)**
   - デモで学んだパイプラインをベースに、ユーザー自身がDiabetes Datasetを用いてモデルを構築し、理解度を確認する。

## 分析パイプライン (Analysis Pipeline)
本Unitのビジネスロジック（処理フロー）は以下のステップで構成される。

1. **データロード (Data Loading)**
   - `sklearn.datasets` から目的のデータを読み込む。
2. **前処理 (Preprocessing)**
   - データを学習用（Train）とテスト用（Test）に分割する（例: 80% / 20%）。
   - 正則化モデル（Ridge, Lasso）を正しく機能させるため、特徴量のスケーリング（`StandardScaler`）を必ず適用する。
3. **モデル学習 (Model Training)**
   - 以下の3つのモデルを学習させる：
     - 通常の線形回帰 (`LinearRegression`)
     - L2正則化 (`Ridge`)
     - L1正則化 (`Lasso`)
4. **評価 (Evaluation)**
   - テストデータを用いて予測を行い、RMSE（二乗平均平方根誤差）と $R^2$ スコア（決定係数）を算出・比較する。
5. **可視化 (Visualization)**
   - 実測値 vs 予測値の散布図を描画し、予測の偏りを確認する。
   - 3つのモデルの「回帰係数（重み）」を棒グラフ等で並べて比較し、Ridge（全体的な縮小）とLasso（スパース化・特徴量選択）の挙動の違いを確認する。
