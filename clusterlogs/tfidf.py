import math
import numpy as np


class TermsAnalysis:

    def __init__(self, tokenized):

        self.tokenized = tokenized


    def process(self):

        f_matrix = self.create_frequency_matrix(self.tokenized)
        tf_matrix = self.create_tf_matrix(f_matrix)
        dpw = self.create_documents_per_words(f_matrix)
        idf_matrix = self.create_idf_matrix(f_matrix, dpw, len(self.tokenized))
        tf_idf = self.create_tf_idf_matrix(tf_matrix, idf_matrix)

        stats = []
        for row in tf_idf:
            all_vals = [v for k, v in row.items()]
            stats.append(np.max(all_vals) - np.std(all_vals))

        return self.remove_unnecessary(tf_idf, stats)



    def create_frequency_matrix(self, tokenized):
        frequency_matrix = []

        for tokens in tokenized:
            freq_table = {}
            for token in tokens:
                if token in freq_table:
                    freq_table[token] += 1
                else:
                    freq_table[token] = 1

            frequency_matrix.append(freq_table)

        return frequency_matrix


    def create_tf_matrix(self, freq_matrix):
        tf_matrix = []

        for f_table in freq_matrix:
            tf_table = {}

            count_words_in_sentence = len(f_table)
            for word, count in f_table.items():
                tf_table[word] = count / count_words_in_sentence

            tf_matrix.append(tf_table)

        return tf_matrix


    def create_documents_per_words(self, freq_matrix):
        word_per_doc_table = {}

        for f_table in freq_matrix:
            for word, count in f_table.items():
                if word in word_per_doc_table:
                    word_per_doc_table[word] += 1
                else:
                    word_per_doc_table[word] = 1

        return word_per_doc_table


    def create_idf_matrix(self, freq_matrix, count_doc_per_words, total_documents):
        idf_matrix = []

        for f_table in freq_matrix:
            idf_table = {}

            for word in f_table.keys():
                idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

            idf_matrix.append(idf_table)

        return idf_matrix


    def create_tf_idf_matrix(self, tf_matrix, idf_matrix):
        tf_idf_matrix = []

        for f_table1, f_table2 in zip(tf_matrix, idf_matrix):

            tf_idf_table = {}

            for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                        f_table2.items()):  # here, keys are the same in both the table
                tf_idf_table[word1] = float(value1 * value2)

            tf_idf_matrix.append(tf_idf_table)

        return tf_idf_matrix


    def remove_unnecessary(self, tf_idf, stats):
        new_arr = []
        for i, row in enumerate(tf_idf):
            x = []
            for k, v in row.items():
                if v >= stats[i]:
                    x.append('｟*｠')
                else:
                    x.append(k)
            new_arr.append(x)
        return new_arr