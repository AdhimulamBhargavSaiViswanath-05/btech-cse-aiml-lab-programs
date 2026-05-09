# Lab 04: MNIST Handwritten Digit Classification using Deep MLP
## Step-by-Step Implementation Guide

---

## 📋 **OVERVIEW**

**AIM:** Implement and analyze a Deep Feedforward Neural Network (MLP) for handwritten digit classification on MNIST dataset without using CNNs.

**Key Learning:** Understand limitations of MLPs for image data, importance of regularization, and effects of hyperparameters.

---

## 🎯 **STEP 1: SETUP AND IMPORTS**

### Task 1.1: Import Required Libraries
```python
# Core libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Deep learning libraries
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam, SGD

# Sklearn utilities
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score

# Display settings
import warnings
warnings.filterwarnings('ignore')
```

### Task 1.2: Set Random Seeds for Reproducibility
```python
# Set seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)
```

---

## 🎯 **STEP 2: LOAD AND EXPLORE MNIST DATASET**

### Task 2.1: Load the MNIST Dataset
```python
# Load MNIST dataset from Keras
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()

# Display dataset information
print(f"Training samples: {X_train.shape[0]}")
print(f"Test samples: {X_test.shape[0]}")
print(f"Image shape: {X_train.shape[1:]} (28x28)")
print(f"Number of classes: {len(np.unique(y_train))}")
```

### Task 2.2: Visualize Sample Images
```python
# Display 10 sample images
plt.figure(figsize=(15, 3))
for i in range(10):
    plt.subplot(1, 10, i+1)
    plt.imshow(X_train[i], cmap='gray')
    plt.title(f"Label: {y_train[i]}")
    plt.axis('off')
plt.suptitle("Sample MNIST Images", fontsize=14)
plt.tight_layout()
plt.show()
```

### Task 2.3: Check Class Distribution
```python
# Check class distribution
unique, counts = np.unique(y_train, return_counts=True)
plt.figure(figsize=(10, 5))
plt.bar(unique, counts)
plt.xlabel("Digit Class")
plt.ylabel("Frequency")
plt.title("Training Data Class Distribution")
plt.xticks(unique)
plt.grid(axis='y', alpha=0.3)
plt.show()

print("\nClass distribution:")
for digit, count in zip(unique, counts):
    print(f"Digit {digit}: {count} samples")
```

---

## 🎯 **STEP 3: DATA PREPROCESSING**

### Task 3.1: Reshape Images (28x28 → 784)
```python
# Flatten images from (28, 28) to (784,)
X_train_flat = X_train.reshape(X_train.shape[0], -1)
X_test_flat = X_test.reshape(X_test.shape[0], -1)

print(f"Training data shape after flattening: {X_train_flat.shape}")
print(f"Test data shape after flattening: {X_test_flat.shape}")
```

### Task 3.2: Normalize Pixel Values (0-255 → 0-1)
```python
# Normalize pixel values to [0, 1]
X_train_norm = X_train_flat / 255.0
X_test_norm = X_test_flat / 255.0

print(f"Pixel value range before normalization: [{X_train_flat.min()}, {X_train_flat.max()}]")
print(f"Pixel value range after normalization: [{X_train_norm.min()}, {X_train_norm.max()}]")
```

### Task 3.3: One-Hot Encode Labels
```python
# One-hot encode labels
y_train_encoded = keras.utils.to_categorical(y_train, 10)
y_test_encoded = keras.utils.to_categorical(y_test, 10)

print(f"Label shape before encoding: {y_train.shape}")
print(f"Label shape after encoding: {y_train_encoded.shape}")
print(f"\nExample - Original label: {y_train[0]}")
print(f"One-hot encoded: {y_train_encoded[0]}")
```

### Task 3.4: Create Validation Split
```python
# Split training data into train and validation sets (80-20 split)
from sklearn.model_selection import train_test_split

X_train_final, X_val, y_train_final, y_val = train_test_split(
    X_train_norm, y_train_encoded, 
    test_size=0.2, 
    random_state=42, 
    stratify=y_train
)

print(f"Final training samples: {X_train_final.shape[0]}")
print(f"Validation samples: {X_val.shape[0]}")
print(f"Test samples: {X_test_norm.shape[0]}")
```

---

## 🎯 **STEP 4: EXPERIMENT 1 - BASELINE MODEL**

