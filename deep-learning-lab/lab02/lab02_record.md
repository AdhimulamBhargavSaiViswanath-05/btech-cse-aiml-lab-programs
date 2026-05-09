# Lab 02: Artificial Neural Network (ANN) for Regression Tasks
**Student ID:** 23BQ1A4201  
**Date:** February 20, 2026  
**Lab:** Deep Learning Lab - Experiment 02

---

## 1. AIM

To implement and evaluate Artificial Neural Networks (ANNs) for regression tasks on two different datasets:
1. **Spotify Dataset**: Predicting song popularity based on audio features
2. **Air Quality Dataset**: Predicting NO2 concentration based on environmental pollutants and meteorological factors

---

## 2. LIST OF LIBRARIES & METHODS USED

### Libraries:
- **pandas** (`pd`): Data manipulation and analysis
- **numpy** (`np`): Numerical computations and array operations
- **matplotlib.pyplot** (`plt`): Data visualization and plotting
- **seaborn** (`sns`): Statistical data visualization
- **sklearn.preprocessing.MinMaxScaler**: Feature normalization (0-1 scaling)
- **sklearn.model_selection.train_test_split**: Dataset splitting
- **sklearn.metrics**: Model evaluation (MSE, MAE, R² Score)
- **tensorflow** (`tf`): Deep learning framework
- **tensorflow.keras.models.Sequential**: Sequential neural network model
- **tensorflow.keras.layers**: Dense, Input, Dropout layers
- **tensorflow.keras.callbacks.EarlyStopping**: Training regularization
- **tensorflow.keras.optimizers.Adam**: Optimization algorithm

### Methods/Techniques:
1. **Data Preprocessing**: Missing value imputation, normalization, correlation analysis
2. **Feature Engineering**: Log transformation (log1p) for skewed features
3. **Feed-Forward Neural Networks (FFNN)**: Multi-layer perceptron architecture
4. **Regularization**: Dropout layers, Early Stopping
5. **Optimization**: Adam optimizer with custom learning rates
6. **Loss Functions**: Huber Loss (Spotify), MSE (Air Quality)

---

## 3. DETAILED DESCRIPTION OF DATASETS

### 3.1 Spotify Features Dataset

**File:** `spotify_features.csv`

**Description:**  
The Spotify dataset contains audio features and metadata for songs with their popularity scores.

**Dataset Size:** 232,725 samples with 18 columns

**Key Features:**
- **Input Features (10):**
  - `danceability`: How suitable a track is for dancing (0-1)
  - `energy`: Intensity and activity measure (0-1)
  - `loudness`: Overall loudness in decibels (dB)
  - `tempo`: Beats per minute (BPM)
  - `acousticness`: Confidence measure of acoustic content (0-1)
  - `speechiness`: Presence of spoken words (0-1)
  - `instrumentalness`: Predicts voice absence (0-1)
  - `liveness`: Presence of audience in recording (0-1)
  - `valence`: Musical positiveness (0-1)
  - `duration_ms`: Track duration in milliseconds

- **Target Variable:**
  - `popularity`: Song popularity score (0-100)

**Preprocessing Steps:**
1. Missing values filled with 0
2. Log transformation applied to `duration_ms` to reduce dominance
3. MinMax normalization (0-1) on all features
4. Log1p transformation + normalization on target variable
5. Correlation analysis: Dropped features with correlation > 0.85
6. Feature encoding (categorical variables) resulting in 50 total features
7. Train-test split: 80% training (186,180 samples), 20% testing (46,545 samples)

### 3.2 Air Quality Dataset

**File:** `air_quality_data.csv`

**Description:**  
The Air Quality dataset contains measurements from chemical sensors monitoring air pollutants and meteorological conditions.

**Dataset Size:** 9,357 samples with 7 input features and 1 target variable

