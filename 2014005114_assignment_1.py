from collections import deque, namedtuple
import heapq
import sys

max_m = 0
max_n = 0
data = []
Node = namedtuple("Node", "index prev depth")

def get_file_name(floor):
    """Get floor number and return input and output filename."""
    if floor == 1:
        in_file_name = "first_floor_input.txt"
    elif floor == 2:
        in_file_name = "second_floor_input.txt"
    elif floor == 3:
        in_file_name = "third_floor_input.txt"
    elif floor == 4:
        in_file_name = "fourth_floor_input.txt"
    elif floor == 5:
        in_file_name = "fifth_floor_input.txt"
    else:
        print("ERROR: wrong floor")
        sys.exit(-1)

    out_file_name = in_file_name.replace("input", "output")
    return in_file_name, out_file_name

def read_input(file_name, floor):
    """Read input file and save meta data and dat in global variable."""
    global max_m, max_n, data

    with open(file_name, "r") as f:
        # Read first line and get metadata of maze.
        metadata = f.readline()
        floor_in_file, max_m, max_n =  metadata.split()
        floor_in_file, max_m, max_n = int(floor_in_file), int(max_m), int(max_n)
        
        # Check file has different floor number with input.
        if floor != int(floor_in_file):
            print("ERROR: floor is different with floor_in_file")
            sys.exit(-1)

        # Read rest of the file and get data of maze.
        data = []
        for line in f:
            data.append([int(i) for i in line.split()])

        # Check data have diffent m and n with metadata.
        if (len(data) != max_m or
            any([len(data[i]) != max_n for i in range(len(data))])):
            print("ERROR: wrong m and n")
            sys.exit(-1)

    print("floor:", floor, "m:",max_m, "n:", max_n, end=' ')

def write_output(file_name, length, time):
    """Write changed data to the file."""
    with open(file_name, "w") as f:
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

def search_floor(fun):
    """Search key first and goal next. Calculate length and time and chagnge data variable."""
    global data

    start_fig = 3
    key_fig = 6
    goal_fig = 4

    # Initialize start index
    start_idx = find_index(start_fig)
    start_node = Node(start_idx, None, 0)

    # Select algorithm and find key and goal
    key_time, key_node = fun(start_node, key_fig)
    new_start_node = Node(key_node.index, None, 0)   
    goal_time, goal_node = fun(new_start_node, goal_fig)

    length = key_node.depth + goal_node.depth
    time = key_time + goal_time
    
    # Calculate optimal path and change data
    path = set()
    path |= (backtrace(key_node))
    path |= backtrace(goal_node)
    path -= set([start_node.index, goal_node.index])
    for a, b in path:
        data[a][b] = 5
    
    return length, time

def f(node, fig, g):
    """Returns g+h value.

    g : cost from start to now(depth)
    h : heuristic function(MD+ED/MD-1)
    """            
    m, n = node.index
    p, q = fig

    h = abs(m-p)+abs(n-q)
    h += ((m-p)**2+(n-q)**2)**0.5 - 1

    return g(node) + h

def find_index(figure):
    """Returns tuple index of figure."""
    for i in range(len(data)):
        try:
            j = data[i].index(figure)
        except ValueError:
            pass
        else:
            return (i,j)
            break
       
def gbfs(init_node, figure):
    return astar_body(init_node, figure, lambda node : 0)

def astar(init_node, figure):
    return astar_body(init_node, figure, lambda node : node.depth)

def astar_body(init_node, figure, g):
    """A* algorithm. Return explored indices and goal index."""
    explored = set()
    fig_idx = find_index(figure)

    # Push tuple (f, idx) to the heap
    h = [(f(init_node, fig_idx, g), init_node)]
    while h:   
        elm = heapq.heappop(h)
        explored.add(elm[1].index)

        # Goal test
        m, n = elm[1].index
        if data[m][n] == figure:
            return len(explored), elm[1]

        for c in find_successor(elm[1], figure):
            if c.index not in (explored or [x.index for _,x in h]):
                heapq.heappush(h, (f(c, fig_idx, g), c))
    else:
        print("FAILED: cannot found figure")
        sys.exit(-1)

