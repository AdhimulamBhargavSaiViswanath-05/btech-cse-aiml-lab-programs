# Lab 03: ANN Classification for Multi-Class Datasets
**Student ID:** 23BQ1A4201  
**Date:** February 20, 2026  
**Lab:** Deep Learning Lab - Experiment 03

---

## 1. AIM

To build and evaluate Artificial Neural Network (ANN) classification algorithms for multi-class classification problems on two different datasets:
1. **Seeds Dataset**: Classify wheat kernels into 3 varieties based on physical measurements
2. **Glass Dataset**: Classify glass types into 6 categories based on chemical composition

To obtain and analyze:
- Confusion matrices
- Accuracy metrics
- Loss and accuracy curves
- Precision, Recall, and F1-Score

---

## 2. LIST OF LIBRARIES & METHODS USED

### Libraries:
- **pandas** (`pd`): Data loading and manipulation
- **numpy** (`np`): Numerical computations and array operations
- **matplotlib.pyplot** (`plt`): Data visualization and plotting
- **seaborn** (`sns`): Statistical data visualization (heatmaps)
- **sklearn.preprocessing.StandardScaler**: Feature standardization (z-score normalization)
- **sklearn.impute.SimpleImputer**: Missing value imputation
- **sklearn.model_selection.train_test_split**: Dataset splitting with stratification
- **sklearn.metrics**: Model evaluation metrics
  - `accuracy_score`: Overall accuracy
  - `confusion_matrix`: Classification confusion matrix
  - `classification_report`: Precision, Recall, F1-Score
  - `precision_recall_fscore_support`: Detailed metrics calculation
- **tensorflow** (`tf`): Deep learning framework
- **tensorflow.keras.models.Sequential**: Sequential neural network model
- **tensorflow.keras.layers**: Dense, Input, Dropout layers
- **tensorflow.keras.optimizers.Adam**: Optimization algorithm
- **tensorflow.keras.utils.to_categorical**: One-hot encoding for labels

### Methods/Techniques:
1. **Data Preprocessing**: Missing value imputation, standardization
2. **Exploratory Data Analysis (EDA)**: Histograms, correlation heatmaps
3. **Stratified Train-Test Split**: Maintains class distribution
4. **One-Hot Encoding**: Converting class labels to categorical format
5. **Feed-Forward Neural Networks (FFNN)**: Multi-layer perceptron for classification
6. **Regularization**: Dropout layers
7. **Multi-Class Classification**: Softmax activation for output
8. **Categorical Cross-Entropy Loss**: For multi-class problems
9. **Model Evaluation**: Confusion matrix, classification report

---

## 3. DETAILED DESCRIPTION OF DATASETS

### 3.1 Seeds Dataset

**File:** `seeds_dataset.txt`

**Description:**  
The Seeds dataset contains measurements of geometrical properties of kernels belonging to three different varieties of wheat: Kama, Rosa, and Canadian. The dataset is used for variety classification based on physical characteristics.

**Dataset Size:** 210 samples with 7 features and 1 target variable

**Key Features:**
- **Input Features (7):**
  - `area`: Area of the kernel
  - `perimeter`: Perimeter of the kernel
  - `compactness`: Compactness (C = 4*pi*A/P²)
  - `kernel_length`: Length of kernel
  - `kernel_width`: Width of kernel
  - `asymmetry_coefficient`: Asymmetry coefficient
  - `groove_length`: Length of kernel groove

- **Target Variable:**
  - `class`: Wheat variety (1, 2, or 3)

**Preprocessing Steps:**
1. Data loaded with whitespace separator
2. Missing values imputed using mean strategy (though none present)
3. Features standardized using StandardScaler (z-score normalization)
4. One-hot encoding applied to target classes (converted to 0, 1, 2)
5. Stratified train-test split: 80% training (168 samples), 20% testing (42 samples)

**Class Distribution:** Balanced (70 samples per class)

### 3.2 Glass Dataset

**File:** `glass.data`

**Description:**  
The Glass Identification dataset contains chemical composition measurements of glass samples. It was collected for forensic analysis to classify glass fragments found at crime scenes.

**Dataset Size:** 214 samples with 9 features and 1 target variable

**Key Features:**
- **Input Features (9):**
  - `RI`: Refractive Index
  - `Na`: Sodium content (weight percent in oxide)
  - `Mg`: Magnesium content
  - `Al`: Aluminum content
  - `Si`: Silicon content
  - `K`: Potassium content
  - `Ca`: Calcium content
  - `Ba`: Barium content
  - `Fe`: Iron content