**Key Features:**
- **Input Features (7):**
  - `CO(GT)`: True hourly averaged CO concentration (mg/m³)
  - `NMHC(GT)`: Non-Methane Hydrocarbons concentration (μg/m³)
  - `C6H6(GT)`: True hourly averaged Benzene concentration (μg/m³)
  - `NOx(GT)`: True hourly averaged NOx concentration (ppb)
  - `T`: Temperature (°C)
  - `RH`: Relative Humidity (%)
  - `AH`: Absolute Humidity

- **Target Variable:**
  - `NO2(GT)`: True hourly averaged NO2 concentration (μg/m³)

**Preprocessing Steps:**
1. MinMax normalization (0-1) applied to all features
2. MinMax normalization applied to target variable
3. Train-test split: 80% training (7,485 samples), 20% testing (1,872 samples) with random_state=42

---

## 4. DETAILS OF MODEL ARCHITECTURE

### 4.1 Spotify Popularity Prediction Model

**Architecture:**
```
Input Layer      → (50 features after encoding)
Hidden Layer 1   → 256 neurons, ReLU activation
Dropout         → 0.2 (20% dropout)
Hidden Layer 2   → 128 neurons, ReLU activation
Dropout         → 0.2
Hidden Layer 3   → 64 neurons, ReLU activation
Dropout         → 0.2
Hidden Layer 4   → 32 neurons, ReLU activation
Output Layer     → 1 neuron, Linear activation
```

**Total Parameters:** 56,321 (220.00 KB)
- Trainable params: 56,321
- Non-trainable params: 0

**Note:** After feature engineering and encoding, the model uses 50 input features (expanded from original 10 audio features through one-hot encoding and feature transformations).

**Activation Functions:**
- Hidden Layers: ReLU (Rectified Linear Unit)
  - Formula: $f(x) = \max(0, x)$
  - Advantage: Prevents vanishing gradient, computationally efficient
- Output Layer: Linear
  - Formula: $f(x) = x$
  - Suitable for continuous value prediction

### 4.2 Air Quality NO2 Prediction Model

**Architecture:**
```
Input Layer      → (7 features)
Hidden Layer 1   → 128 neurons, ReLU activation
Hidden Layer 2   → 64 neurons, ReLU activation
Hidden Layer 3   → 32 neurons, ReLU activation
Hidden Layer 4   → 16 neurons, ReLU activation
Output Layer     → 1 neuron, Sigmoid activation
```

**Total Parameters:** 11,905 (46.50 KB)
- Trainable params: 11,905
- Non-trainable params: 0

**Activation Functions:**
- Hidden Layers: ReLU
- Output Layer: Sigmoid
  - Formula: $f(x) = \frac{1}{1 + e^{-x}}$
  - Output range: (0, 1) - matches normalized target

---

## 5. OPTIMIZATION TECHNIQUES & HYPERPARAMETERS

### 5.1 Spotify Model

**Optimizer:** Adam (Adaptive Moment Estimation)
- **Learning Rate:** 0.0005 (reduced for stability)
- **Beta1:** 0.9 (default, exponential decay rate for first moment)
- **Beta2:** 0.999 (default, exponential decay rate for second moment)

**Loss Function:** Huber Loss
- Formula: $L_\delta(y, f(x)) = \begin{cases} \frac{1}{2}(y - f(x))^2 & \text{for } |y - f(x)| \leq \delta \\ \delta \cdot (|y - f(x)| - \frac{1}{2}\delta) & \text{otherwise} \end{cases}$
- **Advantage:** Robust to outliers, combines MSE and MAE benefits
- **Choice Rationale:** Reduces impact of heteroscedastic variance in popularity scores

**Training Hyperparameters:**
- **Epochs:** 200 (maximum)
- **Batch Size:** 128
- **Validation Split:** 0.2 (20% of training data)

**Regularization:**
- **Dropout Rate:** 0.2 (prevents co-adaptation of neurons)
- **Early Stopping:**
  - Monitor: `val_loss`
  - Patience: 20 epochs
  - Restore best weights: Enabled

