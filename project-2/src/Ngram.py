class Ngram():
    """Class used for representing ngrams.
    
    Attributes:
        count_table (TYPE): Description
        language (TYPE): Description
        language_prob (TYPE): Description
        n (TYPE): Description
        probs_table (TYPE): Description
    """

    def __init__(self, language, count_table, probs_table, n, language_prob=0):
        """Parametrized constructor for Ngrams.
        
        Arguments:
            language (TYPE): Description
            count_table (TYPE): Description
            probs_table (TYPE): Description
            n (TYPE): Description
            language_prob (int, optional): Description
            language {string} -- Choice from ['eu', 'ca', 'gl', 'es', 'en', 'pt']
            count_table {list} -- list of dicts to store all ngram counts.
            probs_table {list} -- list of dicts to store all smoothed ngram probabilities.
            n {int} -- dimension of n-gram (helps with updating the dictionaries)
        
        Keyword Arguments:
            language_prob {int} -- Language probability (default: {0})
        """
        self.language = language
        self.count_table = count_table
        self.probs_table = probs_table
        self.language_prob = language_prob
        self.n = n

    def smoothe(self, delta):
        """Summary
        
        Args:
            delta (TYPE): Description
        """
        # Method that smoothes the count table
        if self.n == 1:
            for key1 in self.count_table.keys():
                self.count_table[key1] += delta
        elif self.n == 2:
            for key1 in self.count_table.keys():
                for key2 in self.count_table.keys():
                    self.count_table[key1][key2] += delta
        elif self.n == 3:
            for key1 in self.count_table.keys():
                for key2 in self.count_table.keys():
                    for key3 in self.count_table.keys():
                        self.count_table[key1][key2][key3] += delta

    def update_probs(self):
        """Calculates probabilities from count_table
        """
        
        if self.n == 1:
            tot = sum(self.count_table.values())
            for key1 in self.count_table.keys():
                self.probs_table[key1] = self.count_table[key1] / tot
        elif self.n == 2:
            for key1 in self.count_table.keys():
                tot = sum(self.count_table[key1].values())
                for key2 in self.count_table.keys():
                    self.probs_table[key1][key2] = self.count_table[key1][key2] / tot
        elif self.n == 3:
            for key1 in self.count_table.keys():
                for key2 in self.count_table.keys():
                    tot = sum(self.count_table[key1][key2].values())
                    for key3 in self.count_table.keys():
                        self.probs_table[key1][key2][key3] = self.count_table[key1][key2][key3] / tot

    def update_language_prob(self, train_df):
        """Updates the language probability for this ngram
        
        Args:
            train_df (dictionary): Training data
        """

        language_count = 0
        for tweet in train_df:
            if tweet['lang'] == self.language:
                language_count += 1
        self.language_prob = language_count / len(train_df)