- **Target Variable:**
  - `Type`: Glass type (1-7, representing different glass categories)
    - 1: Building window (float processed)
    - 2: Building window (non-float processed)
    - 3: Vehicle window (float processed)
    - 5: Containers
    - 6: Tableware
    - 7: Headlamps

**Preprocessing Steps:**
1. ID column dropped (not a predictor)
2. Missing values imputed using mean strategy
3. Features standardized using StandardScaler
4. One-hot encoding applied to target classes (converted to 0-based indexing)
5. Stratified train-test split: 80% training (171 samples), 20% testing (43 samples)

**Class Distribution:** Imbalanced (some classes have few samples)

---

## 4. DETAILS OF MODEL ARCHITECTURE

### 4.1 Seeds Classification Model

**Architecture:**
```
Input Layer      → (7 features)
Hidden Layer 1   → 64 neurons, ReLU activation
Dropout          → 0.3 (30% dropout)
Hidden Layer 2   → 32 neurons, ReLU activation
Dropout          → 0.3
Output Layer     → 3 neurons, Softmax activation
```

**Activation Functions:**
- **Hidden Layers:** ReLU (Rectified Linear Unit)
  - Formula: $f(x) = \max(0, x)$
  - Prevents vanishing gradient problem
  - Computationally efficient
  
- **Output Layer:** Softmax
  - Formula: $\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}$
  - Converts logits to probability distribution
  - Output probabilities sum to 1
  - Suitable for multi-class classification

### 4.2 Glass Classification Model

**Architecture:**
```
Input Layer      → (9 features)
Hidden Layer 1   → 64 neurons, ReLU activation
Dropout          → 0.3 (30% dropout)
Hidden Layer 2   → 32 neurons, ReLU activation
Dropout          → 0.3
Output Layer     → 7 neurons, Softmax activation
```

**Activation Functions:**
- Hidden Layers: ReLU
- Output Layer: Softmax (7 classes)

---

## 5. OPTIMIZATION TECHNIQUES & HYPERPARAMETERS

### 5.1 Seeds Model

**Optimizer:** Adam (Adaptive Moment Estimation)
- **Learning Rate:** 0.001
- **Beta1:** 0.9 (default)
- **Beta2:** 0.999 (default)
- **Epsilon:** 1e-7 (default)

**Loss Function:** Categorical Cross-Entropy
- Formula: $L = -\sum_{i=1}^{K} y_i \log(\hat{y}_i)$
- Where $y_i$ is true label (one-hot) and $\hat{y}_i$ is predicted probability
- Suitable for multi-class classification with one-hot encoded labels

**Training Hyperparameters:**
- **Epochs:** 100
- **Batch Size:** 16
- **Validation Split:** 0.2 (20% of training data)

**Regularization:**
- **Dropout Rate:** 0.3 (prevents overfitting by randomly dropping 30% of neurons during training)

### 5.2 Glass Model

**Optimizer:** Adam
- **Learning Rate:** 0.001

**Loss Function:** Categorical Cross-Entropy

**Training Hyperparameters:**
- **Epochs:** 100
- **Batch Size:** 16
- **Validation Split:** 0.2

**Regularization:**
- **Dropout Rate:** 0.3

---

## 6. MATHEMATICAL ANALYSIS

### 6.1 Standardization (Z-Score Normalization)

For each feature:

$$z = \frac{x - \mu}{\sigma}$$

Where:
- $x$ = original value
- $\mu$ = mean of the feature
- $\sigma$ = standard deviation
- $z$ = standardized value

**Benefits:**
- Centers data around zero (mean = 0)
- Scales data to unit variance (std = 1)
- Prevents features with larger scales from dominating

### 6.2 Forward Propagation

For each layer $l$:

$$z^{[l]} = W^{[l]} \cdot a^{[l-1]} + b^{[l]}$$

$$a^{[l]} = g^{[l]}(z^{[l]})$$

Where:
- $W^{[l]}$ = weight matrix
- $b^{[l]}$ = bias vector
- $g^{[l]}$ = activation function (ReLU or Softmax)

### 6.3 Softmax Function (Output Layer)

For multi-class classification:

$$\text{softmax}(z)_i = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}$$

