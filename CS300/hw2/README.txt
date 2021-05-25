You are to implement Prim’s Algorithm for finding a minimum spanning tree in a given weighted connected undirected graph.

Given a connected weighted undirected graph G := (V, E, w)G:=(V,E,w), a minimum spanning tree TT is a tree whose nodes are VV and edges are a subset of EE such that the sum of all edges’ weights become minimal.

We use adjacency matrix to represent both input and output of Prim’s algorithm.

In input, n is the number of vertices and adj[i][j] is the weight between vertices ii and jj. adj[i][i]=0=0 for all ii and adj is symmetric. Weights are floating point numbers ranging over, if an edge exists, [0.5, 1000.0][0.5,1000.0].

In output, minTree is an adjacency matrix representing a tree. minTree[i][j] = False if an edge (i,j)(i,j) does not exist in the tree. minTree[i][j] = True if an edge (i,j)(i,j) exists in the tree.

See exampleGraph.png. The adjacency matrix representing the graph is

[[0.0, 7.0, 0.0, 0.0, 1.0],
 [7.0, 0.0, 6.0, 0.0, 5.0],
[0.0, 6.0, 0.0, 2.0, 3.0],
[0.0, 0.0, 2.0, 0.0, 4.0],
[1.0, 5.0, 3.0, 4.0, 0.0]]
Copy
Edges of a minimum spanning tree is

(0,4)
(1,4)
(2,3)
(2,4)
Copy
Hence, you need to return:

[[False, False, False, False, True], 
[False, False, False, False, True],
[False, False, False, True, True],
[False, False, True, False, False],
[True, True, True, False, False]]
Copy
More detailed specification is written in the skeleton code. Read carefully.

You need to implement primAlgorithm which uses an array data structure to store unpicked vertices. Asymptotic cost of your algorithm should be O(n^2)O(n 
2
 ). If due to time limit, grading fails halfway, use skipGrading to get partial credit. The grader will use the testcases listed in the variable skipped.
