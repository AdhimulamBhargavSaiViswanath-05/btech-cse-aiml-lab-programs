AIM:
To implement one-hot encoding of words and characters using Python and Keras
Introduction:
The Representation Problem
text
A neural network is a mathematical function that operates on real-valued vectors. Language
is a sequence of discrete symbols (characters, words, tokens). To apply any mathematical
How do we convert a symbol into a number?
model to language, we must first answer a fundamental question: This is the representation problem. Our answer determines what relationships the model can and cannot learn. One-hot encoding is the most direct, assumption-free answer: assign each symbol a unique integer index and represent it as a vector with exactly one '1' at that index position and zeros everywhere else.
Core principle of one-hot encoding
Representation is not neutral. Every choice of representation encodes assumptions about the structure of the data. One-hot encoding makes exactly one assumption: all symbols are distinct. It makes no assumption about similarity, frequency, or relationships. This is both its strength (no wrong assumptions imposed) and its weakness (no useful structure encoded).
Formal definition
Let V (W1 W2...., Wn be a vocabulary of N unique words. Assign each word w₁ an integer index i € (1,2,..., N). The one-hot encoding of word w₁ is:
Onchot (w)e, ERN
where e, is the i-th standard basis vector: e[j]=1 if j = i e[j]=0 ifj≠i
Example: V = {cat, dog, fish, bird), N = 4
onehot (cat) [1,0,0,0] e₁ onehot(dog) = [0,1,0,0] = €2 onehot(fish) = [0,0,1,0]= ез onehot(bird) = [0,0,0,1]
Each word occupies its own dimension of the vector space.
Each word is a point on a different axis of an N-dimensional hypercube.
Deliverables:
1. PART A: Implement manual Word-Level One-Hot Encoding
2. PART B: Implement manual Character-Level One-Hot Encoding (Character vocabulary)
3. PART C: Implement Keras one_hot() - The Hashing Trick (Fixed-size encoding with collision analysis)