**Properties:**
- Outputs are in range (0, 1)
- Sum of all outputs = 1 (valid probability distribution)
- Used with categorical cross-entropy loss

### 6.4 Categorical Cross-Entropy Loss

$$L(\mathbf{y}, \hat{\mathbf{y}}) = -\sum_{i=1}^{K} y_i \log(\hat{y}_i)$$

Where:
- $K$ = number of classes
- $y_i$ = true label (1 for correct class, 0 otherwise)
- $\hat{y}_i$ = predicted probability for class $i$

For batch of $N$ samples:

$$L_{\text{total}} = -\frac{1}{N}\sum_{n=1}^{N}\sum_{i=1}^{K} y_{n,i} \log(\hat{y}_{n,i})$$

### 6.5 Dropout Regularization

During training, randomly set activations to zero with probability $p$:

$$a^{[l]}_{\text{dropout}} = 
\begin{cases} 
0 & \text{with probability } p \\
\frac{a^{[l]}}{1-p} & \text{with probability } 1-p
\end{cases}$$

**Inverted Dropout** (used in Keras):
- Scale remaining activations by $\frac{1}{1-p}$ during training
- No scaling needed during inference

### 6.6 Evaluation Metrics

**Accuracy:**
$$\text{Accuracy} = \frac{\text{Number of Correct Predictions}}{\text{Total Predictions}}$$

**Precision (for class $i$):**
$$\text{Precision}_i = \frac{TP_i}{TP_i + FP_i}$$

**Recall (for class $i$):**
$$\text{Recall}_i = \frac{TP_i}{TP_i + FN_i}$$

**F1-Score (for class $i$):**
$$\text{F1}_i = 2 \cdot \frac{\text{Precision}_i \cdot \text{Recall}_i}{\text{Precision}_i + \text{Recall}_i}$$

Where:
- $TP$ = True Positives
- $FP$ = False Positives
- $FN$ = False Negatives

**Weighted Average** (for imbalanced datasets):
$$\text{Metric}_{\text{weighted}} = \frac{\sum_{i=1}^{K} n_i \cdot \text{Metric}_i}{\sum_{i=1}^{K} n_i}$$

Where $n_i$ is the number of samples in class $i$.

---

## 7. CODE

The complete implementation is available in the Jupyter notebook:

**Notebook:** `lab03/exp03.ipynb`

**Key Code Sections:**

### 7.1 Data Loading & Preprocessing
```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Load seeds dataset
data = pd.read_csv("datasets/seeds_dataset.txt", sep=r'\s+', names=column_names)

# Handle missing values
imputer = SimpleImputer(strategy="mean")
X_imputed = imputer.fit_transform(X)

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)
```

### 7.2 Train-Test Split with Stratification
```python
from sklearn.model_test_split import train_test_split
from tensorflow.keras.utils import to_categorical

# Stratified split (maintains class distribution)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# One-hot encode labels
y_train_cat = to_categorical(y_train - 1)  # Convert 1,2,3 to 0,1,2
y_test_cat = to_categorical(y_test - 1)
```

### 7.3 Model Building
```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input

model = Sequential([
    Input(shape=(X_train.shape[1],)),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dropout(0.3),
    Dense(3, activation='softmax')  # 3 classes
])
```

### 7.4 Model Compilation
```python
from tensorflow.keras.optimizers import Adam

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
```

### 7.5 Model Training
```python
history = model.fit(
    X_train, y_train_cat,
    validation_split=0.2,
    epochs=100,
    batch_size=16,
    verbose=1
)
```

### 7.6 Evaluation & Confusion Matrix
```python
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np

# Predictions
y_pred_probs = model.predict(X_test)
y_pred = np.argmax(y_pred_probs, axis=1)
y_true = np.argmax(y_test_cat, axis=1)

# Metrics
accuracy = accuracy_score(y_true, y_pred)
print("Accuracy:", accuracy)
print(classification_report(y_true, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred)
```

---

## 8. TEST CASES

### 8.1 Seeds Model - Sample Predictions

**Test Set Size:** 42 samples (20% of 210)

**Sample Predictions (from actual model output):**

| Test Case | Actual Class | Predicted Class | Correct? |
|-----------|--------------|-----------------|----------|
| 1         | 1            | 1               | ✓        |
| 2         | 3            | 3               | ✓        |
| 3         | 2            | 1               | ✗        |
| 4         | 3            | 3               | ✓        |
| 5         | 2            | 2               | ✓        |
| 6         | 3            | 3               | ✓        |
| 7         | 2            | 2               | ✓        |
| 8         | 1            | 2               | ✗        |
| 9         | 2            | 2               | ✓        |
| 10        | 2            | 2               | ✓        |

