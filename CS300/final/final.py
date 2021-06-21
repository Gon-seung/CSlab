def solution(A):
    """
    Find the maximum score

    Parameter
    ----------
    A : list of N+2 numbers with A[0]=A[N+1]=1
    """

    size = len(A) # size = N + 2
    DP = list(range(size))
    for i in range(size):
        DP[i] = list(range(size))
    
    for i in range(size):
        for j in range(len(DP[i])):
            DP[i][j] = 0
    for i in range(size - 2):
        DP[i][i + 2] = A[i]* A[i + 1] * A[i + 2]
    
    #print(DP)
    for j in range(4, size + 1):
        for i in range(size):
            if(i + j > size):
                continue
            for k in range(i + 1, i + j - 1):
                tmp = DP[i][k] + DP[k][i + j - 1] + A[i] * A[k] * A[i + j - 1]
                if(DP[i][i + j - 1] < tmp):
                    DP[i][i + j - 1] = tmp

    print(DP)
    return DP[0][size - 1]


if __name__ == "__main__":
    # sample 1
    A = [1,2,3,4,1]
    answer = solution(A)
    print(answer)      # 36