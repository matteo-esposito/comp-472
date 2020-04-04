from NBClassifier import NBClassifier
import utils
import os
import shutil

if __name__ == '__main__':
    # Initialize classifier
    nbc = NBClassifier(V=2, n=2, delta=0.3, train_file="input/training-tweets.txt",
                       test_file="input/test-tweets-given.txt")

    # Import, train, test.
    train_df, test_df = nbc.import_data()
    nbc.train(train_df)
    out_df = nbc.predict(test_df)

    # Remove out/ folder if it exists in preparation for a new run.
    desired_folder_path = os.path.join(os.getcwd(), "out/")
    if os.path.isdir(desired_folder_path):
        shutil.rmtree(desired_folder_path, ignore_errors=True)
    os.mkdir(desired_folder_path)

    # Output trace and evaluation file.
    utils.output_trace_file(out_df, nbc.V, nbc.n,
                            nbc.delta, desired_folder_path)
    utils.output_eval_file(out_df, nbc.V, nbc.n, nbc.delta, 
                            ['eu', 'ca', 'gl', 'es', 'en', 'pt'], desired_folder_path)
