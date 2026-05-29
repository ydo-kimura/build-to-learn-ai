# Unit 15: ResNet を用いた転移学習

> [!TIP]
> **Google Colab で学習を進める方へ**
> ディープラーニング編（Unit 10〜16）では、計算を高速化するために **GPU の有効化** をおすすめします。設定手順は [Appendix (学習環境とキーの準備)](../appendix/index.md#🚀-1-google-colaboratory-での学習の進め方) を最初にご覧ください。

## 1. Transfer Learning with ResNet の理解

<img src="./images/concept.png" width="400" alt="コンセプト図解">

自分でゼロからCNN（虫眼鏡ネットワーク）を作って学習させるのはとても立派ですが、実はこれには**「膨大なデータ」**と**「途方もない時間（計算力）」**が必要です。

そこで現代のAI開発で最もよく使われるチート技が **「転移学習（Transfer Learning）」** です。

**転移学習は「一流シェフの引き抜き」**

あなたが「究極のオムライス専門店」を開きたいとします。
1. **ゼロから学習**: 素人を雇って、包丁の握り方、火の点け方、卵の割り方から数年かけて教え込む。（Unit 14までやってきたこと）
2. **転移学習**: すでにフランス料理で三ツ星を取っている「一流シェフ」を引き抜き、「オムライスの作り方だけ」を1週間で教え込む。

転移学習では、GoogleやMicrosoftなどの大企業がスーパーコンピュータを使って「世の中のありとあらゆる画像」を学ばせた**「学習済みモデル（一流シェフ）」**をそのままダウンロードして使います。彼らはすでに「丸い形」「エッジ」「動物の毛並み」といった特徴を見抜くプロなので、少しだけ追加の勉強をさせるだけで、あなたの用意した画像を完璧に見分けてくれます。

**一流シェフの一人：ResNet（レスネット）**
数ある学習済みモデルの中でも、歴史的な大発明となったのが**ResNet**です。
ネットワークは「深ければ深いほど賢くなる」と思われていましたが、深すぎると逆に情報が迷子になってバカになるという問題がありました。
ResNetは、「もしこの層を通って迷子になるなら、**層をスキップして近道（ショートカット）すればいいじゃん！**」という超画期的なアイデア（Skip Connection）を取り入れ、100層以上という超巨大で賢いネットワークを実現しました。

### 💡 具体的なビジネスユースケース

- **自社専用の画像検索システム**: ECサイトなどで、自社が扱う数千種類の独自アパレル商品を高精度に見分けられるよう、学習済みモデルをファインチューニングして「画像で検索」機能を実現する。
- **顔認証システム**: 世の中の膨大な顔画像で学習したモデルをベースに、自社の社員の顔だけを少数のデータで追加学習させ、安全で高速なセキュリティゲートを作る。
- **ドローンによるインフラ点検**: 一般的な画像認識能力を持つAIに、橋のひび割れや鉄塔のサビといった特殊な画像を転移学習させ、少数のサンプルデータからでも精度の高い点検AIをスピーディに構築する。

## 2. 実装例 (Implementation Example)

ここでは、PyTorchを使って「ResNet18」という一流シェフを雇い、私たちがやりたい「犬と猫の2値分類（2クラス分類）」専用にカスタマイズ（転移学習）するコードを書いてみましょう。

まずはシェフをインターネットからお呼びします。

```python
import torch
import torch.nn as nn
import torchvision.models as models

# 1. 一流シェフ（学習済みのResNet18）をダウンロードして呼んでくる
# weights=models.ResNet18_Weights.DEFAULT と指定することで、知識が詰まった状態のモデルをダウンロードできます。
resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

print(resnet) # 中身を見ると、膨大な量の層（虫眼鏡）が連なっているのがわかります
```

この一流シェフは、元々「ImageNet」というデータセットで学習しており、**1000種類**の物体を見分けることができます。しかし、私たちがやりたいのは「犬か猫か（**2種類**）」だけです。

そこで、シェフの頭の中の「最後の判断を下す部分（全結合層）」だけをすり替えます。

```python
# 2. シェフの今までの知識（虫眼鏡の部分）を「凍結（Freeze）」する
# 「今まで培った包丁の使い方はそのままでいいよ、変えないでね」という指示です。
for param in resnet.parameters():
    param.requires_grad = False # 勾配計算（学習）をストップする

# 3. 最後の全結合層（推理パート）だけを、2クラス分類用に新しく付け替える
# resnetの最後の層は「fc (Fully Connected)」という名前がついています。
# そこで、元のfc層に入力されるはずだった特徴量の数（in_features）を調べます。
num_features = resnet.fc.in_features 

# 古い1000クラス用の層を捨てて、新しい2クラス用の層をくっつけます！
# 新しく作ったこの層だけは requires_grad = True (学習する) になります。
resnet.fc = nn.Linear(num_features, 2)

print("最後の層が2クラス分類用にすり替わりました！")
print(resnet.fc)
```

準備はこれだけで完了です！あとはこのモデルを使って学習ループを回します。

```python
import torch.optim as optim

# 4. 学習の準備
criterion = nn.CrossEntropyLoss()

# ここがポイント！
# Optimizer（乗り物）には、「新しく付け替えた最後の層 (resnet.fc.parameters())」だけを渡します。
# 凍結した部分は学習させる必要がないためです。
optimizer = optim.Adam(resnet.fc.parameters(), lr=0.001)

# ダミーの画像データ (バッチ:4, カラー3色, 縦:224, 横:224) 
# ※ResNetなどの有名モデルは基本的に 224x224 サイズの画像を前提にしています。
dummy_images = torch.randn(4, 3, 224, 224)
dummy_labels = torch.tensor([0, 1, 0, 1])

# 5. 学習ループ（1回だけ回してみるテスト）
resnet.train()

optimizer.zero_grad()
predictions = resnet(dummy_images) # シェフに予測させる！
loss = criterion(predictions, dummy_labels)
loss.backward()
optimizer.step()

print("\n1回分の学習が完了しました！Loss:", loss.item())
```

**解説:**
たったこれだけのコードで、世界のトップクラスの画像認識AIを自分のタスクに応用できてしまいます！
ポイントは以下の3ステップです。
1. 学習済みモデルを読み込む。
2. 既存の層を「凍結（`requires_grad = False`）」する。
3. 最後の層（`fc` または `classifier` など）を自分のクラス数に合わせて付け替える。

これだけで、数万枚の画像と数日の学習時間がなくても、たった数百枚の画像・数分で超高精度なAIが作れてしまいます。

## 3. 実践 (Practice)

別の超有名モデル「MobileNet V2」を使って転移学習の準備をしてみましょう。
MobileNetは、スマートフォンなどの計算力が低い場所でもサクサク動くように軽量化された優秀なモデルです。

**要件定義:**
- `models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)` を使って学習済みモデルを読み込んでください。
- モデルのすべてのパラメータを凍結（`requires_grad = False`）してください。
- 今回は「10種類の花」を見分けるAIを作りたいとします。
- MobileNet V2の最後の層は `fc` ではなく **`classifier[1]`** という名前になっています。
- 元の層の入力数 (`in_features`) を取得し、出力数が `10` になるように新しい `nn.Linear` にすり替えてください。
- （学習ループは書かなくて大丈夫です。モデルの準備部分だけ書きましょう！）

**ヒント:**
```python
mobilenet = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
# mobilenetの最後はこうなっています
# mobilenet.classifier = nn.Sequential(
#     nn.Dropout(p=0.2),
#     nn.Linear(in_features=1280, out_features=1000) <- これが classifier[1]
# )
```

## 4. 答え合わせ (Answer Key)

<details>
<summary>解答例を見る（クリックで展開）</summary>

```python
import torch
import torch.nn as nn
import torchvision.models as models

# 1. 一流シェフ（軽量級のMobileNet V2）をダウンロード
mobilenet = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

# 2. 既存の知識（パラメータ）をすべて凍結する
for param in mobilenet.parameters():
    param.requires_grad = False

# 3. 最後の層の入力数を調べる
# MobileNet V2では classifier[1] が最後のLinear層です
num_features = mobilenet.classifier[1].in_features

# 4. 10クラス分類用に最後の層をすり替える
mobilenet.classifier[1] = nn.Linear(num_features, 10)

print("転移学習の準備が完了しました！")
print("新しい分類層:", mobilenet.classifier[1])

# --- （おまけ）Optimizerの設定 ---
# 付け替えた層だけを最適化の対象にします
import torch.optim as optim
optimizer = optim.Adam(mobilenet.classifier[1].parameters(), lr=0.001)
```

</details>
