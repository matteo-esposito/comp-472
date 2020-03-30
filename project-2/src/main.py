from NBClassifier import NBClassifier
import utils


if __name__ == "__main__":
    # Initialize classifier
    nbc = NBClassifier(V=0, n=2, delta=0.5, train_file="input/training-tweets.txt",
                       test_file="input/test-tweets-given.txt")

    # Initialize grams based on NBC parameters.
    eu_gram, ca_gram, gl_gram, es_gram, en_gram, pt_gram = nbc.init_ngrams()
    selector = {
        "eu": eu_gram,
        "ca": ca_gram,
        "gl": gl_gram,
        "es": es_gram,
        "en": en_gram,
        "pt": pt_gram
    }

    # Import, train, test.
    train_df, test_df = nbc.import_data()
    nbc.train(train_df, selector)
    out_df = nbc.predict(test_df, selector)

    # Output results
    utils.output_trace_file(out_df, nbc.V, nbc.n, nbc.delta)
