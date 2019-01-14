from collections import deque, namedtuple
import heapq
import sys

Node = namedtuple("Node", "index prev depth")

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

def find_index(data, figure):
    """Returns tuple index of figure."""
    for i in range(len(data)):
        try:
            j = data[i].index(figure)
        except ValueError:
            pass
        else:
            return (i,j)
            break
       
def gbfs(data, m, n, init_node, figure):
    return astar_body(data, m, n, init_node, figure, lambda node : 0)

def astar(data, m, n, init_node, figure):
    return astar_body(data, m, n, init_node, figure, lambda node : node.depth)

def astar_body(data, m, n, init_node, figure, g):
    """A* algorithm. Return explored indices and goal index."""
    explored = set()
    fig_idx = find_index(data, figure)

    # Push tuple (f, idx) to the heap
    h = [(f(init_node, fig_idx, g), init_node)]
    while h:   
        elm = heapq.heappop(h)
        explored.add(elm[1].index)
        # Goal test
        x, y = elm[1].index
        if data[x][y] == figure:
            return len(explored), elm[1]
        for c in find_successor(data, m, n, elm[1], figure):
            if c.index not in (explored or [x.index for _,x in h]):
                heapq.heappush(h, (f(c, fig_idx, g), c))
    else:
        print("FAILED: cannot found figure")
        sys.exit(-1)

def find_successor(data, m, n, idx, figure):
    """Return successor indices."""
    x, y = idx.index
    result = set()
    possible_figure = (2, figure)
    
    # Successor index must be in maze.
    if x-1 >= 0:
        result.add((x-1, y))
    if x+1 <= m-1:
        result.add((x+1, y))
    if y-1 >= 0:
        result.add((x, y-1))
    if y+1 <= n-1:
        result.add((x, y+1))
    
    # Data in successor index should be possible figure
    # and index has incremented depth.
    result = [Node((a,b), idx, idx.depth+1) for a, b in result
              if data[a][b] in possible_figure]
    return result

def bfs(data, m, n, init_node, figure):
    """Breadth first search. Return explored indices and goal index."""
    explored = set()
    d = deque([init_node])

    while d:   
        node = d.pop()
        explored.add(node.index)
        for c in find_successor(data, m, n, node, figure):
            if c.index not in explored and c not in d:
                # Goal test
                x, y = c.index
                if data[x][y] == figure:
                    return len(explored), c
                else:
                    d.appendleft(c)
    else:
        print("FAILED: cannot found figure")
        sys.exit(-1)

def dfs(data, m, n, init_node, figure):
    """Depth first search. Return explored indices and goal index."""
    explored = set()
    s = [init_node]

    while s:   
        node = s.pop()
        explored.add(node.index)
        # Goal test
        x, y = node.index
        if data[x][y] == figure:
            return len(explored), node
        for c in find_successor(data, m, n, node, figure):
            if c.index not in explored and c not in s:
                s.append(c)
    else:
        print("FAILED: cannot found figure")
        sys.exit(-1)

def dls(data, m, n, init_idx, figure, depth):
    """Recursion version Depth-limeted search."""
    explored = set()
    result = dls_recursive(init_idx, figure, depth, explored)
    
    return len(explored), result

def dls_recursive(data, m, n, idx, figure, limit, explored):
    """Helper function for dls."""
    explored |= set([idx.index])
    x, y = idx.index
    if data[m][n] == figure:
        return idx
    elif limit == 0:
        return 'C'
    else:
        cut_occured = False
        for c in find_successor(data, m, n, idx, figure):
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

def ids_recur(data, m, n, init_idx, figure):
    """Recursion version iterative-deepening search."""
    time = 0
    for depth in range(m*n):
        depth_time, result = dls(data, m, n, init_idx, figure, depth)
        time += depth_time
        if result != ('C' or 'F'):
            return time, result

    if result == 'C':
        print("FAILED: cutoff")
    elif result == 'F':
        print("FAILED: failed")
    sys.exit(-1)

def dls_iter(data, m, n, init_node, figure, depth):
    """Iteration version Depth-limeted search."""
    explored = set()
    s = [init_node]

    while s:   
        node = s.pop()
        if node.depth > depth:
            continue
        explored.add(node.index)

        for c in find_successor(data, m, n, node, figure):
            if c.index not in explored and c not in s:
                # Goal test
                x, y = c.index
                if data[x][y] == figure:
                    return len(explored), c
                else:
                    s.append(c)
    else:
        return len(explored), 'C'

def ids_iter(data, m, n, init_idx, figure):
    """Iteration version iterative-deepening search."""
    time = 0
    for depth in range(m*n):
        depth_time, result = dls_iter(data, m, n, init_idx, figure, depth)
        time += depth_time
        if result != ('C' or 'F'):
            return time, result

    if result == 'C':
        print("FAILED: cutoff")
    elif result == 'F':
        print("FAILED: failed")
    sys.exit(-1)

if __name__ == "__main__":
    ...