### 5.2 Air Quality Model

**Optimizer:** Adam
- **Learning Rate:** 0.001

**Loss Function:** Mean Squared Error (MSE)
- Formula: $\text{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$

**Training Hyperparameters:**
- **Epochs:** 200 (maximum)
- **Batch Size:** 64
- **Validation Split:** 0.2

**Regularization:**
- **Early Stopping:**
  - Monitor: `val_loss`
  - Patience: 20 epochs
  - Restore best weights: Enabled

---

## 6. MATHEMATICAL ANALYSIS

### 6.1 Forward Propagation

For each layer $l$ in the network:

$$z^{[l]} = W^{[l]} \cdot a^{[l-1]} + b^{[l]}$$

$$a^{[l]} = g^{[l]}(z^{[l]})$$

Where:
- $W^{[l]}$ = weight matrix for layer $l$
- $b^{[l]}$ = bias vector for layer $l$
- $a^{[l-1]}$ = activation from previous layer
- $g^{[l]}$ = activation function (ReLU/Linear/Sigmoid)

### 6.2 Backpropagation

Gradient computation using chain rule:

$$\frac{\partial L}{\partial W^{[l]}} = \frac{\partial L}{\partial a^{[l]}} \cdot \frac{\partial a^{[l]}}{\partial z^{[l]}} \cdot \frac{\partial z^{[l]}}{\partial W^{[l]}}$$

### 6.3 Adam Optimizer Update Rule

$$m_t = \beta_1 \cdot m_{t-1} + (1 - \beta_1) \cdot g_t$$
$$v_t = \beta_2 \cdot v_{t-1} + (1 - \beta_2) \cdot g_t^2$$

Bias-corrected estimates:
$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}$$
$$\hat{v}_t = \frac{v_t}{1 - \beta_2^t}$$

Parameter update:
$$\theta_t = \theta_{t-1} - \alpha \cdot \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}$$

### 6.4 Dropout Regularization

During training, randomly drop neurons with probability $p$:

$$a^{[l]} = \text{dropout}(a^{[l]}, p)$$

Scaling during inference:
$$a^{[l]}_{\text{inference}} = (1-p) \cdot a^{[l]}_{\text{training}}$$

### 6.5 Evaluation Metrics

**Mean Squared Error (MSE):**
$$\text{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

**Root Mean Squared Error (RMSE):**
$$\text{RMSE} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2}$$

**Mean Absolute Error (MAE):**
$$\text{MAE} = \frac{1}{n}\sum_{i=1}^{n}|y_i - \hat{y}_i|$$

**R² Score (Coefficient of Determination):**
$$R^2 = 1 - \frac{\sum_{i=1}^{n}(y_i - \hat{y}_i)^2}{\sum_{i=1}^{n}(y_i - \bar{y})^2}$$

Where $\bar{y}$ is the mean of actual values.

---

## 7. CODE

The complete implementation is available in the following Jupyter notebooks:

1. **Spotify Dataset:** `lab02/spotify.ipynb`
2. **Air Quality Dataset:** `lab02/air_quality.ipynb`

**Key Code Sections:**

### 7.1 Data Loading & Preprocessing
```python
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load data
spotify_df = pd.read_csv("datasets/spotify_features.csv")
air_quality_df = pd.read_csv("datasets/air_quality_data.csv")

# Normalize features
scaler_X = MinMaxScaler()
X_normalized = scaler_X.fit_transform(X)
```

### 7.2 Model Building (Spotify)
```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Dropout

spotify_model = Sequential([
    Input(shape=(len(features_spotify),)),
    Dense(256, activation='relu'),
    Dropout(0.2),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(1, activation='linear')
])
```

### 7.3 Model Compilation
```python
from tensorflow.keras.optimizers import Adam

spotify_model.compile(
    optimizer=Adam(learning_rate=0.0005),
    loss=tf.keras.losses.Huber(),
    metrics=['mae']
)
```