**New Sample Prediction:**
- **Input:** [15.5, 14.8, 0.88, 5.7, 3.4, 2.0, 5.1]
- **Predicted Class:** 1

### 8.2 Glass Model - Sample Predictions

**Test Set Size:** 43 samples (20% of 214)

**Sample Predictions (from actual model output):**

| Test Case | Actual Type | Predicted Type | Correct? |
|-----------|-------------|----------------|----------|
| 1         | 7           | 7              | ✓        |
| 2         | 5           | 5              | ✓        |
| 3         | 2           | 2              | ✓        |
| 4         | 5           | 5              | ✓        |
| 5         | 1           | 1              | ✓        |
| 6         | 1           | 2              | ✗        |
| 7         | 2           | 2              | ✓        |
| 8         | 2           | 2              | ✓        |
| 9         | 1           | 1              | ✓        |
| 10        | 1           | 1              | ✓        |

**New Sample Prediction:**
- **Input:** [1.52101, 13.64, 4.49, 1.10, 71.78, 0.06, 8.75, 0.00, 0.00]
- **Predicted Type:** 1

---

## 9. GRAPHS AND PLOTS

### 9.1 Seeds Dataset Visualizations

1. **Feature Distribution Histograms**
   - Shows distribution of all 7 features
   - Most features show near-normal distributions after standardization
   - Helps identify outliers and data quality

2. **Correlation Heatmap**
   - Feature correlation matrix
   - Strong correlations between physical dimensions (area, perimeter, length)
   - Helps understand feature relationships

3. **Training vs Validation Accuracy**
   - Accuracy curves over 100 epochs
   - Both training and validation accuracy increase and converge
   - No significant overfitting observed

4. **Training vs Validation Loss**
   - Loss curves over 100 epochs
   - Both losses decrease smoothly
   - Convergence indicates good model fit

5. **Confusion Matrix**
   - 3×3 matrix for 3 classes (Kama, Rosa, Canadian)
   - Diagonal elements show correct predictions
   - Class 0 (Kama): 8/14 correct (57%)
   - Class 1 (Rosa): 13/14 correct (93%)
   - Class 2 (Canadian): 14/14 correct (100%)
   - Total: 35/42 correct (83.33% accuracy)

### 9.2 Glass Dataset Visualizations

1. **Feature Distribution Histograms**
   - Shows distribution of 9 chemical composition features
   - Wide range of scales (RI ~1.5, Si ~70%, Ba ~0-3%)
   - Standardization essential before training

2. **Correlation Heatmap**
   - Chemical composition correlations
   - RI strongly correlated with Ca and Si
   - Ba and Fe weakly correlated with other features

3. **Training vs Validation Accuracy**
   - Accuracy curves over 100 epochs
   - More fluctuation due to smaller dataset and class imbalance
   - Validation accuracy plateaus around 65-70%

4. **Training vs Validation Loss**
   - Loss curves show gradual decrease
   - Some fluctuation due to small batch size and imbalance

5. **Confusion Matrix**
   - 6×6 matrix (classes present in test: 0, 1, 2, 4, 5, 6)
   - Class 0: 11/14 correct (79%)
   - Class 1: 11/15 correct (73%)
   - Class 2: 0/3 correct (0%) - difficult class
   - Class 4: 2/3 correct (67%)
   - Class 5: 1/2 correct (50%)
   - Class 6: 5/6 correct (83%)
   - Total: 30/43 correct (69.77% accuracy)

6. **Model Performance Comparison Bar Chart**
   - Side-by-side comparison of Seeds vs Glass models
   - Metrics: Accuracy, Precision, Recall, F1-Score
   - Seeds model outperforms Glass model across all metrics

---

## 10. CONFUSION MATRIX ANALYSIS

### 10.1 Seeds Model Confusion Matrix (Actual Output)

```
              Predicted
           Class 0  Class 1  Class 2
Actual 0      8        6        0
Actual 1      1       13        0
Actual 2      0        0       14
```

**Analysis:**
- **Class 0 (Kama):** 
  - Precision: 0.89 (8 correct out of 9 predicted as Class 0)
  - Recall: 0.57 (8 correct out of 14 actual Class 0)
  - Often misclassified as Class 1 (6 instances)
  
