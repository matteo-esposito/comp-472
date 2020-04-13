from NBClassifier import NBClassifier
from BYOM import BYOM
import utils
import os
import shutil

if __name__ == '__main__':
<<<<<<< HEAD
        # Initialize classifier
    nbc = NBClassifier(V=2, n=2, delta=0.5, train_file="input/training-tweets.txt",
                       test_file="input/test5.txt")
=======
    a=1
    b=2
    c=0.5
>>>>>>> 1dbf253c3508fc9f509920f63141496380ff0d05

    # Initialize classifier
    # nbc = NBClassifier(V=a, n=b, delta=c, train_file="input/training-tweets.txt",
    #                    test_file="input/test5.txt")

    # # Import, train, test.
    # train_df, test_df = nbc.import_data()
    # nbc.train(train_df)
    # out_df = nbc.predict(test_df)

    # # Remove out/ folder if it exists in preparation for a new run.
    # desired_folder_path = os.path.join(os.getcwd(), "out/")
    # if os.path.isdir(desired_folder_path):
    #     shutil.rmtree(desired_folder_path, ignore_errors=True)
    # os.mkdir(desired_folder_path)

    # # Output trace and evaluation file.
    # utils.output_trace_file(out_df, nbc.V, nbc.n,
    #                         nbc.delta, desired_folder_path)
    # utils.output_eval_file(out_df, nbc.V, nbc.n, nbc.delta,
    #                         ['eu', 'ca', 'gl', 'es', 'en', 'pt'], desired_folder_path)

    # BYOM Classifier

    nbc_BYOM = BYOM(V=a, delta=c, train_file="input/training-tweets.txt",
                    test_file="input/test5.txt", w1=0.6, w2=0.2)
    # Import, train, test.
    train_df, test_df = nbc_BYOM.m3.import_data()
    nbc_BYOM.train_all(train_df)
    nbc_BYOM.lin_interp_weighted_prob()
    out_df = nbc_BYOM.predict_new(test_df)

    # Remove out/ folder if it exists in preparation for a new run.
    desired_folder_path = os.path.join(os.getcwd(), "out_BYOM/")
    if os.path.isdir(desired_folder_path):
        shutil.rmtree(desired_folder_path, ignore_errors=True)
    os.mkdir(desired_folder_path)

    utils.output_trace_file(out_df, nbc_BYOM.m3.V, "BYOM",
                            nbc_BYOM.m3.delta, desired_folder_path)
    utils.output_eval_file(out_df, nbc_BYOM.m3.V, "BYOM", nbc_BYOM.m3.delta,
                           ['eu', 'ca', 'gl', 'es', 'en', 'pt'], desired_folder_path)
