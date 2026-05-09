
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import NearestCentroid

# =========================
# 1️⃣ Rocchio - Manual Class
# =========================
class RocchioClassifier:
    def __init__(self):
        self.class_centroids = {}
        self.classes_ = None

    def fit(self, X_train, y_train):
        """Compute class centroids"""
        self.classes_ = np.unique(y_train)
        X_train = X_train.toarray()  # Convert sparse to ndarray if TF-IDF
        for c in self.classes_:
            X_c = X_train[y_train == c]
            self.class_centroids[c] = np.mean(X_c, axis=0)
        return self

    def predict(self, X_test):
        X_test = X_test.toarray()
        predictions = []
        for x in X_test:
            sims = {c: cosine_similarity([x], [self.class_centroids[c]])[0][0] for c in self.classes_}
            best_class = max(sims, key=sims.get)
            predictions.append(best_class)
        return np.array(predictions)


# =========================
# 2️⃣ Maximum Entropy
# =========================
def train_maxent(X_train, y_train):
    maxent_model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
    maxent_model.fit(X_train, y_train)
    return maxent_model

# =========================
# 3️⃣ SVM
# =========================
def train_svm(X_train, y_train):
    svm_model = LinearSVC(max_iter=10000)
    svm_model.fit(X_train, y_train)
    return svm_model

# =========================
# 4️⃣ Rocchio - Using Library (Nearest Centroid)
# =========================
def train_rocchio_library(X_train, y_train):
    clf = NearestCentroid(metric='cosine')
    clf.fit(X_train, y_train)
    return clf

# =========================
# 5️⃣ Evaluation
# =========================
def evaluate_model(model, X_test, y_test, model_name="Model"):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"\n=== {model_name} Evaluation ===")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision (weighted): {precision:.4f}")
    print(f"Recall (weighted): {recall:.4f}")
    print(f"F1-score (weighted): {f1:.4f}")
    print("Sample Predictions (first 10):")
    print("Predicted:", y_pred[:10])
    print("Actual:   ", y_test[:10])
    
    return y_pred


# # import numpy as np
# # from sklearn.metrics.pairwise import cosine_similarity

# # class RocchioClassifier:
# #     def __init__(self):
# #         self.class_centroids = {}
# #         self.class_labels = None

# #     def fit(self, X_train, y_train, target_names=None):
# #         """
# #         Train Rocchio classifier by computing centroids per class.
        
# #         Parameters:
# #         - X_train: TF-IDF vectors (sparse matrix)
# #         - y_train: labels
# #         - target_names: optional class names
# #         """
# #         self.class_labels = np.unique(y_train)
# #         self.target_names = target_names

# #         for c in self.class_labels:
# #             # Select documents belonging to class c
# #             X_c = X_train[y_train == c]
            
# #             # Compute centroid (mean vector)
# #             centroid = X_c.mean(axis=0)
# #             self.class_centroids[c] = centroid

# #     def predict(self, X_test):
# #         """
# #         Predict labels for test set by comparing cosine similarity
# #         with centroids.
# #         """
# #         predictions = []

# #         for x in X_test:
# #             sims = []
# #             for c in self.class_labels:
# #                 # Cosine similarity between x and class centroid
# #                 sim = cosine_similarity(x, self.class_centroids[c])
# #                 sims.append((c, sim))
            
# #             # Pick class with highest similarity
# #             best_class = max(sims, key=lambda t: t[1])[0]
# #             predictions.append(best_class)

# #         return np.array(predictions)




# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity

# class RocchioClassifier:
#     def __init__(self):
#         self.class_centroids = {}
#         self.class_labels = None
#         self.target_names = None

#     def fit(self, X_train, y_train, target_names=None):
#         """
#         Train Rocchio classifier by computing centroids per class.
        
#         Parameters:
#         - X_train: TF-IDF vectors (sparse matrix)
#         - y_train: labels
#         - target_names: optional class names
#         """
#         self.class_labels = np.unique(y_train)
#         self.target_names = target_names

#         for c in self.class_labels:
#             # Select documents belonging to class c
#             X_c = X_train[y_train == c]
            

#             # Compute centroid (mean vector) -> convert to dense array
#             centroid = X_c.mean(axis=0).A1  # .A1 gives a flat numpy array
#             self.class_centroids[c] = centroid

#     def predict(self, X_test):
#         """
#         Predict labels for test set by comparing cosine similarity
#         with centroids.
#         """
#         predictions = []

#         for i in range(X_test.shape[0].toarray()):
#             x = X_test[i].toarray()  # convert sparse row to ndarray

#             sims = []
#             for c in self.class_labels:
#                 centroid = self.class_centroids[c].reshape(1, -1)  # 2D array
#                 sim = cosine_similarity(x, centroid)[0][0]  # scalar value
#                 sims.append((c, sim))

#             # Pick class with highest similarity
#             best_class = max(sims, key=lambda t: t[1])[0]
#             predictions.append(best_class)

#         return np.array(predictions)




# # from rocchio import RocchioClassifier
# from roch import RocchioClassifier

# # 3. Train Rocchio
# rocchio = RocchioClassifier()
# rocchio.fit(X_train_tfidf[:500], y_train[:500], target_names=newsgroups_train.target_names)

# # 4. Predict
# y_pred = rocchio.predict(X_test_tfidf[:200]) # test with 200 samples

# # 5. Evaluate
# print("Accuracy:", accuracy_score(y_test[:200], y_pred))

# # 6. Sample predictions
# print("Predicted:", y_pred[:10])
# print("Actual:   ", y_test[:10])


# # import numpy as np
# # from sklearn.metrics.pairwise import cosine_similarity

# # class RocchioClassifier:
# #     def __init__(self):
# #         self.class_centroids = {}
# #         self.class_labels = None

# #     def fit(self, X_train, y_train, target_names=None):
# #         self.class_labels = np.unique(y_train)
# #         self.target_names = target_names

# #         for c in self.class_labels:
# #             X_c = X_train[y_train == c]
# #             centroid = X_c.mean(axis=0)
# #             self.class_centroids[c] = np.asarray(centroid)  # ✅ ensure ndarray

# #     def predict(self, X_test):
# #         predictions = []

# #         for x in X_test:
# #             sims = []
# #             for c in self.class_labels:
# #                 sim = cosine_similarity(
# #                     np.asarray(x).reshape(1, -1), 
# #                     self.class_centroids[c].reshape(1, -1)
# #                 )[0][0]  # ✅ cosine_similarity returns [[val]]
# #                 sims.append((c, sim))

# #             best_class = max(sims, key=lambda t: t[1])[0]
# #             predictions.append(best_class)

# #         return np.array(predictions)
