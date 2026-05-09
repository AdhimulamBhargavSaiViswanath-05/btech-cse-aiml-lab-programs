# Lab 07: IMDB Sentiment Analysis using Deep Neural Network (Keras)
**Student ID:** 23BQ1A4201  
**Date:** March 18, 2026  
**Lab:** Deep Learning Lab - Experiment 07

---

## 1. AIM

To build and evaluate a Deep Neural Network for **binary sentiment classification** (Positive/Negative) on the IMDB movie review dataset using Keras, including:
- text vectorization (multi-hot encoding),
- model regularization (Dropout + L2),
- early stopping,
- confusion matrix and classification report,
- hyperparameter comparison.

---

## 2. LIBRARIES AND TOOLS USED

- `numpy`
- `matplotlib.pyplot`
- `seaborn`
- `tensorflow` / `keras`
- `tensorflow.keras.datasets.imdb`
- `tensorflow.keras.layers` (`Dense`, `Dropout`)
- `tensorflow.keras.callbacks.EarlyStopping`
- `sklearn.metrics` (`classification_report`, `confusion_matrix`)

---

## 3. DATASET DETAILS

Dataset: **IMDB movie reviews** (binary sentiment)

### Recorded outputs from notebook
```
Training samples : 25000
Test samples     : 25000
Sample review    : [1, 14, 22, 16, 43, 530, 973, 1622, 1385, 65, 458, 4468, 66, 3941, 4] ...
Label            : 1 → Positive
Review lengths   : min=11, max=2494, mean=239
```

Vocabulary control:
- Top `NUM_WORDS = 10000` frequent words retained.

Class balance:
```
Positive: 12500 | Negative: 12500
```
(Perfectly balanced classes.)

---

## 4. TEXT PREPROCESSING AND VECTORIZATION

### 4.1 Decoding reviews
Used `imdb.get_word_index()` and reverse mapping (`+3` index shift) to decode integer tokens back to words.

### 4.2 Multi-hot vectorization
Each review converted into a binary vector of size 10,000:

$$x_i \in \mathbb{R}^{10000}, \quad x_i[j] = 1 \text{ if word } j \text{ appears in review } i$$

Recorded outputs:
```
x_train_vec shape: (25000, 10000)
x_test_vec  shape: (25000, 10000)
Non-zeros in review 0: 120.0 (unique words present)
```

### 4.3 Train/Validation split
Validation set taken from first 10,000 training examples.

Recorded outputs:
```
Training samples  : 15000
Validation samples: 10000
Test samples      : 25000
```

---

## 5. MODEL ARCHITECTURE

Model type: `keras.Sequential`

Architecture:
1. Dense(16, ReLU, L2 regularization)
2. Dropout(0.5)
3. Dense(16, ReLU, L2 regularization)
4. Dropout(0.5)
5. Dense(1, Sigmoid)

Compilation:
- Optimizer: Adam (`lr=0.001`)
- Loss: `binary_crossentropy`
- Metric: `accuracy`

### Model summary highlights (recorded)
- Hidden layer 1 params: **160,016**
- Hidden layer 2 params: **272**
- **Total params: 160,305 (626.19 KB)**
- Trainable params: **160,305**
- Non-trainable params: **0**

---

## 6. TRAINING DETAILS

Training settings:
- Epochs: up to 20
- Batch size: 512
- Validation: `(x_val, y_val)`
- Callback: `EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)`

Recorded key logs:
- Early epoch trend showed rapid gain from ~0.62 to >0.90 training accuracy.
- Validation accuracy peaked around high 88% range.

Recorded stop condition:
```
Training stopped at epoch: 9
```

---

## 7. TEST EVALUATION RESULTS

Recorded outputs:
```
Test Loss     : 0.3407
Test Accuracy : 0.8832  (88.32%)
```

### Classification report (recorded)
```
Negative       0.88      0.89      0.88     12500
Positive       0.89      0.88      0.88     12500

accuracy                           0.88     25000
macro avg       0.88      0.88      0.88     25000
weighted avg    0.88      0.88      0.88     25000
```

Interpretation:
- Balanced precision/recall across both classes.
- Strong and consistent binary sentiment performance.

---

## 8. CONFUSION MATRIX ANALYSIS

From saved confusion matrix image (`23BQ1A4201 - exp7_confusion_matrix.png`):

| True \ Pred | Negative | Positive |
|---|---:|---:|
| Negative | 11104 | 1396 |
| Positive | 1523 | 10977 |

This confirms:
- True Negative (TN) = 11104
- False Positive (FP) = 1396
- False Negative (FN) = 1523
- True Positive (TP) = 10977

Overall behavior:
- Slightly better recall for Negative class than Positive class.
- Errors are reasonably balanced; no severe class bias.

---

## 9. SAVED FIGURES (ARTIFACTS)

The experiment generated and saved:
1. `23BQ1A4201 - exp7_training_curves.png`
   - Training vs validation loss and accuracy curves.
2. `23BQ1A4201 - exp7_confusion_matrix.png`
   - Confusion matrix heatmap for test set.

---

## 10. CUSTOM REVIEW PREDICTION (REAL-WORLD CHECK)

The notebook includes custom review inference pipeline:
- tokenization by `.lower().split()`
- index conversion using IMDB dictionary with offset
- vectorization to 10,000-dim multi-hot vector
- sentiment prediction via sigmoid probability

Three sample custom reviews were evaluated and printed with probability score and sentiment label.

---

## 11. HYPERPARAMETER COMPARISON EXPERIMENT

Notebook compared 4 configs and reported test accuracy:

```
Baseline                       → Test Acc: 88.52%
Wider (32 units)               → Test Acc: 88.46%
No Regularization              → Test Acc: 87.67%
Large + Low LR                 → Test Acc: 86.76%
```

### Observation
- Best among tested variants: **Baseline (88.52%)**.
- Regularization clearly helps; removing it dropped performance.
- Increasing width or lowering learning rate did not improve over baseline in this setup.

---

## 12. CONCLUSION

The IMDB sentiment classification experiment was successfully implemented end-to-end with preprocessing, model training, evaluation, and hyperparameter study.

Key outcomes:
- Baseline test accuracy around **88.3%** on 25,000 test reviews.
- Balanced class-wise performance (precision/recall/F1 near 0.88).
- Early stopping prevented unnecessary overtraining.
- Regularized baseline outperformed more complex alternatives.
- Training and confusion matrix figures were generated and stored correctly.

---

**Notebook Reference:** `lab07/exp07.ipynb`  
**Saved Figures:**
- `lab07/23BQ1A4201 - exp7_training_curves.png`
- `lab07/23BQ1A4201 - exp7_confusion_matrix.png`

**Verified by:** 23BQ1A4201  
**Date:** March 18, 2026  
**Signature:** _________________________