### Task 4.1: Build Baseline Architecture
**Architecture:** 784 → 512 → 256 → 10

```python
# Create baseline model
def create_baseline_model():
    model = Sequential([
        Dense(512, activation='relu', input_shape=(784,), name='hidden1'),
        Dense(256, activation='relu', name='hidden2'),
        Dense(10, activation='softmax', name='output')
    ])
    return model

baseline_model = create_baseline_model()
baseline_model.summary()
```

### Task 4.2: Calculate Total Parameters
```python
# Calculate total parameters manually
params_layer1 = (784 * 512) + 512  # weights + biases
params_layer2 = (512 * 256) + 256
params_output = (256 * 10) + 10

total_params = params_layer1 + params_layer2 + params_output

print(f"Layer 1 parameters: {params_layer1:,}")
print(f"Layer 2 parameters: {params_layer2:,}")
print(f"Output layer parameters: {params_output:,}")
print(f"Total parameters: {total_params:,}")
```

### Task 4.3: Compile the Model
```python
# Compile model
baseline_model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
```

### Task 4.4: Train the Model
```python
# Train baseline model
history_baseline = baseline_model.fit(
    X_train_final, y_train_final,
    validation_data=(X_val, y_val),
    epochs=20,
    batch_size=128,
    verbose=1
)
```

### Task 4.5: Evaluate on Test Set
```python
# Evaluate baseline model
test_loss, test_accuracy = baseline_model.evaluate(X_test_norm, y_test_encoded)
print(f"\n✅ Baseline Model Test Accuracy: {test_accuracy * 100:.2f}%")
print(f"✅ Baseline Model Test Loss: {test_loss:.4f}")
```

### Task 4.6: Plot Training History
```python
# Plot accuracy and loss curves
def plot_history(history, title="Model Training History"):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Accuracy plot
    axes[0].plot(history.history['accuracy'], label='Train Accuracy')
    axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].set_title(f'{title} - Accuracy')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Loss plot
    axes[1].plot(history.history['loss'], label='Train Loss')
    axes[1].plot(history.history['val_loss'], label='Validation Loss')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].set_title(f'{title} - Loss')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()

plot_history(history_baseline, "Baseline Model")
```

### Task 4.7: Generate Confusion Matrix
```python
# Confusion matrix for baseline model
y_pred_baseline = baseline_model.predict(X_test_norm)
y_pred_classes = np.argmax(y_pred_baseline, axis=1)

cm = confusion_matrix(y_test, y_pred_classes)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=range(10), yticklabels=range(10))
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix - Baseline Model')
plt.show()
```

### Task 4.8: Classification Report
```python
# Detailed classification report
print("\n📊 Classification Report - Baseline Model:")
print(classification_report(y_test, y_pred_classes, target_names=[str(i) for i in range(10)]))
```

---

## 🎯 **STEP 5: EXPERIMENT 2 - DEEP NETWORK**

### Task 5.1: Build Deep Architecture (4-5 Hidden Layers)
**Architecture:** 784 → 512 → 256 → 128 → 64 → 10

```python
# Create deep model
def create_deep_model():
    model = Sequential([
        Dense(512, activation='relu', input_shape=(784,), name='hidden1'),
        Dense(256, activation='relu', name='hidden2'),
        Dense(128, activation='relu', name='hidden3'),
        Dense(64, activation='relu', name='hidden4'),
        Dense(10, activation='softmax', name='output')
    ])
    return model

deep_model = create_deep_model()
deep_model.summary()
```

### Task 5.2: Compile and Train Deep Model
```python
# Compile
deep_model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train
history_deep = deep_model.fit(
    X_train_final, y_train_final,
    validation_data=(X_val, y_val),
    epochs=20,
    batch_size=128,
    verbose=1
)
```

### Task 5.3: Evaluate Deep Model
```python
# Evaluate
test_loss_deep, test_accuracy_deep = deep_model.evaluate(X_test_norm, y_test_encoded)
print(f"\n✅ Deep Model Test Accuracy: {test_accuracy_deep * 100:.2f}%")
print(f"✅ Deep Model Test Loss: {test_loss_deep:.4f}")

# Plot history
plot_history(history_deep, "Deep Model")
```

---

## 🎯 **STEP 6: EXPERIMENT 3 - OVERFITTING STUDY**

