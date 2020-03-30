def to_char_list(tweet, vocabulary):
    """Convert tweet string into a character list for all characters in string that are in the vocabulary chosen (including spaces).
    
    Arguments:
        tweet {String} -- Tweet
        vocabulary {list} -- list of accepted characters.
    
    Returns:
        list -- list of characters and spaces present in the tweet provided.
    """
    return [char for char in str(tweet) if char in vocabulary or char == ' ']


# TODO:
#   - Implement 2 space delimiter as per assignment.
#   - Add some i/o catches for non-existant folder, file, etc. (see project 1)
def output_trace_file(table, v, n, d):
    """Write trace file.
    
    Arguments:
        table {dataframe} -- result of prediction on test set.
        V, n, d {int} -- Parameters of NBClassifier, for use in naming file.
    """
    with open(f"out/trace_{v}_{n}_{d}.txt", 'a') as f:
        f.write(table.to_string(header=False, index=False))
        f.close()
