# Lab 04: Deep MLP for MNIST Digit Classification
**Student ID:** 23BQ1A4201  
**Date:** March 17, 2026  
**Lab:** Deep Learning Lab - Experiment 04

---

## 1. AIM

To implement and analyze a Deep Feedforward Neural Network (MLP) for handwritten digit classification on the MNIST dataset **without using CNNs**, and to study the impact of depth, regularization, optimizer choice, and hyperparameters on model performance.

---

## 2. LIBRARIES, TOOLS, AND METHODS USED

### Libraries
- **NumPy** (`numpy`) for numerical operations
- **Pandas** (`pandas`) for tabular result summary
- **Matplotlib** (`matplotlib.pyplot`) and **Seaborn** (`seaborn`) for visualizations
- **TensorFlow/Keras** for deep learning:
  - `Sequential`
  - `Dense`, `Dropout`
  - `l2` regularizer
  - `EarlyStopping`
  - `Adam`, `SGD`
- **Scikit-learn**:
  - `train_test_split`
  - `confusion_matrix`, `classification_report`

### Methods/Techniques
1. Flattening image tensors (28×28 → 784)
2. Pixel normalization ($x/255$)
3. One-hot encoding of labels
4. Stratified train-validation split
5. Deep feedforward (MLP) architectures
6. Regularization: Dropout, L2, EarlyStopping
7. Hyperparameter tuning: learning rate, batch size, width
8. Optimizer comparison: Adam vs SGD
9. Evaluation via confusion matrix, classification report, and test accuracy

---

## 3. DATASET DESCRIPTION (MNIST)

- **Total samples:** 70,000
- **Training samples:** 60,000
- **Test samples:** 10,000
- **Image size:** 28 × 28
- **Channels:** 1 (grayscale)
- **Classes:** 10 (digits 0–9)
- **Pixel range:** 0 to 255

### Why this dataset matters
MNIST is a benchmark for image classification and helps evaluate:
- handling high-dimensional inputs (784 features)
- model capacity vs overfitting
- optimization and regularization behavior

---

## 4. PREPROCESSING PIPELINE

1. Loaded dataset using `keras.datasets.mnist.load_data()`
2. Flattened each image: $(28,28) \rightarrow (784,)$
3. Normalized pixel values:

$$x_{norm} = \frac{x}{255}$$

4. One-hot encoded labels to shape `(N, 10)`
5. Train-validation split from training data (80:20) with stratification

---

## 5. MODEL ARCHITECTURES USED

### 5.1 Baseline Model
Architecture: **784 → 512 → 256 → 10**  
Activations: ReLU (hidden), Softmax (output)

### 5.2 Deep Model
Architecture: **784 → 512 → 256 → 128 → 64 → 10**

### 5.3 Overfitting Study Model
Architecture: **784 → 1024 → 512 → 256 → 10** (no dropout)

### 5.4 Regularized Models
- Dropout model (0.3 after each hidden layer)
- L2 model (`l2(0.001)`)
- Full regularization model (Dropout + L2 + EarlyStopping)

---

## 6. HYPERPARAMETERS AND TRAINING SETUP

- Loss: `categorical_crossentropy`
- Primary metric: `accuracy`
- Baseline batch size: 128
- Typical epochs: 20 (30 for overfitting study, up to 50 with EarlyStopping)

### Tuned values
- Learning rates: `[0.0001, 0.001, 0.01]`
- Batch sizes: `[32, 64, 128, 256]`
- Width configs: `[128,64]`, `[256,128]`, `[512,256]`, `[1024,512]`

---

## 7. MATHEMATICAL NOTES

### 7.1 Softmax
For class $i$:

$$\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}$$

### 7.2 Categorical Cross-Entropy

$$L = -\sum_{i=1}^{K} y_i \log(\hat{y}_i)$$

### 7.3 Parameter count example (784×512 layer)

$$784 \times 512 + 512 = 401,920$$

(Weights + biases)

---

## 8. EXPERIMENTAL RESULTS SUMMARY (FROM `exp04.ipynb`)

