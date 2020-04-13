
from NBClassifier import NBClassifier

class BYOM():
    """New model built using linear interpolation of probabilities
    from each individual model (Unigram, Bigram, Trigram)
    """
    global languages
    languages = ['eu', 'ca', 'gl', 'es', 'en', 'pt']

    def __init__(self, V, delta, train_file, test_file, w1, w2):
        """Parameterized constructor for Build Your Own Model

        Arguments:
            V {int} -- Vocabulary choice (1=[a,z], 2=[a-zA-Z], 3=isalpha())
            delta {int} -- smoothing factor
            train_file {string} -- path to train file
            test_file {string} -- path to test file
            w1 {float} -- Arbitrary weight for Trigram
            w2 {float} -- Arbitrary weight for Bigram (w1 + w2 < 1)
        """

        self.m1 = NBClassifier(V=V, n=1, delta=delta,train_file=train_file, test_file=test_file)
        self.m2 = NBClassifier(V=V, n=2, delta=delta,train_file=train_file, test_file=test_file)
        self.m3 = NBClassifier(V=V, n=3, delta=delta,train_file=train_file, test_file=test_file)
        self.w1 = w1
        self.w2 = w2
        self.w3 = 1 - (w1 + w2)

    def train_all(self,train_df):
        """Trains all individual models with training data set
        """

        self.m1.train(train_df)
        self.m2.train(train_df)
        self.m3.train(train_df)

    def lin_interp_weighted_prob(self):
        """Creates new linearly interpolated probabilities for one model
        """

        for language in languages:
            table1 = self.m1.selector[language].probs_table
            table2 = self.m2.selector[language].probs_table
            table3 = self.m3.selector[language].probs_table

            for key1 in table3.keys():
                for key2 in table3.keys():
                    for key3 in table3.keys():
                        table3[key1][key2][key3] = self.w1*table3[key1][key2][key3] + self.w2*table2[key2][key3] +self.w3*table1[key3]

    def predict_new(self, test_df):
        """Tests test dataset with new probabilities
        """
        return self.m3.predict(test_df)







