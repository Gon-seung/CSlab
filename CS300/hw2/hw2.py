
def main():

    exampleGraph = [[0.0, 7.0, 0.0, 0.0, 1.0],
                    [7.0, 0.0, 6.0, 0.0, 5.0],
                    [0.0, 6.0, 0.0, 2.0, 3.0],
                    [0.0, 0.0, 2.0, 0.0, 4.0],
                    [1.0, 5.0, 3.0, 4.0, 0.0]]
                    
    MST = primAlgorithm(5, exampleGraph)
    
    for i in range(5):
        s = ""
        for j in range(5):
            s += (str(MST[i][j]) + " ")
        print(s)
        

# The assignment has 10 testcases.
# store indices of the testcases you want to skip
# for example: [9,10] => skip 9th and the last (10th) test cases
# store any number not within [1, ..., 10] if you don't want to skip any testcases
skipGrading = [0]



# PRIM'S ALGORITHM: Given a weighted connected undirected graph, compute a MST.
#      INPUT:   n: number of vertices 
#               adj: adjacency matrix (2-dimensional array) with weights             
#                   adj[0][3] (= adj[3][0]) is the weight of the edge between vertex 0 and vertex 3
#                   weight of an edge is a floating point number between [0.5, 1000]
#                   if there is no edge between i and j, adj[i][j] = 0
#      OUTPUT:  minTree: adjacency matrix (2-dimensional array) with boolean entries of the MST
#                   minTree[i][j] = True if the MST has an edge between the vertex i and j
#                   minTree[i][j] = False if the MST has no edge between the vertex i and j
def primAlgorithm(n, adj):
    minTree = [x[:] for x in [[False] * n] * n]   
    
#     implement here
    node = [0]
    dis = []

    while(len(node) != n):
        for i in range(n):
            if(adj[node[-1]][i] != 0 and not (i in node)):
                dis.append([i,adj[node[-1]][i], node[-1]])
        min = 10000
        pos1 = 0
        pos2 = 0
        del_pos = []
        for i in range(len(dis)):
            if(dis[i][1] < min and not (dis[i][0] in node)):
                pos1 = dis[i][2]
                pos2 = dis[i][0]
                min = dis[i][1]
            elif (dis[i][0] in node):
                del_pos.append(dis[i])
        node.append(pos2)
        while(len(del_pos) > 0):
            dis.remove(del_pos[-1])
            del_pos.pop()
        minTree[pos1][pos2] = True
        minTree[pos2][pos1] = True

        
    return minTree







if __name__ == "__main__":
    main()
