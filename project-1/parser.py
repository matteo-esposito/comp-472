# Let test file be importable
testfile = "test-cases-and-solutions/test.txt"

def parse(filepath):
    """
    Function to parse a .txt file with the following format:

        3 7 100 111001011

    Arguments:
        filepath {String} -- filepath to input .txt file

    Returns:
        Nested list -- nested list where each inner list is composed of the 4 inputs 
                       (3 integers and one grid (in nested list form))

        [
        3, 7, 100, [[1, 1, 1], 
                    [0, 0, 1], 
                    [0, 1, 1]]
        ]

        Inputs:
            "1. the size of the puzzle (n)
            2. the maximum depth search for DFS (max_d)
            3. the maximum search path length (max_l) for BFS and A⋆
            4. the values of the initial puzzle’s n × n tokens, where each token will be represented by a 1 (•) or a 0 (◦). The order of the tokens will be left-to-right, top-down.

            Note: When using DFS, you can ignore maxl and when using BFS or A⋆ , you can ignore max_d."
    """
    
    # Open and read file
    with open(filepath) as f:
        lines = [line.rstrip().split(" ") for line in f]

    # Parse input data
    nested_outlist = []
    for l in lines:
        # Initialize list and grid string
        inner_list = []
        grid = l[3]
        
        # Append first 3 entries
        for entry in l[:3]:
            inner_list.append(int(entry))
        
        # Deal with 4th entry (turn into int grid row and append to inner_list)
        grid_size = inner_list[0]
        string_grid = [list(grid[i:i + grid_size]) for i in range(0, len(l[3]), grid_size)] # Split string into rows
        fourth_element = [list(map(int, row)) for row in string_grid] # Convert entries to int
        inner_list.append(fourth_element)
        
        nested_outlist.append(inner_list)

    return nested_outlist