### Task 6.1: Model WITHOUT Dropout (Observe Overfitting)
```python
# Model without regularization
def create_overfit_model():
    model = Sequential([
        Dense(1024, activation='relu', input_shape=(784,), name='hidden1'),
        Dense(512, activation='relu', name='hidden2'),
        Dense(256, activation='relu', name='hidden3'),
        Dense(10, activation='softmax', name='output')
    ])
    return model

overfit_model = create_overfit_model()
overfit_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train for more epochs to observe overfitting
history_overfit = overfit_model.fit(
    X_train_final, y_train_final,
    validation_data=(X_val, y_val),
    epochs=30,
    batch_size=128,
    verbose=1
)

plot_history(history_overfit, "Overfitting Model (No Dropout)")
```

### Task 6.2: Analyze Overfitting
```python
# Compare train vs validation accuracy
final_train_acc = history_overfit.history['accuracy'][-1]
final_val_acc = history_overfit.history['val_accuracy'][-1]

print(f"\n📈 Final Training Accuracy: {final_train_acc * 100:.2f}%")
print(f"📉 Final Validation Accuracy: {final_val_acc * 100:.2f}%")
print(f"⚠️  Overfitting Gap: {(final_train_acc - final_val_acc) * 100:.2f}%")
```

---

## 🎯 **STEP 7: EXPERIMENT 4 - REGULARIZATION STUDY**

### Task 7.1: Model WITH Dropout
```python
# Model with dropout
def create_dropout_model():
    model = Sequential([
        Dense(512, activation='relu', input_shape=(784,), name='hidden1'),
        Dropout(0.3),
        Dense(256, activation='relu', name='hidden2'),
        Dropout(0.3),
        Dense(128, activation='relu', name='hidden3'),
        Dropout(0.3),
        Dense(10, activation='softmax', name='output')
    ])
    return model

dropout_model = create_dropout_model()
dropout_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history_dropout = dropout_model.fit(
    X_train_final, y_train_final,
    validation_data=(X_val, y_val),
    epochs=20,
    batch_size=128,
    verbose=1
)

plot_history(history_dropout, "Model with Dropout")
```

### Task 7.2: Model WITH L2 Regularization
```python
# Model with L2 regularization
def create_l2_model():
    model = Sequential([
        Dense(512, activation='relu', kernel_regularizer=l2(0.001), input_shape=(784,)),
        Dense(256, activation='relu', kernel_regularizer=l2(0.001)),
        Dense(128, activation='relu', kernel_regularizer=l2(0.001)),
        Dense(10, activation='softmax')
    ])
    return model

l2_model = create_l2_model()
l2_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history_l2 = l2_model.fit(
    X_train_final, y_train_final,
    validation_data=(X_val, y_val),
    epochs=20,
    batch_size=128,
    verbose=1
)

plot_history(history_l2, "Model with L2 Regularization")
```

### Task 7.3: Model WITH Dropout + L2 + Early Stopping
```python
# Complete regularization
def create_regularized_model():
    model = Sequential([
        Dense(512, activation='relu', kernel_regularizer=l2(0.001), input_shape=(784,)),
        Dropout(0.4),
        Dense(256, activation='relu', kernel_regularizer=l2(0.001)),
        Dropout(0.4),
        Dense(128, activation='relu', kernel_regularizer=l2(0.001)),
        Dropout(0.3),
        Dense(10, activation='softmax')
    ])
    return model

reg_model = create_regularized_model()
reg_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Early stopping callback
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

history_reg = reg_model.fit(
    X_train_final, y_train_final,
    validation_data=(X_val, y_val),
    epochs=50,
    batch_size=128,
    callbacks=[early_stop],
    verbose=1
)

plot_history(history_reg, "Fully Regularized Model")

# Evaluate
test_loss_reg, test_accuracy_reg = reg_model.evaluate(X_test_norm, y_test_encoded)
print(f"\n✅ Regularized Model Test Accuracy: {test_accuracy_reg * 100:.2f}%")
```

---

## 🎯 **STEP 8: EXPERIMENT 5 - HYPERPARAMETER TUNING**

