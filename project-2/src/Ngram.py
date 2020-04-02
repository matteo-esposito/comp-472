class Ngram2():
        """Class used for representing ngrams.
    """

    def __init__(self, language, count_table, probs_table, language_prob=0):
        """Parametrized constructor for Ngrams.
        
        Arguments:
            language {string} -- Choice from ['eu', 'ca', 'gl', 'es', 'en', 'pt']
            count_table {list} -- list of dicts to store all ngram counts.
            probs_table {list} -- list of dicts to store all smoothed ngram probabilities.
        
        Keyword Arguments:
            language_prob {int} -- Language probability (default: {0})
        """
        self.language = language
        self.count_table = count_table
        self.probs_table = probs_table
        self.language_prob = language_prob
