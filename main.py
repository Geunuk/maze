import os
import sys
import argparse
from collections import namedtuple

from algorithm import Node, find_index, bfs, dfs, ids_iter, gbfs, astar

start_fig = 3
key_fig = 6
goal_fig = 4

fun_dict = {"bfs": bfs, "dfs": dfs, "ids": ids_iter, "gbfs": gbfs, "astar": astar}
file_name = {1: ("first_floor_input.txt", "first_floor_output.txt"),
             2: ("second_floor_input.txt", "second_floor_output.txt"),
             3: ("third_floor_input.txt", "third_floor_output.txt"),
             4: ("fourth_floor_input.txt", "fourth_floor_output.txt"),
             5: ("fifth_floor_input.txt", "fifth_floor_output.txt")}

def read_input(floor):
    """Read input file and save meta data and dat in global variable."""
    in_file_name = file_name[floor][0]

    cur_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(cur_path, "floors")
    file_path = os.path.join(data_path, in_file_name)

    with open(file_path, "r") as f:
        # Read first line and get metadata of maze.
        metadata = f.readline()
        floor_in_file, m, n =  metadata.split()
        floor_in_file, m, n = int(floor_in_file), int(m), int(n)
        
        # Check file has different floor number with input.
        if floor != int(floor_in_file):
            print("ERROR: floor is different with floor_in_file")
            sys.exit(-1)

        # Read rest of the file and get data of maze.
        data = []
        for line in f:
            data.append([int(i) for i in line.split()])

        # Check data have diffent m and n with metadata.
        if (len(data) != m or
            any([len(data[i]) != n for i in range(len(data))])):
            print("ERROR: wrong m and n")
            sys.exit(-1)

    print("floor:", floor, "m:", m, "n:", n, end=' ')

    return data, m, n

def write_output(floor, data, length, time):
    """Write changed data to the file."""
    out_file_name = file_name[floor][1]

    cur_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(cur_path, "floors")
    file_path = os.path.join(data_path, out_file_name)

    with open(file_path, "w") as f:
        for line in data:
            new_line = ' '.join([str(i) for i in line]) + '\n'
            f.write(new_line)

        f.write("---\n")
        f.write("length=" + str(length) + "\n")
        f.write("time=" + str(time) + "\n")
    
    print("length:", length, "time:", time)

def backtrace(node):
    """Backtrace from goal node to the start node
    using 'prev' attr and return path.
    """
    result = set()
    tmp_node = node
    while tmp_node.prev != None:
        result.add(tmp_node.index)
        tmp_node = tmp_node.prev
    result.add(tmp_node.index)

    return result

def search_floor(fun, floor):
    """Search key first and goal next. Calculate length and time and chagnge data variable."""
    data, m, n = read_input(floor)

    # Initialize start index
    start_idx = find_index(data, start_fig)
    start_node = Node(start_idx, None, 0)

    # Select algorithm and find key and goal
    key_time, key_node = fun(data, m, n, start_node, key_fig)
    new_start_node = Node(key_node.index, None, 0)   
    goal_time, goal_node = fun(data, m, n, new_start_node, goal_fig)

    length = key_node.depth + goal_node.depth
    time = key_time + goal_time
    
    # Calculate optimal path and change data
    path = set()
    path |= (backtrace(key_node))
    path |= backtrace(goal_node)
    path -= set([start_node.index, goal_node.index])
    for a, b in path:
        data[a][b] = 5

    write_output(floor, data, length, time)

def avg_branch_factor():
    def num_branch(m, n):
        possible_figure = (2, 4, 6)
        result = 0

        if m-1 >= 0 and data[m-1][n] in possible_figure:
            result += 1 
        if m+1 <= max_m-1 and data[m+1][n] in possible_figure:
            result += 1 
        if n-1 >= 0 and data[m][n-1] in possible_figure:
            result += 1 
        if n+1 <= max_n-1 and data[m][n+1] in possible_figure:
            result += 1 
        return result
 
    result = 0
    n = 0

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] in (2, 4, 6):
                n += 1
                result += num_branch(i,j) - 1
    
    return result/n

def test_branch_factor():
    for i in range(1, 6):
        in_file_name, out_file_name = get_file_name(floor)
        read_input(in_file_name, floor)
        print(branch_avg())
               
def test():
    algorithm =  [bfs, dfs, ids_iter, gbfs,astar]
    for fun in algorithm:
        print("fun:", fun.__name__)
        zero_floor(fun)
        if fun != ids_iter:
            first_floor(fun)
        second_floor(fun)
        third_floor(fun)
        fourth_floor(fun)
        fifth_floor(fun)
        print('-'*60)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", metavar='alg', help='select algorithm to use when explore maze')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--floor', metavar='floor', type=int, help="floor to search")
    group.add_argument('-a', '--all', action='store_true', help='explore all fllor')

    args = parser.parse_args()

    if not args.algorithm in fun_dict.keys():
        parser.error("choose algorithm between 'bfs', 'dfs', 'ids', 'gbfs' and 'astar")

    if not args.all and not args.floor in list(range(1,6)):
        parser.error("choose floor between 1 to 5")

    fun = fun_dict[args.algorithm]

    if args.all:
        for floor in range(1, 6):
            search_floor(fun, floor)
    else:
        search_floor(fun, args.floor)

if __name__ == "__main__":
    main()
