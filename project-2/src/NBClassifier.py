from Ngram import Ngram
from decimal import Decimal
import utils
import math
import numpy as np
import pandas as pd
import string


class NBClassifier():
    """Class used for Naive Bayes Classifier.
    """
    global V
    global vocab

    # TODO: Improve setup - Choices of vocabularies to be used in the model calls.

    vocab = {
        0: list(string.ascii_lowercase),
        1: list(string.ascii_lowercase) + list(string.ascii_uppercase),
        2: []  # TODO: Add isalpha() dictionary.
    }

    def __init__(self, V, n, delta, train_file, test_file):
        self.V = V
        self.n = n
        self.delta = delta
        self.train_file = train_file
        self.test_file = test_file

    def import_data(self):
        train = pd.read_csv(self.train_file, sep='\t', names=["id", "user", "lang", "tweet"])
        test = pd.read_csv(self.test_file, sep='\t', names=["id", "user", "lang", "tweet"])
        return train, test

    # TODO: Add functionality for unigrams and trigrams
    def init_ngrams(self):
        """Initialize NGram objects
        """
        if self.n == 2:
            eu_bigram = Ngram(language="eu",
                              count_table=pd.DataFrame(data=0, index=vocab[self.V], columns=vocab[self.V]),
                              probs_table=pd.DataFrame(data=0, index=vocab[self.V], columns=vocab[self.V]))
            ca_bigram = Ngram(language="ca",
                              count_table=pd.DataFrame(data=0, index=vocab[self.V], columns=vocab[self.V]),
                              probs_table=pd.DataFrame(data=0, index=vocab[self.V], columns=vocab[self.V]))
            gl_bigram = Ngram(language="gl",
                              count_table=pd.DataFrame(data=0, index=vocab[self.V], columns=vocab[self.V]),
                              probs_table=pd.DataFrame(data=0, index=vocab[self.V], columns=vocab[self.V]))
            es_bigram = Ngram(language="es",
                              count_table=pd.DataFrame(data=0, index=vocab[self.V], columns=vocab[self.V]),
                              probs_table=pd.DataFrame(data=0, index=vocab[self.V], columns=vocab[self.V]))
            en_bigram = Ngram(language="en",
                              count_table=pd.DataFrame(data=0, index=vocab[self.V], columns=vocab[self.V]),
                              probs_table=pd.DataFrame(data=0, index=vocab[self.V], columns=vocab[self.V]))
            pt_bigram = Ngram(language="pt",
                              count_table=pd.DataFrame(data=0, index=vocab[self.V], columns=vocab[self.V]),
                              probs_table=pd.DataFrame(data=0, index=vocab[self.V], columns=vocab[self.V]))
        return eu_bigram, ca_bigram, gl_bigram, es_bigram, en_bigram, pt_bigram

    def train(self, train_df, selector):
        """Train the Naive Bayes Classifier. Modify all gram objects inplace.

        Arguments:
            train_df {dataframe} -- Training set of tweets
            selector {dict} -- Dictionary of languages and grams (used to facilitate loops).
        """
        ### Populate count table
        for language in set(train_df['lang']):

            # Choose appropriate table given language of tweet.
            table = selector[language].count_table

            # Modify entries in table selected above.
            for t in train_df[train_df['lang'] == language]['tweet']:
                char_tweet = utils.to_char_list(t, vocab[self.V])
                for i in range(len(char_tweet) - 1):
                    c1 = char_tweet[i]
                    c2 = char_tweet[i + 1]
                    if c1 in table.columns and c2 in table.columns:
                        table.at[c1, c2] += 1

        ### Add smoothing, generate probability table and get language probabilities.
        for l, bigram in selector.items():
            bigram.count_table += 0.5
            bigram.probs_table = bigram.count_table.div(bigram.count_table.sum(axis=1), axis=0)
            bigram.language_prob = train_df[train_df['lang'] == l].shape[0] / train_df.shape[0]

        return

    def predict(self, test_df, selector):
        """Test the trained classifier on new data. (log base 10 used for scoring function). Then place predictions in the test dataframe for output.

        Arguments:
            test_df {dataframe} -- Test tweets
            selector {dict} -- Dictionary of languages and grams (used to facilitate loops).
        """
        # Generate probability for test set for all 6 languages
        test_langs = []
        test_probs = []

        # For every tweet we generate a prob for each language and store the max.
        for t in test_df['tweet']:
            test_tweet = utils.to_char_list(t, vocab[self.V])
            lang_probs = {}

            # Get probs
            for language in set(test_df['lang']):
                p = math.log10(selector[language].language_prob)
                table = selector[language].probs_table
                for i in range(len(test_tweet) - 1):
                    c1 = test_tweet[i]
                    c2 = test_tweet[i + 1]
                    if c1 in table.columns and c2 in table.columns:
                        p += math.log10(table.at[c1, c2])
                lang_probs[language] = p

            # Populate prediction lists
            test_langs.append(max(lang_probs, key=lang_probs.get))
            test_probs.append('%.2E' % Decimal(max(lang_probs.values())))

        test_df['pred_lang'] = test_langs
        test_df['pred_prob'] = test_probs
        test_df['result'] = np.where(test_df['pred_lang'] == test_df['lang'], 'correct', 'wrong')

        return test_df