```
========================================================================
COMPREHENSIVE RESULTS SUMMARY
========================================================================
                   Model  Test Accuracy (%)  Parameters
     Baseline (2 layers)          98.140001      535818
         Deep (4 layers)          98.030001      575050
No Dropout (Overfitting)          98.310000     1462538
            With Dropout          98.229998      567434
                 With L2          97.570002      567434
     Full Regularization          97.539997      567434
          Adam Optimizer          97.930002      535818
           SGD Optimizer          97.979999      535818
========================================================================
Best Model: No Dropout (Overfitting)
Best Accuracy: 98.31%
```

### Exact Notebook Output Block (as recorded)

```
Baseline total parameters (manual): 535,818
Deep model parameters: 575,050
Best model from summary: No Dropout (Overfitting)
Best accuracy achieved: 98.31%
```

### Observations
- All models achieved strong MLP performance (mostly 97.5%–98.3%).
- Highest test accuracy came from the no-dropout high-capacity model.
- Regularized models improved generalization stability but slightly reduced peak test accuracy in this run.
- Adam and SGD both performed similarly in final test accuracy; SGD was marginally higher in this run.

---

## 9. VISUALIZATION SUMMARY

Notebook includes:
1. Sample MNIST digit visualizations
2. Class distribution chart
3. Training/validation accuracy and loss curves (for each major experiment)
4. Baseline confusion matrix
5. Optimizer comparison curves (Adam vs SGD)

All plot titles are prefixed with:  
**`23BQ1A4201 - ...`**

---

## 10. CONFUSION MATRIX & CLASSIFICATION REPORT DISCUSSION

- Baseline confusion matrix is strongly diagonal, indicating high per-class performance.
- Misclassifications mostly occur between visually similar digits (e.g., 4/9, 5/3, 7/1 in general MNIST behavior).
- Classification report confirms high precision/recall/F1 across most classes.

---

## 11. ANALYSIS QUESTIONS (ANSWERED)

1. **Why does MNIST require more neurons than Iris?**  
   MNIST has 784-dimensional image input versus very low-dimensional tabular Iris features, so representational complexity and parameter demand are much higher.

2. **Compute total number of parameters in your baseline model.**  
   Baseline total = **535,818**.

3. **Why is softmax necessary for multi-class classification?**  
   Softmax converts logits to a probability distribution over 10 classes; probabilities sum to 1 and allow argmax-based class prediction.

4. **Why does overfitting occur more severely in MLPs for image data?**  
   MLPs ignore spatial locality and use dense connections, causing many parameters and high memorization risk.

5. **Compare training and validation curves.**  
   Most models converge well; larger non-regularized models can show higher variance or widening train–validation gap, indicating overfitting tendency.

6. **What is the effect of dropout?**  
   Dropout reduces co-adaptation and helps regularization; often improves robustness though peak test accuracy may be slightly lower in some runs.

7. **Why are CNNs preferred for image tasks?**  
   CNNs exploit local spatial features and parameter sharing, making them more efficient and usually more accurate for images.

8. **How many parameters does your deepest model contain?**  
   Deep (4 hidden layer) model parameters = **575,050**.

9. **Which optimizer performed best and why?**  
   In this run, SGD slightly exceeded Adam in final test accuracy (97.98% vs 97.93%), while Adam generally converged faster in early epochs.

10. **What is the best accuracy achieved without CNNs?**  
    **98.31%**.

---

## 12. VIVA VOCE QUICK ANSWERS

1. MNIST is more complex due to high-dimensional image input and intra-class variation.
2. MNIST input dimensionality (flattened) is **784**.
3. Parameters in 784×512 layer = **401,920**.
4. ReLU avoids vanishing gradient in positive region and is computationally simple.
5. Dropout solves overfitting by randomly disabling neurons during training.
6. MLP ignores spatial locality because every pixel is treated independently after flattening.
7. Vanishing gradient: gradients become very small in deep networks, slowing learning in earlier layers.
8. Model size increases due to fully connected layers and large neuron counts.
9. CNN is superior because of local receptive fields and shared kernels.
10. Best non-CNN accuracy in this experiment: **98.31%**.

---

## 13. CONCLUSION

- The Lab objective was achieved successfully using MLP-only architectures on MNIST.
- The notebook demonstrates the effects of architecture depth, regularization, and optimizer choice.
- Best test performance reached **98.31%**, which is strong for non-CNN models.
- Results reinforce the key insight: MLPs can perform well, but CNNs remain more suitable for image tasks due to spatial inductive bias.

---

**Verified by:** 23BQ1A4201  
**Date:** March 17, 2026  
**Signature:** _________________________
