# Domain Entities (Datasets): Unit 1

本Unitでは、以下の2つのデータセット（エンティティ）を扱う。

## 1. California Housing Dataset (デモ用)

カリフォルニアの各ブロックグループごとの国勢調査データに基づき、住宅価格の中央値を予測する。

- **取得方法** : `sklearn.datasets.fetch_california_housing`
- **サンプル数** : 20,640
- **特徴量 (Features - 8次元)** :
  - `MedInc`: ブロックの世帯収入の中央値
  - `HouseAge`: 住宅の築年数の中央値
  - `AveRooms`: 1世帯あたりの平均部屋数
  - `AveBedrms`: 1世帯あたりの平均寝室数
  - `Population`: ブロックの人口
  - `AveOccup`: 1世帯あたりの平均構成人数
  - `Latitude`: 緯度
  - `Longitude`: 経度
- **目的変数 (Target)** :
  - `MedHouseVal`: 住宅価格の中央値 (10万ドル単位)

## 2. Diabetes Dataset (自己実践用)

糖尿病患者のベースラインデータから、1年後の疾患進行状況を予測する。

- **取得方法** : `sklearn.datasets.load_diabetes`
- **サンプル数** : 442
- **特徴量 (Features - 10次元)** :
  - `age`: 年齢
  - `sex`: 性別
  - `bmi`: ボディマス指数 (BMI)
  - `bp`: 平均血圧
  - `s1` 〜 `s6`: 6種類の血清測定値
- **目的変数 (Target)** :
  - ベースラインから1年後の疾患進行度（定量的な指標）
