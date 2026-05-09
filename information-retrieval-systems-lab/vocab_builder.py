# vocab_builder.py
from collections import Counter

class VocabularyBuilder:
    def __init__(self, documents):
        self.documents = documents
        self.vocabulary = []
        self.term_frequencies = {}
        self.document_lists = {}

    def build(self):
        for doc_index, document in enumerate(self.documents):
            tokens = document.split()
            # Build vocabulary + document lists
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary.append(token)
                if token not in self.document_lists:
                    self.document_lists[token] = {doc_index}
                else:
                    self.document_lists[token].add(doc_index)

            # Term frequencies
            self.term_frequencies[doc_index] = Counter(tokens)

    def get_vocabulary(self):
        return self.vocabulary

    def get_term_frequencies(self):
        return self.term_frequencies
