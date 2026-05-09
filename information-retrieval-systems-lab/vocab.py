# vocab_builder.py
from collections import Counter

class VocabularyBuilder:
    def __init__(self, documents):
        """
        documents: list of preprocessed text strings (each doc already tokenized/cleaned)
        """
        self.documents = documents
        self.vocabulary = []
        self.term_frequencies = {}
        self.document_lists = {}
    
    def build(self):
        """
        Build vocabulary, term frequencies, and document lists.
        """
        for doc_index, document in enumerate(self.documents):
            tokens = document.split()

            # build vocabulary + document lists
            for token in tokens:
                if token not in self.vocabulary:
                    self.vocabulary.append(token)

                if token not in self.document_lists:
                    self.document_lists[token] = {doc_index}
                else:
                    self.document_lists[token].add(doc_index)

            # build term frequencies for this doc
            doc_term_frequencies = Counter(tokens)
            self.term_frequencies[doc_index] = doc_term_frequencies
    
    def summary(self, n_vocab_sample=20, n_doclist_sample=5):
        """
        Print a summary of built structures.
        """
        print(f"Size of vocabulary: {len(self.vocabulary)}")
        print(f"\nSample of vocabulary (first {n_vocab_sample} words): {self.vocabulary[:n_vocab_sample]}")
        
        print(f"\nNumber of documents with term frequencies: {len(self.term_frequencies)}")

        if 0 in self.term_frequencies:
            print(f"\nTerm frequencies for document 0 (first 10 terms):")
            sample_doc_tf = dict(list(self.term_frequencies[0].items())[:10])
            for term, freq in sample_doc_tf.items():
                print(f"  '{term}': {freq}")
        else:
            print("\nTerm frequencies for document 0 not available.")

        print(f"\nNumber of unique words with document lists: {len(self.document_lists)}")

        print(f"\nDocument lists for sample words (first {n_doclist_sample} words):")
        for i, word in enumerate(self.vocabulary[:n_doclist_sample]):
            if word in self.document_lists:
                docs = list(self.document_lists[word])[:5]  # show first 5 doc indices
                print(f"  '{word}': {docs}...")
            else:
                print(f"  '{word}': Document list not available.")

    def get_vocabulary(self):
        return self.vocabulary

    def get_term_frequencies(self):
        return self.term_frequencies

    def get_document_lists(self):
        return self.document_lists
