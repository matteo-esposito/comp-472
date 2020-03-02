from a_star import *
from board import Board
from input_parser import parse, testfile, collapse_list
from node import Node
from memory_profiler import profile
import time


@profile
def test_mem_iterative(case_args):
    initial_node = Node('0', Board(case_args[3]), 0)
    with open('mem_test_cases/mem_test_search_file.txt', 'w+') as search_file:
        result, final_node = iterative_a_star(*case_args[:3], initial_node, search_file, 0)
        search_file.close()
    return


@profile
def test_mem_recursive(case_args):
    initial_node = Node('0', Board(case_args[3]), 0)
    with open('mem_test_cases/mem_test_search_file.txt', 'w+') as search_file:
        result, final_node = recursive_a_star(*case_args[:3], initial_node, 100000000, search_file, 0, 0)
        search_file.close()
    return


if __name__ == '__main__':
    case1 = 'mem_test_cases/case1.txt'
    case2 = 'mem_test_cases/case2.txt'
    case3 = 'mem_test_cases/case3.txt'

    start = time.time()
    test_mem_iterative(parse(case1)[0])
    print(time.time() - start)