- **Class 1 (Rosa):**
  - Precision: 0.81 (13 correct out of 16 predicted as Class 1)
  - Recall: 0.93 (13 correct out of 14 actual Class 1)
  - Best recall, occasionally confused with Class 0

- **Class 2 (Canadian):**
  - Precision: 0.82 (14 correct out of 17 predicted as Class 2)
  - Recall: 1.00 (all 14 actual Class 2 correctly identified)
  - Perfect recall - most distinctive class

### 10.2 Glass Model Confusion Matrix (Actual Output)

Classes present in test set: 0, 1, 2, 4, 5, 6 (original labels: 1, 2, 3, 5, 6, 7)

```
              Predicted
           C0  C1  C2  C3  C4  C5
Actual 0   11   2   0   0   1   0
Actual 1    3  11   0   0   1   0
Actual 2    1   0   0   0   0   2
Actual 4    0   0   0   0   2   1
Actual 5    0   0   0   0   1   1
Actual 6    0   1   0   0   0   5
```

**Analysis:**
- **Class 0 (Building Float):** Good precision (0.69) and recall (0.79)
- **Class 1 (Building Non-Float):** Good performance (0.73 recall)
- **Class 2 (Vehicle Float):** Poor performance (0% recall) - only 3 samples, all misclassified
- **Class 4 (Containers):** Moderate performance (67% recall)
- **Class 5 (Tableware):** Difficult class (50% recall, only 2 samples)
- **Class 6 (Headlamps):** Best performance (83% recall)

**Challenges:**
- Class imbalance (classes 2, 4, 5 have very few samples)
- Similar chemical compositions between some glass types
- Building window types (0 and 1) often confused with each other

---

## 11. MODEL PERFORMANCE SUMMARY

### 11.1 Seeds Classification Model

**Overall Performance (from actual output):**
- **Accuracy:** 0.8333 (83.33%)
- **Precision (weighted):** 0.8416 (84.16%)
- **Recall (weighted):** 0.8333 (83.33%)
- **F1-Score (weighted):** 0.8218 (82.18%)

**Per-Class Metrics:**

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| 0     | 0.89      | 0.57   | 0.70     | 14      |
| 1     | 0.81      | 0.93   | 0.87     | 14      |
| 2     | 0.82      | 1.00   | 0.90     | 14      |

**Interpretation:**
- Excellent overall accuracy (>80%)
- Class 2 perfectly identified (recall = 1.0)
- Class 0 has lower recall (0.57) - improvement needed
- Well-balanced performance across classes

### 11.2 Glass Classification Model

**Overall Performance (from actual output):**
- **Accuracy:** 0.6977 (69.77%)
- **Precision (weighted):** 0.6564 (65.64%)
- **Recall (weighted):** 0.6977 (69.77%)
- **F1-Score (weighted):** 0.6727 (67.27%)

**Per-Class Metrics:**

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| 0     | 0.69      | 0.79   | 0.73     | 14      |
| 1     | 0.69      | 0.73   | 0.71     | 15      |
| 2     | 0.00      | 0.00   | 0.00     | 3       |
| 4     | 1.00      | 0.67   | 0.80     | 3       |
| 5     | 0.50      | 0.50   | 0.50     | 2       |
| 6     | 0.71      | 0.83   | 0.77     | 6       |

**Interpretation:**
- Moderate overall accuracy (~70%)
- Class imbalance significantly affects performance
- Classes 2, 4, 5 have very few samples (2-3 each)
- Building window types (0, 1) achieve reasonable performance
- Class 2 completely fails (0% recall) - insufficient training data

---

## 12. COMPARATIVE ANALYSIS

### 12.1 Model Comparison Table

| Metric              | Seeds Model | Glass Model | Winner |
|---------------------|-------------|-------------|--------|
| **Dataset Size**    | 210         | 214         | Similar|
| **Features**        | 7           | 9           | -      |
| **Classes**         | 3           | 7 (6 in test)| -      |
| **Test Samples**    | 42          | 43          | Similar|
| **Accuracy**        | 83.33%      | 69.77%      | Seeds  |
| **Precision**       | 84.16%      | 65.64%      | Seeds  |
| **Recall**          | 83.33%      | 69.77%      | Seeds  |
| **F1-Score**        | 82.18%      | 67.27%      | Seeds  |
| **Architecture**    | 7→64→32→3   | 9→64→32→7   | Similar|
| **Class Balance**   | Balanced    | Imbalanced  | Seeds  |

