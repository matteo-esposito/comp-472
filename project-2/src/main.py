from NBClassifier import NBClassifier
import utils, os, shutil


if __name__ == "__main__":
    # Initialize classifier
    nbc = NBClassifier(V=1, n=2, delta=0.5, train_file="input/training-tweets.txt",
                       test_file="input/test-tweets-given.txt")

    # Initialize ngrams based on NBC parameters.
    eu_ngram, ca_ngram, gl_ngram, es_ngram, en_ngram, pt_ngram = nbc.init_ngrams()
    selector = {
        "eu": eu_ngram,
        "ca": ca_ngram,
        "gl": gl_ngram,
        "es": es_ngram,
        "en": en_ngram,
        "pt": pt_ngram
    }

    # Import, train, test.
    train_df, test_df = nbc.import_data()
    nbc.train(train_df, selector)
    out_df = nbc.predict(test_df, selector)

    # Output results
    desired_folder_path = os.path.join(os.getcwd(), "out/")
    if os.path.isdir(desired_folder_path):
        shutil.rmtree(desired_folder_path, ignore_errors=True)
    os.mkdir(desired_folder_path)

    utils.output_trace_file(out_df, nbc.V, nbc.n, nbc.delta)
    utils.output_eval_file(out_df, nbc.V, nbc.n, nbc.delta, selector)
