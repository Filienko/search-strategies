# search-strategies
Experimenting with various uninformed and informed search strategies for a classic slide puzzle
The game outputs **only the path of the final solution**, not every node visited. 

To input the puzzle, follow that format:

[size] [current puzzle board state] [search strategy]

where:

**size**[0...7] produces a 7 by 7 target state

**current puzzle board state** requries to provide the 'size by size' current state

**search strategy**[DFS, BFS, GBFS[Greedy], Astar] searches for the solution, if exists, utilizing the listed search strategy

DFS and GBFS are not complete, solution may not be found, but it would attemp to trace all possible solutions. Also, to speed up computation, depth-limited DFS was implemented. That ensures better effeciency, limiting the depth, however ensures the non-completeness.

e.g. 2 "32 1" BFS

For more examples, look at input.txt file. 
