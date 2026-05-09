# Lab 05: CNN for Cats vs Dogs Classification using Keras
**Student ID:** 23BQ1A4201  
**Date:** March 18, 2026  
**Lab:** Deep Learning Lab - Experiment 05

---

## 1. AIM

To implement a **Convolutional Neural Network (CNN)** for binary image classification (Dog/Cat) using Keras, and compare performance between:
1. A **Sequential API** model
2. A **Functional API** model

---

## 2. LIBRARIES AND TOOLS USED

- `tensorflow` / `keras`
- `Sequential`, `Model`, `Input`
- `Conv2D`, `MaxPooling2D`, `Flatten`, `Dense`
- `ImageDataGenerator`
- `numpy`, `matplotlib`, `os`, `zipfile`, `shutil`

---

## 3. DATASET DETAILS

Dataset folder used:
- `D:/DL Lab 2026/lab05/cats_and_dogs_filtered/train`
- `D:/DL Lab 2026/lab05/cats_and_dogs_filtered/validation`

### Generator output (as recorded)
```
Found 2000 images belonging to 2 classes.
Found 1000 images belonging to 2 classes.
```

### Data preprocessing
- Rescaling: $x \rightarrow x/255$
- Training augmentation:
  - `shear_range=0.1`
  - `zoom_range=0.1`
  - `horizontal_flip=False`
- Validation/test: only rescaling

### Image settings
- `target_size=(150, 150)`
- `batch_size=32`
- `class_mode='binary'`

---

## 4. MODEL ARCHITECTURES

Both models use the same CNN backbone and classifier:

- Conv2D(16, 3×3, ReLU) → MaxPool
- Conv2D(32, 3×3, ReLU) → MaxPool
- Conv2D(64, 3×3, ReLU) → MaxPool
- Conv2D(64, 3×3, ReLU) → MaxPool
- Flatten
- Dense(256, ReLU)
- Dense(1, Sigmoid)

Loss/Optimizer/Metrics:
- Loss: `binary_crossentropy`
- Optimizer: `adam`
- Metric: `accuracy`

---

## 5. MODEL SUMMARY (SEQUENTIAL API)

```
Model: "sequential_1"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Layer (type)                    ┃ Output Shape           ┃       Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ conv2d_8 (Conv2D)               │ (None, 148, 148, 16)   │           448 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_8 (MaxPooling2D)  │ (None, 74, 74, 16)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_9 (Conv2D)               │ (None, 72, 72, 32)     │         4,640 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_9 (MaxPooling2D)  │ (None, 36, 36, 32)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_10 (Conv2D)              │ (None, 34, 34, 64)     │        18,496 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_10 (MaxPooling2D) │ (None, 17, 17, 64)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_11 (Conv2D)              │ (None, 15, 15, 64)     │        36,928 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_11 (MaxPooling2D) │ (None, 7, 7, 64)       │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten_2 (Flatten)             │ (None, 3136)           │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_4 (Dense)                 │ (None, 256)            │       803,072 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_5 (Dense)                 │ (None, 1)              │           257 │
==
 Total params: 863,841 (3.30 MB)
 Trainable params: 863,841 (3.30 MB)
 Non-trainable params: 0 (0.00 B)
```

---

## 6. MODEL SUMMARY (FUNCTIONAL API)

```
Model: "functional_3"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Layer (type)                    ┃ Output Shape           ┃       Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ input_layer_3 (InputLayer)      │ (None, 150, 150, 3)    │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_12 (Conv2D)              │ (None, 148, 148, 16)   │           448 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_12 (MaxPooling2D) │ (None, 74, 74, 16)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_13 (Conv2D)              │ (None, 72, 72, 32)     │         4,640 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_13 (MaxPooling2D) │ (None, 36, 36, 32)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_14 (Conv2D)              │ (None, 34, 34, 64)     │        18,496 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_14 (MaxPooling2D) │ (None, 17, 17, 64)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_15 (Conv2D)              │ (None, 15, 15, 64)     │        36,928 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_15 (MaxPooling2D) │ (None, 7, 7, 64)       │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten_3 (Flatten)             │ (None, 3136)           │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_6 (Dense)                 │ (None, 256)            │       803,072 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_7 (Dense)                 │ (None, 1)              │           257 │
Total params: 863,841 (3.30 MB)
 Trainable params: 863,841 (3.30 MB)
 Non-trainable params: 0 (0.00 B)
```