def find_successor(idx, figure):
    """Return successor indices."""
    m, n = idx.index
    result = set()
    possible_figure = (2, figure)
    
    # Successor index must be in maze.
    if m-1 >= 0:
        result.add((m-1, n))
    if m+1 <= max_m-1:
        result.add((m+1, n))
    if n-1 >= 0:
        result.add((m, n-1))
    if n+1 <= max_n-1:
        result.add((m, n+1))

    # Data in successor index should be possible figure
    # and index has incremented depth.
    result = [Node((a,b), idx, idx.depth+1) for a, b in result
              if data[a][b] in possible_figure]
    return result

def bfs(init_node, figure):
    """Breadth first search. Return explored indices and goal index."""
    explored = set()
    d = deque([init_node])

    while d:   
        node = d.pop()
        explored.add(node.index)
        for c in find_successor(node, figure):
            if c.index not in explored and c not in d:
                # Goal test
                m, n = c.index
                if data[m][n] == figure:
                    return len(explored), c
                else:
                    d.appendleft(c)
    else:
        print("FAILED: cannot found figure")
        sys.exit(-1)

def dfs(init_node, figure):
    """Depth first search. Return explored indices and goal index."""
    explored = set()
    s = [init_node]

    while s:   
        node = s.pop()
        explored.add(node.index)
        # Goal test
        m, n = node.index
        if data[m][n] == figure:
            return len(explored), node
        for c in find_successor(node, figure):
            if c.index not in explored and c not in s:
                s.append(c)
    else:
        print("FAILED: cannot found figure")
        sys.exit(-1)

def dls(init_idx, figure, depth):
    """Recursion version Depth-limeted search."""
    explored = set()
    result = dls_recursive(init_idx, figure, depth, explored)
    
    return len(explored), result

def dls_recursive(idx, figure, limit, explored):
    """Helper function for dls."""
    explored |= set([idx.index])
    m, n = idx.index
    if data[m][n] == figure:
        return idx
    elif limit == 0:
        return 'C'
    else:
        cut_occured = False
        for c in find_successor(idx, figure):
            if c.index not in backtrace(idx):
                result = dls_recursive(c, figure, limit-1, explored)
                if result == 'C':
                    cut_occured = True
                elif result != 'F':
                    return result
        if cut_occured:
            return 'C'
        else:
            return 'F'

def ids_recur(init_idx, figure):
    """Recursion version iterative-deepening search."""
    time = 0
    for depth in range(max_m*max_n):
        depth_time, result = dls(init_idx, figure, depth)
        time += depth_time
        if result != ('C' or 'F'):
            return time, result

    if result == 'C':
        print("FAILED: cutoff")
    elif result == 'F':
        print("FAILED: failed")
    sys.exit(-1)

def dls_iter(init_node, figure, depth):
    """Iteration version Depth-limeted search."""
    explored = set()
    s = [init_node]

    while s:   
        node = s.pop()
        if node.depth > depth:
            continue
        explored.add(node.index)

        for c in find_successor(node, figure):
            if c.index not in explored and c not in s:
                # Goal test
                m, n = c.index
                if data[m][n] == figure:
                    return len(explored), c
                else:
                    s.append(c)
    else:
        return len(explored), 'C'

def ids_iter(init_idx, figure):
    """Iteration version iterative-deepening search."""
    time = 0
    for depth in range(max_m*max_n):
        depth_time, result = dls_iter(init_idx, figure, depth)
        time += depth_time
        if result != ('C' or 'F'):
            return time, result

    if result == 'C':
        print("FAILED: cutoff")
    elif result == 'F':
        print("FAILED: failed")
    sys.exit(-1)

def execute(floor, fun):
    """Read input and start searching. Write result to the output file"""
    in_file_name, out_file_name = get_file_name(floor)
    read_input(in_file_name, floor)
    length, time = search_floor(fun)
    write_output(out_file_name, length, time)

def first_floor(fun):
    execute(1, fun)

def second_floor(fun):
    execute(2, fun)

def third_floor(fun):
    execute(3, fun)

def fourth_floor(fun):
    execute(4, fun)

def fifth_floor(fun):
    execute(5, fun)

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

if __name__ == "__main__":
    algorithm =  astar
    first_floor(algorithm)
    second_floor(algorithm)
    third_floor(algorithm)
    fourth_floor(algorithm)
    fifth_floor(algorithm)