### 7.4 Training with Early Stopping
```python
from tensorflow.keras.callbacks import EarlyStopping

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=20,
    restore_best_weights=True
)

history = spotify_model.fit(
    X_train, y_train,
    validation_split=0.2,
    epochs=200,
    batch_size=128,
    callbacks=[early_stopping]
)
```

---

## 8. TEST CASES

### 8.1 Spotify Model - Sample Predictions

**Test Set Size:** 46,545 samples (20% of dataset)

**Sample Outputs (from actual model predictions):**

| Test Case | Actual Popularity | Predicted Popularity | Error  |
|-----------|-------------------|----------------------|--------|
| 1         | 45.0              | 44.77                | 0.23   |
| 2         | 25.0              | 32.56                | -7.56  |
| 3         | 19.0              | 33.76                | -14.76 |
| 4         | 29.0              | 36.23                | -7.23  |
| 5         | 17.0              | 21.58                | -4.58  |
| 6         | 16.0              | 1.60                 | 14.40  |
| 7         | 63.0              | 65.36                | -2.36  |
| 8         | 51.0              | 58.26                | -7.26  |
| 9         | 41.0              | 46.24                | -5.24  |
| 10        | 65.0              | 46.52                | 18.48  |

### 8.2 Air Quality Model - Sample Predictions

**Test Set Size:** 1,872 samples (20% of dataset)

**Sample Outputs (Normalized, from actual model predictions):**

| Test Case | Actual NO2 | Predicted NO2 | Error   |
|-----------|------------|---------------|---------|
| 1         | 0.5037     | 0.5410        | -0.0373 |
| 2         | 0.4593     | 0.4615        | -0.0022 |
| 3         | 0.6407     | 0.6345        | 0.0062  |
| 4         | 0.6815     | 0.6868        | -0.0053 |
| 5         | 0.7407     | 0.6603        | 0.0804  |
| 6         | 0.0000     | 0.0004        | -0.0004 |
| 7         | 0.6296     | 0.5960        | 0.0336  |
| 8         | 0.5389     | 0.5563        | -0.0174 |
| 9         | 0.4685     | 0.4885        | -0.0200 |
| 10        | 0.4944     | 0.5114        | -0.0170 |

---

## 9. GRAPHS AND PLOTS

### 9.1 Spotify Dataset Visualizations

1. **Distribution of Popularity**
   - Histogram showing the distribution of song popularity scores
   - Shows right-skewed distribution with most songs having moderate popularity

2. **Boxplot of Input Features**
   - Identifies outliers in features like loudness, tempo, duration_ms
   - Shows feature value ranges after normalization

3. **Correlation Heatmap**
   - Feature correlation matrix
   - High correlation between energy and loudness
   - Negative correlation between acousticness and energy

4. **Training vs Validation Loss**
   - Loss curves over epochs
   - Shows convergence around epoch ~80-100
   - Early stopping prevents overfitting

5. **Actual vs Predicted Popularity**
   - Scatter plot with perfect prediction line (red dashed)
   - Points clustered around diagonal indicate good predictions
   - Some variance at extreme values

6. **Residuals Plot**
   - Residuals vs Predicted values
   - Random scatter around zero indicates unbiased predictions
   - Slight heteroscedasticity visible at extremes

### 9.2 Air Quality Dataset Visualizations

1. **Distribution of NO2(GT)**
   - Histogram showing normalized NO2 concentration distribution
   - Near-normal distribution after normalization

2. **Boxplot of Input Features**
   - Shows feature ranges and outliers
   - Identifies potential data quality issues

3. **Correlation Heatmap**
   - Strong correlation between NOx and NO2 (expected)
   - Moderate correlation between benzene (C6H6) and NO2
   - Weak correlation with meteorological factors (T, RH, AH)

4. **Training vs Validation Loss**
   - Both curves decrease and converge
   - Early stopping triggered around epoch ~60-80
   - No significant overfitting observed