---

## 7. TRAINING LOG HIGHLIGHTS (AS PROVIDED)

### 7.1 Sequential model (`model_seq`)
```
Epoch 1/15
62/62 ━━━━━━━━━━━━━━━━━━━━ 53s 773ms/step - accuracy: 0.5066 - loss: 0.6939 - val_accuracy: 0.5252 - val_loss: 0.6709
Epoch 2/15
62/62 ━━━━━━━━━━━━━━━━━━━━ 6s 95ms/step - accuracy: 0.5625 - loss: 0.6903 - val_accuracy: 0.5554 - val_loss: 0.6699
Epoch 15/15
62/62 ━━━━━━━━━━━━━━━━━━━━ 45s 722ms/step - accuracy: 0.7424 - loss: 0.5018 - val_accuracy: 0.7107 - val_loss: 0.5735
==
32/32 - 6s - 193ms/step - accuracy: 0.7110 - loss: 0.5741

Test accuracy: 0.7110000252723694
```

### 7.2 Functional model (`model_Functional`)
```
Epoch 1/15
62/62 ━━━━━━━━━━━━━━━━━━━━ 50s 726ms/step - accuracy: 0.5203 - loss: 0.6960 - val_accuracy: 0.5010 - val_loss: 0.6895
Epoch 2/15
62/62 ━━━━━━━━━━━━━━━━━━━━ 7s 105ms/step - accuracy: 0.4062 - loss: 0.7102 - val_accuracy: 0.5010 - val_loss: 0.6879
Epoch 15/15
62/62 ━━━━━━━━━━━━━━━━━━━━ 26s 415ms/step - accuracy: 0.7830 - loss: 0.4635 - val_accuracy: 0.7379 - val_loss: 0.5622
==
32/32 - 4s - 124ms/step - accuracy: 0.7370 - loss: 0.5670

Test accuracy: 0.7369999885559082
```

---

## 8. PERFORMANCE COMPARISON

| Model | Parameters | Final Test Loss | Final Test Accuracy |
|---|---:|---:|---:|
| Sequential CNN | 863,841 | 0.5741 | 0.7110 (71.10%) |
| Functional CNN | 863,841 | 0.5670 | 0.7370 (73.70%) |

### Best model
- **Functional API model** performed better on test set.
- Accuracy improvement over Sequential:

$$73.70\% - 71.10\% = 2.60\%$$

---

## 9. ANALYSIS

1. Both models have identical architecture and parameter count.
2. Performance difference is due to training dynamics (random initialization, optimizer path, mini-batch ordering), not architecture size.
3. Validation accuracy improved significantly by epoch 15 in both models, indicating effective learning.
4. The experiment demonstrates that the Functional API can replicate Sequential architecture while offering greater flexibility for advanced architectures.

---

## 10. CODE STRUCTURE IN NOTEBOOK (`exp05.ipynb`)

1. Import libraries
2. Build train/test image generators
3. Define and compile Sequential CNN
4. Define and compile Functional CNN
5. Train Sequential CNN
6. Evaluate Sequential CNN
7. Train Functional CNN
8. Evaluate Functional CNN

---

## 11. CONCLUSION

The experiment successfully implemented CNN-based binary image classification for cats vs dogs using Keras. Both Sequential and Functional implementations reached reasonable performance, with the Functional model achieving the best test accuracy of **73.70%**. This confirms the correctness of preprocessing, architecture design, and training pipeline, while also showing practical comparison of Keras model APIs.

---

**Notebook Reference:** `lab05/exp05.ipynb`  
**Dataset Folder:** `lab05/cats_and_dogs_filtered/`  

**Verified by:** 23BQ1A4201  
**Date:** March 18, 2026  
**Signature:** _________________________