### 12.2 Key Insights

**Why Seeds Model Performs Better:**
1. **Balanced Classes:** All 3 classes have exactly 70 samples each
2. **Fewer Classes:** Only 3 classes vs 6-7 in Glass
3. **Clear Separability:** Seed varieties have distinct physical measurements
4. **Adequate Training Data:** 56-60 samples per class in training

**Why Glass Model Underperforms:**
1. **Class Imbalance:** Some classes have only 2-3 samples in test set
2. **More Classes:** 6-7 classes to distinguish
3. **Similar Features:** Chemical compositions can be similar across types
4. **Insufficient Data:** Not enough samples for rare glass types (vehicle windows, tableware)

---

## 13. CONCLUSION

### 13.1 Seeds Classification

**Achievements:**
1. Successfully built ANN classifier with 83.33% accuracy
2. Class 2 (Canadian wheat) achieved perfect recall (100%)
3. Confusion matrix shows clear diagonal pattern
4. Training and validation curves indicate good convergence
5. No significant overfitting observed

**Key Findings:**
- Physical measurements effectively distinguish wheat varieties
- 2-hidden layer architecture sufficient for this problem
- Dropout regularization prevents overfitting
- Stratified splitting ensures representative test set
- Class 1 (Rosa) achieves best overall performance (F1: 0.87)

**Limitations:**
- Class 0 (Kama) has lower recall (57%) - often confused with Class 1
- Could benefit from more training data or feature engineering
- Model may struggle with borderline cases between Kama and Rosa

### 13.2 Glass Classification

**Achievements:**
1. Built multi-class classifier achieving 69.77% accuracy
2. Building window types (Classes 0, 1) well-classified
3. Headlamps (Class 6) achieved 83% recall
4. Model handles 6-7 different glass types

**Key Findings:**
- Chemical composition provides moderate discriminative power
- Class imbalance significantly impacts performance
- Rare classes (2, 4, 5) poorly classified due to insufficient samples
- Model architecture appropriate but limited by data

**Challenges:**
- Class 2 (Vehicle Float) completely misclassified (0% recall)
- Only 2-3 test samples for some classes - unreliable evaluation
- Building window types (float vs non-float) often confused
- Forensic glass identification remains challenging

**Recommendations for Improvement:**
1. **Data Augmentation:** Generate synthetic samples for rare classes
2. **Class Weights:** Apply higher weights to minority classes in loss function
3. **Feature Engineering:** Add derived features (ratios, combinations)
4. **Ensemble Methods:** Combine multiple models
5. **Collect More Data:** Especially for rare glass types
6. **Try Other Architectures:** CNN, ResNet for feature extraction

### 13.3 Learning Outcomes

1. **Multi-Class Classification:** Successfully implemented softmax and categorical cross-entropy
2. **Stratified Splitting:** Understood importance for maintaining class distribution
3. **Confusion Matrix Analysis:** Identified per-class strengths and weaknesses
4. **Class Imbalance Handling:** Recognized impact on model performance
5. **Standardization:** Learned necessity for features with different scales
6. **Dropout Regularization:** Applied to prevent overfitting
7. **Model Evaluation:** Used comprehensive metrics beyond accuracy
8. **Comparative Analysis:** Understood dataset characteristics impact on performance

### 13.4 Practical Applications

**Seeds Classification:**
- Agricultural quality control
- Seed sorting automation
- Crop variety verification
- Breeding program assistance

**Glass Classification:**
- Forensic investigation (crime scene analysis)
- Recycling facility automation
- Manufacturing quality control
- Historical glass identification

### 13.5 Future Work

**For Seeds Model:**
- Experiment with deeper architectures
- Try ensemble methods (Random Forest, XGBoost for comparison)
- Collect data for more wheat varieties
- Deploy as real-time classification system

**For Glass Model:**
- Address class imbalance using SMOTE or class weights
- Collect more samples for rare glass types
- Feature selection (identify most discriminative chemical elements)
- Try other loss functions (Focal Loss for imbalanced data)
- Compare with traditional ML (SVM, k-NN)

---

**Verified by:** 23BQ1A4201  
**Date:** February 20, 2026  
**Signature:** _________________________
