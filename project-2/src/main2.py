from NBClassifier2 import NBClassifier2
import utils2
import os
import shutil

if __name__ == '__main__':
        # Initialize classifier
    nbc = NBClassifier2(V=1, n=3, delta=0.5, train_file="input/training-tweets.txt",
                        test_file="input/test-tweets-given.txt")

    # Import, train, test.
    train_df, test_df = nbc.import_data()
    nbc.train(train_df)
    out_df = nbc.predict(test_df)

    # Output results
    desired_folder_path = os.path.join(os.getcwd(), "out_builtin/")
    if os.path.isdir(desired_folder_path):
        shutil.rmtree(desired_folder_path, ignore_errors=True)
    os.mkdir(desired_folder_path)

    utils2.output_trace_file(out_df, nbc.V, nbc.n, nbc.delta, 'out_builtin')
    utils2.output_eval_file(out_df, nbc.V, nbc.n, nbc.delta, ['eu', 'ca', 'gl', 'es', 'en', 'pt'], 'out_builtin')
