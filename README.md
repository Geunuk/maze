# mazes

This program find time and length to escape maze and write town path to output file.
To escape maze, first find the key and navigate exit.
For more description, check 'problem_description.pdf'

## Input file
Size of row, size of column were stored at first line.
Afther that, structure of maze is described with wall as '1', paswh as '2', start point as '3', exit point as '4' and key as '6'.  

### Example
5 21 21  
1 3 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 2 1 2 2 2 2 2 1 2 2 2 2 2 1 2 2 2 1 2 1  
1 2 1 1 1 2 1 2 1 2 1 1 1 2 1 2 1 2 1 2 1  
1 2 2 2 2 2 1 2 1 2 2 2 1 2 1 2 1 2 2 2 1  
1 1 1 1 1 1 1 2 1 1 1 2 1 2 1 2 1 1 1 2 1  
1 2 2 2 2 2 1 2 2 2 1 2 1 2 1 2 2 2 1 2 1  
1 2 1 1 1 2 1 1 1 2 1 2 1 2 1 1 1 2 1 2 1  
1 2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2 1 2 1  
1 2 1 2 1 1 1 2 1 1 1 1 1 1 1 2 1 2 1 1 1  
1 2 1 2 1 2 2 2 1 2 2 2 2 6 1 2 1 2 2 2 1  
1 2 1 2 1 1 1 2 1 2 1 2 1 1 1 2 1 2 1 2 1  
1 2 1 2 2 2 1 2 1 2 1 2 2 2 2 2 1 2 1 2 1  
1 2 1 1 1 2 1 2 1 2 1 1 1 1 1 1 1 1 1 2 1  
1 2 1 2 1 2 1 2 1 2 2 2 1 2 2 2 2 2 2 2 1  
1 2 1 2 1 2 1 1 1 1 1 2 1 2 1 2 1 1 1 2 1  
1 2 1 2 1 2 1 2 2 2 2 2 1 2 1 2 1 2 1 2 1  
1 2 1 2 1 2 1 2 1 1 1 1 1 2 1 2 1 2 1 2 1  
1 2 1 2 1 2 1 2 1 2 2 2 1 2 1 2 1 2 2 2 1  
1 2 1 2 1 2 1 2 1 2 1 2 1 1 1 2 1 2 1 1 1  
1 2 2 2 1 2 2 2 2 2 1 2 2 2 2 2 1 2 2 2 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 4 1  

## Supported Algorithms
* A*(astar) - Heuristic function: manhattan dist + (euclidean dist/manhattan dist - 1)
* Greedy Best First Search(gbfs)
* Breadth First Search(bfs)
* Depth First Search(dfs)
* Iterative Deepening Search(ids)

## Run Algorithm for one floort
Choose floor between 1 to 5.  
Choose Algorithm between astar, gbfs, bfs, dfs, ids  
```
$python3 main.py -f [floor] [algorithm]
```


## Run algorithm for all floors

```
$python3 main.py -a [algorithm]
```

## Notice
For detailed decription of whole result and heuristic, look 'report.pdf'