5. **Actual vs Predicted NO2**
   - Scatter plot with diagonal reference line
   - Strong linear relationship visible
   - Good prediction accuracy across value ranges

6. **Residuals Plot**
   - Residuals randomly distributed around zero
   - Homoscedastic pattern (constant variance)
   - Few outliers present

---

## 10. CONCLUSION

### 10.1 Spotify Popularity Prediction

**Model Performance (Normalized Scale):**
- **MSE:** 0.0104
- **RMSE:** 0.1019
- **MAE:** 0.0556
- **R² Score:** 0.6732

**Model Performance (Original Scale):**
- **MSE:** 95.8091
- **RMSE:** 9.7882 popularity points
- **MAE:** 7.1936 popularity points
- **R² Score:** 0.7123

**Key Findings:**
1. Audio features alone provide moderate prediction capability for song popularity
2. Popularity is influenced by non-musical factors (marketing, artist fame, timing) not captured in dataset
3. Model struggles with extreme popularity values (very low and very high)
4. Dropout and early stopping effectively prevented overfitting
5. Huber loss helped manage outliers better than standard MSE

**Challenges:**
- High variance in popularity scores for similar audio features
- Limited features (doesn't include artist popularity, release date, genre nuances)
- Skewed distribution of popularity scores

### 10.2 Air Quality NO2 Prediction

**Model Performance (Normalized Scale):**
- **MSE:** 0.0012
- **RMSE:** 0.0352
- **MAE:** 0.0221
- **R² Score:** 0.9766 (excellent predictive power)

**Key Findings:**
1. Strong relationship between chemical pollutants and NO2 concentration
2. NOx(GT) is the strongest predictor (chemically related to NO2)
3. Model achieves high accuracy with relatively simple architecture
4. Meteorological factors (T, RH, AH) provide additional predictive value
5. Sigmoid activation in output layer ensures predictions stay within normalized range

**Practical Applications:**
- Real-time air quality monitoring and forecasting
- Environmental policy decision support
- Public health alert systems
- Urban planning and traffic management

### 10.3 Comparative Analysis

| Aspect                    | Spotify Model         | Air Quality Model    |
|---------------------------|-----------------------|----------------------|
| **Dataset Size**          | 232,725 samples       | 9,357 samples        |
| **Input Features**        | 50 (after encoding)   | 7                    |
| **Model Parameters**      | 56,321                | 11,905               |
| **Complexity**            | Higher (4 layers)     | Moderate (4 layers)  |
| **Regularization**        | Dropout + Early Stop  | Early Stop only      |
| **Performance (R²)**      | 0.7123                | 0.9766               |
| **RMSE (original)**       | 9.79 points           | N/A (normalized)     |
| **MAE (normalized)**      | 0.0556                | 0.0221               |
| **Challenge**             | Non-musical factors   | Sensor noise         |
| **Interpretability**      | Low                   | High (chemistry)     |

### 10.4 Learning Outcomes

1. Successfully implemented ANNs for regression tasks
2. Understood importance of data preprocessing and normalization
3. Learned to select appropriate loss functions (MSE vs Huber)
4. Applied regularization techniques (dropout, early stopping)
5. Evaluated models using multiple metrics (MSE, RMSE, MAE, R²)
6. Visualized model performance and residuals
7. Interpreted results in context of problem domain

### 10.5 Future Improvements

**For Spotify Model:**
- Include additional features (artist popularity, genre, release date)
- Try ensemble methods or more complex architectures
- Experiment with different loss functions
- Collect more recent data with social media metrics

**For Air Quality Model:**
- Incorporate temporal dependencies (LSTM/GRU)
- Add weather forecast features
- Ensemble with traditional statistical models
- Deploy for real-time monitoring

---

**Verified by:** 23BQ1A4201  
**Date:** February 20, 2026  
**Signature:** _________________________
