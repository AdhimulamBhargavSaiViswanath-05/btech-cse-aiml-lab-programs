# Lab 06: One-Hot Encoding of Words and Characters using Python and Keras
**Student ID:** 23BQ1A4201  
**Date:** March 18, 2026  
**Lab:** Deep Learning Lab - Experiment 06

---

## 1. AIM

To implement one-hot encoding at both **word level** and **character level** using Python and NumPy, and to implement Keras `one_hot()` encoding (hashing trick) with fixed-size encoding and basic collision understanding.

---

## 2. INTRODUCTION

Neural networks operate on numeric vectors, while natural language is made of discrete symbols (characters/words). Therefore, we need a representation method to convert symbols into numbers.

One-hot encoding is the simplest representation:
- each unique symbol gets a unique index,
- vector size = vocabulary size,
- exactly one position is `1`, all others are `0`.

### Key property
One-hot encoding assumes only symbol identity (distinctness). It does **not** encode semantic similarity.

---

## 3. LIBRARIES AND TOOLS USED

- `numpy` for manual one-hot vector creation
- `tensorflow.keras.preprocessing.text.one_hot` for hash-based word encoding
- `tensorflow.keras.preprocessing.sequence.pad_sequences` for equal-length sequence formatting
- `tensorflow.keras.preprocessing.text.Tokenizer` for vocabulary building and binary matrix representation

---

## 4. THEORY AND FORMAL DEFINITION

Let vocabulary be:

$$V = \{w_1, w_2, \dots, w_N\}$$

Assign each word $w_i$ an index $i$. Its one-hot vector is the standard basis vector $e_i \in \mathbb{R}^N$:

$$e_i[j] = \begin{cases}
1, & j=i \\
0, & j\neq i
\end{cases}$$

For example, if $V = \{cat, dog, fish, bird\}$:
- $onehot(cat) = [1,0,0,0]$
- $onehot(dog) = [0,1,0,0]$
- $onehot(fish) = [0,0,1,0]$
- $onehot(bird) = [0,0,0,1]$

---

## 5. IMPLEMENTATION PARTS

## 5.1 PART A: Manual Word-Level One-Hot Encoding

### Code idea
- Create vocabulary list
- Map each word to index
- Build zero vector of size vocabulary
- Set index position to 1

### Notebook implementation summary
- Example used: `words = ["cat", "dog", "fish"]`
- Vocabulary mapping: `{ 'cat':0, 'dog':1, 'fish':2 }`
- Encoded vectors generated for `cat`, `dog`

### Exact output from notebook
```
Vocabulary: {'cat': 0, 'dog': 1, 'fish': 2}
cat: [1. 0. 0.]
dog: [0. 1. 0.]
```

---

## 5.2 PART B: Manual Character-Level One-Hot Encoding

### Code idea
- Build character vocabulary (e.g., `['a','b','c','d']`)
- Create index dictionary
- Generate one-hot vector per character

### Notebook implementation summary
- Character mapping: `{ 'a':0, 'b':1, 'c':2, 'd':3 }`
- Tested encodings for `c` and `d`

### Exact output from notebook
```
0 a
1 b
2 c
3 d
{'a': 0, 'b': 1, 'c': 2, 'd': 3}
c: [0. 0. 1. 0.]
d: [0. 0. 0. 1.]
```

### Additional helper output (from first code cell)
```
[0. 1. 0. 0.]
```
(Represents one-hot encoding of character `b` in `[a,b,c,d]` vocabulary.)

---

## 5.3 PART C: Keras `one_hot()` - Hashing Trick + Padding

### Code idea
- Use Keras `one_hot(text, n)` where `n` is hash space size
- Words are mapped to integer hashes (not strict vocabulary indices)
- Use `pad_sequences` to align sequence lengths

### Notebook input
- `text1 = "cat dog fish dog"`
- `text2 = "lion elephant"`
- hash space size = 10

### Exact output from notebook
```
[[1, 4, 3, 4], [2, 4]]
[[1 4 3 4]
 [2 4 0 0]]
```

### Interpretation
- Repeated words map to repeated integers (e.g., `dog` mapped consistently inside same run).
- Sequence lengths differ and are padded using trailing zeros.
- Since hashing is used, collisions are possible when hash space is small.

---

## 6. TOKENIZER-BASED TEXT ENCODING (ADDITIONAL CELL)

### Purpose
To show practical vocabulary creation and binary matrix conversion with Keras `Tokenizer`.

### Exact output from notebook
```
Vocabulary (word → index):
{'ai': 1, 'i': 2, 'love': 3, 'is': 4, 'very': 5, 'powerful': 6}

Integer Sequences:
Text 1: [2, 3, 1]
Text 2: [1, 4, 5, 6]

Matrix Representation (texts_to_matrix):
[[0. 1. 1. 1. 0. 0. 0.]
 [0. 1. 0. 0. 1. 1. 1.]]

Matrix Shape: (2, 7)
```

### Interpretation
- `Tokenizer` generates deterministic word index mapping from corpus.
- `texts_to_sequences` converts sentence tokens into integer IDs.
- `texts_to_matrix(..., mode='binary')` creates binary presence vectors per text.

---

## 7. DELIVERABLES COVERAGE

### Deliverable 1: PART A Manual Word-Level One-Hot Encoding
✅ Completed and verified with vocabulary + encoded vectors.

### Deliverable 2: PART B Manual Character-Level One-Hot Encoding
✅ Completed and verified with character mapping + encoded vectors.

### Deliverable 3: PART C Keras `one_hot()` (Hashing Trick)
✅ Completed and verified with encoded integer sequences and padded output.

Collision concept explained: hash mapping can map different words to same index if hash space is limited.

---

## 8. COMPARATIVE DISCUSSION

| Method | Mapping Type | Vector/Output Type | Vocabulary Dependence | Collision Risk |
|---|---|---|---|---|
| Manual Word One-Hot | Explicit dictionary index | Binary vector | Yes | No |
| Manual Character One-Hot | Explicit dictionary index | Binary vector | Yes | No |
| Keras `one_hot()` | Hash-based index | Integer sequence | Not strict vocabulary index | Yes |
| Tokenizer + Matrix | Learned word index | Integer seq / binary matrix | Yes | No (indexing), N/A for matrix |

---

## 9. LEARNING OUTCOMES

1. Understood why text must be numerically represented for neural models.
2. Implemented one-hot encoding manually at word and character levels.
3. Understood Keras hash-based one-hot encoding and padding.
4. Compared explicit indexing vs hash-based encoding.
5. Practiced converting text into binary matrix features for downstream models.

---

## 10. CONCLUSION

The experiment was completed successfully. All required parts (A, B, C) were implemented in `exp06.ipynb` and validated with outputs. Manual one-hot encoding provides clear symbol isolation, while Keras hash-based one-hot offers compact and convenient encoding with potential collision trade-offs.

---

**Notebook Reference:** `lab06/exp06.ipynb`  
**Question Reference:** `lab06/question.md`  

**Verified by:** 23BQ1A4201  
**Date:** March 18, 2026  
**Signature:** _________________________