### Task 8.1: Vary Learning Rate
```python
# Test different learning rates
learning_rates = [0.0001, 0.001, 0.01]
lr_results = {}

for lr in learning_rates:
    print(f"\n🔄 Training with learning rate: {lr}")
    
    model = create_baseline_model()
    model.compile(
        optimizer=Adam(learning_rate=lr),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    history = model.fit(
        X_train_final, y_train_final,
        validation_data=(X_val, y_val),
        epochs=15,
        batch_size=128,
        verbose=0
    )
    
    test_loss, test_acc = model.evaluate(X_test_norm, y_test_encoded, verbose=0)
    lr_results[lr] = test_acc
    print(f"✅ Test Accuracy with LR={lr}: {test_acc * 100:.2f}%")

# Compare learning rates
print("\n📊 Learning Rate Comparison:")
for lr, acc in lr_results.items():
    print(f"LR={lr}: {acc * 100:.2f}%")
```

### Task 8.2: Vary Batch Size
```python
# Test different batch sizes
batch_sizes = [32, 64, 128, 256]
batch_results = {}

for bs in batch_sizes:
    print(f"\n🔄 Training with batch size: {bs}")
    
    model = create_baseline_model()
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    history = model.fit(
        X_train_final, y_train_final,
        validation_data=(X_val, y_val),
        epochs=15,
        batch_size=bs,
        verbose=0
    )
    
    test_loss, test_acc = model.evaluate(X_test_norm, y_test_encoded, verbose=0)
    batch_results[bs] = test_acc
    print(f"✅ Test Accuracy with Batch Size={bs}: {test_acc * 100:.2f}%")

# Compare batch sizes
print("\n📊 Batch Size Comparison:")
for bs, acc in batch_results.items():
    print(f"Batch Size={bs}: {acc * 100:.2f}%")
```

### Task 8.3: Vary Network Width
```python
# Test different neuron counts
neuron_configs = [
    [128, 64],
    [256, 128],
    [512, 256],
    [1024, 512]
]

width_results = {}

for neurons in neuron_configs:
    print(f"\n🔄 Training with neurons: {neurons}")
    
    model = Sequential([
        Dense(neurons[0], activation='relu', input_shape=(784,)),
        Dense(neurons[1], activation='relu'),
        Dense(10, activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    history = model.fit(
        X_train_final, y_train_final,
        validation_data=(X_val, y_val),
        epochs=15,
        batch_size=128,
        verbose=0
    )
    
    test_loss, test_acc = model.evaluate(X_test_norm, y_test_encoded, verbose=0)
    width_results[str(neurons)] = test_acc
    print(f"✅ Test Accuracy: {test_acc * 100:.2f}%")
```

---

## 🎯 **STEP 9: EXPERIMENT 6 - OPTIMIZER COMPARISON**

### Task 9.1: Compare SGD vs Adam
```python
# Adam optimizer
model_adam = create_baseline_model()
model_adam.compile(optimizer=Adam(learning_rate=0.001), 
                   loss='categorical_crossentropy', metrics=['accuracy'])

history_adam = model_adam.fit(
    X_train_final, y_train_final,
    validation_data=(X_val, y_val),
    epochs=20,
    batch_size=128,
    verbose=1
)

# SGD optimizer
model_sgd = create_baseline_model()
model_sgd.compile(optimizer=SGD(learning_rate=0.01, momentum=0.9), 
                  loss='categorical_crossentropy', metrics=['accuracy'])

history_sgd = model_sgd.fit(
    X_train_final, y_train_final,
    validation_data=(X_val, y_val),
    epochs=20,
    batch_size=128,
    verbose=1
)

# Evaluate both
_, acc_adam = model_adam.evaluate(X_test_norm, y_test_encoded, verbose=0)
_, acc_sgd = model_sgd.evaluate(X_test_norm, y_test_encoded, verbose=0)

print(f"\n✅ Adam Optimizer Test Accuracy: {acc_adam * 100:.2f}%")
print(f"✅ SGD Optimizer Test Accuracy: {acc_sgd * 100:.2f}%")
```

