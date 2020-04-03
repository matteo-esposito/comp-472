from Ngram import Ngram
from decimal import Decimal
import utils
import math
import string
from copy import deepcopy


class NBClassifier():

    global vocabulary
    global VALID_N
    global languages
    vocabulary = {
        0: list(string.ascii_lowercase),
        1: list(string.ascii_lowercase) + list(string.ascii_uppercase),
        2: []  # Will be populated by NBClassifier.__get_vocab_2()
    }
    VALID_N = {1, 2, 3}
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
        if n not in VALID_N:
            raise ValueError(f'value of n must be in {VALID_N}')

        self.V = V
        self.n = n
        self.delta = delta
        self.train_file = train_file
        self.test_file = test_file
        self.vocab = vocabulary[self.V]
        if self.V == 2:
            self.vocab = self.__get_vocab_2()
        self.selector = self.init_ngrams()

    def __get_vocab_2(self):
        """Returns the list of all unique isalpha() characters from train file as vocab

        Returns:
            list: list of characters representing vocabulary 2 as per the assignment guidelines.
        """
        with open(self.train_file, 'r', encoding='utf-8') as f:
            unique_chars = set(f.read())
            f.close()
        return list(c for c in unique_chars if c.isalpha())

    def import_data(self):
        """Imports data from train file

        Returns:
            dataframe: train, test lists of dicts
        """
        train = []
        test = []

        with open(self.train_file, 'r', encoding='utf-8') as f:
            for line in f:
                row = line.split('\t')
                if len(row) != 4:
                    break
                train.append(
                    {'id': row[0], 'user': row[1], 'lang': row[2], 'tweet': row[3]})

        with open(self.test_file, 'r', encoding='utf-8') as f:
            for line in f:
                row = line.split('\t')
                if len(row) != 4:
                    break
                test.append({'id': row[0], 'user': row[1],
                             'lang': row[2], 'tweet': row[3]})

        return train, test

    def init_ngrams(self):
        """Initialize NGram objects
        
        Returns:
            dict: language and Ngram object key value pairs.
        """
        # Unigram case
        if self.n == 1:

            unigram_table = {word: 0 for word in self.vocab}

            return {lan: Ngram(language=lan,
                               count_table=deepcopy(unigram_table),
                               probs_table=deepcopy(unigram_table),
                               n=self.n) for lan in languages}

        # Bigram case
        elif self.n == 2:

            bigram_table = {word1:
                            {word2: 0 for word2 in self.vocab}
                            for word1 in self.vocab}

            return {lan: Ngram(language=lan,
                               count_table=deepcopy(bigram_table),
                               probs_table=deepcopy(bigram_table),
                               n=self.n) for lan in languages}
        # Trigram case
        elif self.n == 3:

            trigram_table = {word1:
                             {word2:
                              {word3: 0 for word3 in self.vocab}
                              for word2 in self.vocab}
                             for word1 in self.vocab}

            return {lan: Ngram(language=lan,
                               count_table=deepcopy(trigram_table),
                               probs_table=deepcopy(trigram_table),
                               n=self.n) for lan in languages}

    def train(self, train_df):
        """Train the Naive Bayes Classifier. Modify all gram objects inplace.

        Arguments:
            train_df {dataframe} -- Training set of tweets
        """
        # Populate count table
        for language in languages:

            # Choose appropriate table given language of tweet.
            table = self.selector[language].count_table

            # Modify entries in table selected above.
            for row in train_df:
                if row['lang'] != language:
                    continue
                t = row['tweet']

                char_tweet = utils.to_char_list(t, self.vocab)

                if self.n == 1:
                    for i in range(len(char_tweet)):
                        c1 = char_tweet[i]
                        if c1 in self.vocab:
                            table[c1] += 1
                elif self.n == 2:
                    for i in range(len(char_tweet) - 1):
                        c1 = char_tweet[i]
                        c2 = char_tweet[i + 1]
                        if c1 in self.vocab and c2 in self.vocab:
                            table[c1][c2] += 1
                elif self.n == 3:
                    for i in range(len(char_tweet) - 2):
                        c1 = char_tweet[i]
                        c2 = char_tweet[i + 1]
                        c3 = char_tweet[i + 2]
                        if c1 in self.vocab and c2 in self.vocab and c3 in self.vocab:
                            table[c1][c2][c3] += 1

        # Add smoothing, generate probability table and get language probabilities.
        for l in self.selector.keys():
            ngram = self.selector[l]
            ngram.smoothe(self.delta)
            ngram.update_probs()
            ngram.update_language_prob(train_df)
        return

    def predict(self, test_df):
        """Test the trained classifier on new data. (log base 10 used for scoring function). Then place predictions in the test dataframe for output.

        Arguments:
            test_df {dictionary} -- Test tweets with predictions and correct/incorrect markers.
        """
        # Generate probability for test set for all 6 languages
        test_langs = []
        test_probs = []

        # For every tweet we generate a prob for each language and store the max.
        for t in test_df:
            if self.V in [0, 1]:
                test_tweet = utils.to_char_list(t['tweet'], self.vocab)
            else:
                test_tweet = utils.to_char_list(
                    t['tweet'], self.vocab, use_alpha=True)
            lang_probs = {}

            # Get probs
            for language in languages:
                p = math.log10(self.selector[language].language_prob)
                table = self.selector[language].probs_table

                if self.n == 1:
                    for i in range(len(test_tweet)):
                        c1 = test_tweet[i]
                        if c1 in self.vocab:
                            p += math.log10(table[c1])
                        elif self.V == 2:
                            p += math.log10(self.delta)
                elif self.n == 2:
                    for i in range(len(test_tweet) - 1):
                        c1 = test_tweet[i]
                        c2 = test_tweet[i + 1]
                        if c1 in self.vocab and c2 in self.vocab:
                            p += math.log10(table[c1][c2])
                        elif self.V == 2:
                            p += math.log10(self.delta)
                elif self.n == 3:
                    for i in range(len(test_tweet) - 2):
                        c1 = test_tweet[i]
                        c2 = test_tweet[i + 1]
                        c3 = test_tweet[i + 2]
                        if c1 in self.vocab and c2 in self.vocab and c3 in self.vocab:
                            p += math.log10(table[c1][c2][c3])
                        elif self.V == 2:
                            p += math.log10(self.delta)

                lang_probs[language] = p

            # Add predictions
            t['pred_lang'] = max(lang_probs, key=lang_probs.get)
            t['pred_prob'] = '%.2E' % Decimal(max(lang_probs.values()))
            t['result'] = 'correct' if t['pred_lang'] == t['lang'] else 'wrong'

        return test_df
