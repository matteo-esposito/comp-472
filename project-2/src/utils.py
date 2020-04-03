import os


def to_char_list(tweet, vocabulary, use_alpha=False):
    """Convert tweet string into a character list for all characters in string that are in the 
    vocabulary chosen (including spaces).

    Arguments:
        tweet {String} -- Tweet
        vocabulary {list} -- list of accepted characters.

    Returns:
        list -- list of characters and spaces present in the tweet provided.
    """
    if not use_alpha:
        return [char for char in str(tweet) if char in vocabulary or char == ' ']
    else:
        return [char for char in str(tweet) if char.isalpha() or char == ' ']


def output_trace_file(table, v, n, d, out_path):
    """Write trace file.

    Arguments:
        table {dictionary} -- result of prediction on test set.
        V, n, d {int} -- Parameters of NBClassifier, for use in naming file.
    """
    with open(os.path.join(out_path, f"trace_{v}_{n}_{d}.txt"), 'w', encoding="utf-8") as f:
        for r in table:
            f.write(f'{r["id"]}  {r["lang"]}  {r["pred_prob"]}  {r["pred_lang"]}  {r["result"]}\n')
        f.close()


def output_eval_file(table, v, n, d, languages, out_path):
    """Write overall evaluation file.

    Arguments:
        table {dictionary} -- result of prediction on test set.
    """

    # Calculate accuracy
    correct = 0
    for r in table:
        if r['result'] == 'correct':
            correct += 1
    acc = correct / len(table)

    precisions = {}
    recalls = {}
    f1s = {}
    l_counts = {}

    for l in languages:
        count = 0
        tp = 0
        fp = 0
        fn = 0

        for r in table:
            if r['lang'] == l and r['pred_lang'] == l:
                tp += 1
                count += 1
            elif r['lang'] != l and r['pred_lang'] == l:
                fp += 1
            elif r['lang'] == l and r['pred_lang'] != l:
                fn += 1
                count += 1

        if (tp + fp) == 0 or (tp + fn) == 0:
            precisions[l] = 0
            recalls[l] = 0
        else:
            precisions[l] = tp / (tp + fp)
            recalls[l] = tp / (tp + fn)

        # Workaround for cases where there are 0 true positives and therefore 0 precision and recall and undefined f1.
        if precisions[l] + recalls[l] == 0:
            f1s[l] = 0
        else:
            f1s[l] = (2 * precisions[l] * recalls[l]) / (precisions[l] + recalls[l])

        l_counts[l] = count

    macro_f1 = sum(f1s.values()) / len(f1s)
    wa_f1 = sum(l_counts[l] * f1s[l] for l in languages) / len(table)

    with open(os.path.join(out_path, f"eval_{v}_{n}_{d}.txt"), 'a') as f:
        f.write(str(round(acc, 3)))
        f.write('\n')

        for metric_list in [precisions, recalls, f1s]:
            for l in languages:
                f.write(str(round(metric_list[l], 3)))
                f.write("  ")
            f.write("\n")

        f.write(str(round(macro_f1, 3)))
        f.write("  ")
        f.write(str(round(wa_f1, 3)))

        f.close()