### Task 9.2: Visualize Optimizer Comparison
```python
# Plot comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy
axes[0].plot(history_adam.history['val_accuracy'], label='Adam')
axes[0].plot(history_sgd.history['val_accuracy'], label='SGD')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Validation Accuracy')
axes[0].set_title('Optimizer Comparison - Accuracy')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Loss
axes[1].plot(history_adam.history['val_loss'], label='Adam')
axes[1].plot(history_sgd.history['val_loss'], label='SGD')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Validation Loss')
axes[1].set_title('Optimizer Comparison - Loss')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 🎯 **STEP 10: COMPREHENSIVE RESULTS SUMMARY**

### Task 10.1: Create Comparison Table
```python
# Create summary DataFrame
results_summary = pd.DataFrame({
    'Model': [
        'Baseline (2 layers)',
        'Deep (4 layers)',
        'No Dropout (Overfitting)',
        'With Dropout',
        'With L2',
        'Full Regularization',
        'Adam Optimizer',
        'SGD Optimizer'
    ],
    'Test Accuracy (%)': [
        test_accuracy * 100,
        test_accuracy_deep * 100,
        # Add your results here
        0.0,  # Replace with actual value
        0.0,  # Replace with actual value
        0.0,  # Replace with actual value
        test_accuracy_reg * 100,
        acc_adam * 100,
        acc_sgd * 100
    ],
    'Parameters': [
        baseline_model.count_params(),
        deep_model.count_params(),
        # Add your parameter counts
        0,
        0,
        0,
        reg_model.count_params(),
        model_adam.count_params(),
        model_sgd.count_params()
    ]
})

print("\n" + "="*60)
print("📊 COMPREHENSIVE RESULTS SUMMARY")
print("="*60)
print(results_summary.to_string(index=False))
print("="*60)
```

### Task 10.2: Best Model Selection
```python
# Identify best model
best_accuracy = results_summary['Test Accuracy (%)'].max()
best_model_name = results_summary.loc[results_summary['Test Accuracy (%)'].idxmax(), 'Model']

print(f"\n🏆 Best Model: {best_model_name}")
print(f"🎯 Best Accuracy: {best_accuracy:.2f}%")
```

---

## 🎯 **STEP 11: ANALYSIS AND INSIGHTS**

### Task 11.1: Answer Analysis Questions

Create a markdown cell and answer these questions:

**Q1: Why does MNIST require more neurons than Iris?**
- Your answer here...

**Q2: Compute total number of parameters in your baseline model.**
```python
# Show calculation
print(f"Total parameters: {total_params:,}")
```

**Q3: Why is softmax necessary for multi-class classification?**
- Your answer here...

**Q4: Why does overfitting occur more severely in MLPs for image data?**
- Your answer here...

**Q5: Compare training and validation curves.**
- Analyze the plots you generated...

**Q6: What is the effect of dropout?**
- Compare models with and without dropout...

**Q7: Why are CNNs preferred for image tasks?**
- Your answer here...

**Q8: How many parameters does your deepest model contain?**
```python
print(f"Deepest model parameters: {deep_model.count_params():,}")
```

**Q9: Which optimizer performed best and why?**
- Compare Adam vs SGD results...

**Q10: What is the best accuracy achieved without CNNs?**
```python
print(f"Best accuracy: {best_accuracy:.2f}%")
```

---

## ✅ **DELIVERABLES CHECKLIST**

- [ ] Python Notebook with all experiments
- [ ] Printed outputs of all models
- [ ] Confusion matrices for each major model
- [ ] Accuracy/loss plots for all experiments
- [ ] Comparative summary table
- [ ] Insights section (minimum 1 page analysis)
- [ ] Answers to all 10 analysis questions
- [ ] Record with VIVA questions answered

---

## 📌 **IMPORTANT NOTES**

1. **Run each section sequentially** - Don't skip steps
2. **Save your notebook frequently** - Ctrl+S after each experiment
3. **Keep all outputs** - Don't clear cells
4. **Take screenshots** of key visualizations
5. **Write detailed insights** - Explain what you observe
6. **Compare results** - Always compare with baseline
7. **Document observations** - Note any interesting patterns

---

## 🎓 **EXPECTED PERFORMANCE BENCHMARKS**

- Simple MLP: ~96-97%
- Deeper MLP with tuning: ~97-98%
- Cannot match CNN: ~99%+

---

## 🔍 **DEBUGGING TIPS**

If you encounter issues:

1. **Shape mismatch errors**: Check data preprocessing steps
2. **Low accuracy**: Verify normalization and one-hot encoding
3. **Overfitting**: Add more dropout or regularization
4. **Slow training**: Reduce model size or increase batch size
5. **Memory errors**: Reduce batch size or model width

---

**Good Luck! 🚀**

Remember: The goal is to understand **why** MLPs have limitations for images and **how** regularization helps!
