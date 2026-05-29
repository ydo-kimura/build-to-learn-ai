# Unit 15: Transfer Learning with ResNet

<p class="unit-hero">
  <img src="/en/assets/units/unit15_transfer_learning/images/hero.png" alt="Hero: Transfer Learning" />
</p>

> [!TIP]
> **For learners using Google Colab**
> For the deep learning section (Units 10–16), we recommend **enabling a GPU** to speed up computation. See [Appendix (Learning Environment and API Setup)](../appendix/index.md#🚀-1-learning-with-google-colaboratory) for setup steps first.

## 1. Understanding Transfer Learning with ResNet

<img src="/en/assets/units/unit15_transfer_learning/images/diagram-concept.svg" alt="Diagram: Transfer learning" class="unit-diagram" />

Building and training a CNN from scratch is admirable, but it requires **massive data** and **enormous time (compute)**.

The cheat technique most used in modern AI development is **transfer learning**.

**Transfer learning is like "hiring a top chef"**

Suppose you want to open the ultimate omurice specialty restaurant.

1. **Train from scratch**: Hire a beginner and teach knife skills, fire control, and how to crack eggs over several years. (What you did through Unit 14.)
2. **Transfer learning**: Poach a Michelin three-star French chef and teach only "how to make omurice" in one week.

In transfer learning, you download a **pretrained model (top chef)** that big companies like Google and Microsoft trained on supercomputers with "every kind of image in the world." They already detect round shapes, edges, and animal fur—so with a little extra training, they classify your images perfectly.

**One top chef: ResNet**
Among pretrained models, **ResNet** was a historic breakthrough.
People assumed deeper networks were smarter, but too much depth made information get lost and performance collapsed.
ResNet introduced **skip connections**—"if this layer makes you get lost, just skip it and take a shortcut!"—enabling 100+ layer networks that actually work.

### 💡 Concrete Business Use Cases

- **Custom image search**: Fine-tune a pretrained model so an e-commerce site can distinguish thousands of proprietary apparel SKUs for "search by image."
- **Face authentication**: Start from a model trained on huge face datasets and add a few samples of your employees for a fast, secure gate.
- **Drone infrastructure inspection**: Transfer general vision ability to cracks in bridges or rust on towers and build accurate inspection AI from few samples.

<img src="/en/assets/units/unit15_transfer_learning/images/diagram-workflow.svg" alt="Diagram: ResNet18 flow" class="unit-diagram" />

## 2. Implementation Example

Here you will use PyTorch to hire **ResNet18**, a top chef, and customize it for **binary dog-vs-cat classification**.

First, call the chef from the internet.

```python
import torch
import torch.nn as nn
import torchvision.models as models

# 1. Download pretrained ResNet18
# weights=models.ResNet18_Weights.DEFAULT loads ImageNet-trained weights
resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

print(resnet) # Many stacked layers (conv blocks)
```

This chef was trained on ImageNet and can distinguish **1000** object classes. You only need **2**—dog or cat.

So replace only the "final decision layer (fully connected layer)" in the chef's head.

```python
# 2. Freeze existing feature layers
# Keep pretrained weights fixed; do not update them
for param in resnet.parameters():
    param.requires_grad = False # Stop gradient computation for frozen layers

# 3. Replace the final fully connected layer for 2-class classification
# ResNet's last layer is named "fc (Fully Connected)"
# Check how many features feed into the original fc layer
num_features = resnet.fc.in_features

# Swap the 1000-class head for a new 2-class head
# Only the new layer will have requires_grad = True (trainable)
resnet.fc = nn.Linear(num_features, 2)

print("Final layer replaced for 2-class classification!")
print(resnet.fc)
```

That is all the setup! Now run a training loop with this model.

```python
import torch.optim as optim

# 4. Training setup
criterion = nn.CrossEntropyLoss()

# Key point: optimize only the replaced final layer (resnet.fc.parameters())
# Frozen layers do not need updates
optimizer = optim.Adam(resnet.fc.parameters(), lr=0.001)

# Dummy images (batch: 4, RGB 3 channels, 224x224)
# ResNet and similar models expect 224x224 input
dummy_images = torch.randn(4,  3, 224, 224)
dummy_labels = torch.tensor([0, 1, 0, 1])

# 5. Training loop (single-step test)
resnet.train()

optimizer.zero_grad()
predictions = resnet(dummy_images) # Forward pass
loss = criterion(predictions, dummy_labels)
loss.backward()
optimizer.step()

print("\nOne training step complete! Loss:", loss.item())
```

**Explanation:**
With just this much code, you can adapt world-class image recognition AI to your task!
The three key steps:

1. Load a pretrained model.
2. **Freeze** existing layers (`requires_grad = False`).
3. Replace the final layer (`fc` or `classifier`) to match your number of classes.

That lets you build highly accurate AI from hundreds of images in minutes—not tens of thousands of images and days of training.

## 3. Practice

Prepare transfer learning with another famous model: **MobileNet V2**.
MobileNet is lightweight so it runs smoothly on phones and other low-power devices.

**Requirements:**

- Load a pretrained model with `models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)`.
- Freeze all model parameters (`requires_grad = False`).
- You want an AI that distinguishes **10 types of flowers**.
- MobileNet V2's final layer is not `fc` but **`classifier[1]`**.
- Get the original layer's `in_features` and replace it with a new `nn.Linear` with output size `10`.
- (No training loop needed—just the model preparation!)

**Hints:**

```python
mobilenet = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
# MobileNet ends with:
# mobilenet.classifier = nn.Sequential(
#     nn.Dropout(p=0.2),
#     nn.Linear(in_features=1280, out_features=1000) <- this is classifier[1]
# )
```

## 4. Answer Key

<details>
<summary>View sample solution (click to expand)</summary>

```python
import torch
import torch.nn as nn
import torchvision.models as models

# 1. Download pretrained MobileNet V2
mobilenet = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

# 2. Freeze all existing parameters
for param in mobilenet.parameters():
    param.requires_grad = False

# 3. Check input size of the final layer
# In MobileNet V2, classifier[1] is the final Linear layer
num_features = mobilenet.classifier[1].in_features

# 4. Replace the final layer for 10-class classification
mobilenet.classifier[1] = nn.Linear(num_features, 10)

print("Transfer learning setup complete!")
print("New classification layer:", mobilenet.classifier[1])

# --- (Optional) Optimizer setup ---
# Optimize only the replaced layer
import torch.optim as optim
optimizer = optim.Adam(mobilenet.classifier[1].parameters(), lr=0.001)
```

</details>
