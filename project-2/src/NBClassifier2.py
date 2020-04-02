from Ngram import Ngram
from decimal import Decimal
import utils
import math
import string


class NBClassifier2():

    global vocab
    vocab = {
        0: list(string.ascii_lowercase),
        1: list(string.ascii_lowercase) + list(string.ascii_uppercase),
        2: [chr(codepoint) for codepoint in range(17 * 2**16) if chr(codepoint).isalpha()]
    }
    languages = ['eu', 'ca', 'gl', 'es', 'en', 'pt']

    def __init__(self, V, n, delta, train_file, test_file):
        """Parametrized constructor for Naive Bayes Classifier.

        Arguments:
            V {int} -- Vocabulary choice (1=[a,z], 2=[a-zA-Z], 3=isalpha())
            n {int} -- ngram selection (1=uni, 2=bi, 3=tri)
            delta {int} -- smoothing factor
            train_file {string} -- path to train file
            test_file {string} -- path to test file
        """
        self.V = V
        self.n = n
        self.delta = delta
        self.train_file = train_file
        self.test_file = test_file

    def import_data(self):
        train = []
        test = []

        with open(self.train_file, 'r', encoding='utf-8') as f:
            for line in f:
                row = line.split('\t')
                if len(row) != 4:
                    break
                train.append({'id': row[0], 'user': row[1], 'lang': row[2], 'tweet': row[3]})

        with open(self.test_file, 'r', encoding='utf-8') as f:
            for line in f:
                row = line.split('\t')
                if len(row) != 4:
                    break
                test.append({'id': row[0], 'user': row[1], 'lang': row[2], 'tweet': row[3]})

        return train, test

    def init_ngrams(self):
        """Initialize NGram objects
        """
        # Unigram case
        if self.n == 1:

            unigram_table = {word: 0 for word in vocab[self.V]}

            return (Ngram(language=lan,
                          count_table=unigram_table,
                          probs_table=unigram_table) for lan in languages)

        # Bigram case
        elif self.n == 2:

            bigram_table = {word1:
                            {word2: 0 for word2 in vocab[self.V]}
                            for word1 in vocab[self.V]}

            return (Ngram(language=lan,
                          count_table=bigram_table,
                          probs_table=bigram_table) for lan in languages)
        # Trigram case
        elif self.n == 3:

            trigram_table = {word1:
                             {word2:
                              {word3: 0 for word3 in vocab[self.V]}
                              for word2 in vocab[self.V]}
                             for word1 in vocab[self.V]}

            return (Ngram(language=lan,
                          count_table=trigram_table,
                          probs_table=trigram_table) for lan in languages)

    def train(self, train_df, selector):
        """Train the Naive Bayes Classifier. Modify all gram objects inplace.

        Arguments:
            train_df {dataframe} -- Training set of tweets
            selector {dict} -- Dictionary of languages and grams (used to facilitate loops).
        """
        # Populate count table
        for language in languages:

            # Choose appropriate table given language of tweet.
            table = selector[language].count_table

            # Modify entries in table selected above.
            for row in train_df:
                if row['lang'] != language:
                    continue
                t = row['tweet']
                char_tweet = utils.to_char_list(t, vocab[self.V])

        return
