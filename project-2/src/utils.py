import numpy as np

def to_char_list(tweet, vocabulary):
    """Convert tweet string into a character list for all characters in string that are in the 
    vocabulary chosen (including spaces).

    Arguments:
        tweet {String} -- Tweet
        vocabulary {list} -- list of accepted characters.

    Returns:
        list -- list of characters and spaces present in the tweet provided.
    """
    return [char for char in str(tweet) if char in vocabulary or char == ' ']


# TODO: Implement 2 space delimiter as per assignment.
def output_trace_file(table, v, n, d):
    """Write trace file.

    Arguments:
        table {dataframe} -- result of prediction on test set.
        V, n, d {int} -- Parameters of NBClassifier, for use in naming file.
    """
    with open(f"out/trace_{v}_{n}_{d}.txt", 'a') as f:
        f.write(table.to_string(header=False, index=False))
        f.close()

def output_eval_file(table, v, n, d, selector):
    """Write overall evaluation file.
    
    Arguments:
        table {dataframe} -- test df with results of classification task.
    """

    acc = round(table[table['result'] == 'correct'].shape[0]/table.shape[0], 3)

    precisions = {}
    recalls = {}
    f1s = {}
    wa_f1 = 0

    for l in selector.keys():
        tp = table[(table['lang'] == l) & (table['pred_lang'] == l)].shape[0]
        fp = table[(table['lang'] != l) & (table['pred_lang'] == l)].shape[0]
        fn = table[(table['lang'] == l) & (table['pred_lang'] != l)].shape[0]

        if (tp+fp) == 0 or (tp+fn) == 0:
            precisions[l] = 0
            recalls[l] = 0
        else:
            precisions[l] = tp/(tp+fp)
            recalls[l] = tp/(tp+fn)
        
        # TODO: fix this workaround for gl, since we have 1 datapoint and 0 true positives.
        if precisions[l]+recalls[l] == 0:
            f1s[l] = 0
        else:
            f1s[l] = (2*precisions[l]*recalls[l])/(precisions[l]+recalls[l])
        
        wa_f1 += table[table['lang'] == l].shape[0]*f1s[l]
        
    macro_f1 = np.average(list(f1s.values()))
    wa_f1 /= table.shape[0]

    with open(f"out/eval_{v}_{n}_{d}.txt", 'a') as f:
        f.write(str(acc))
        f.write('\n')

        for metric_list in [precisions, recalls, f1s]:
            for l in selector.keys():
                f.write(str(round(metric_list[l], 3)))
                f.write("  ")
            f.write("\n")
        
        f.write(str(round(macro_f1, 3)))
        f.write("  ")
        f.write(str(round(wa_f1, 3)))
        
        f.close()
