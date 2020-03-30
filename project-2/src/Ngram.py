class Ngram():
    """Class used for bigram model.
    """

    def __init__(self, language, count_table, probs_table, language_prob=0):
        self.language = language
        self.count_table = count_table
        self.probs_table = probs_table
        self.language_prob = language_prob
