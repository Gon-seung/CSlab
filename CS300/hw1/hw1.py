
def main():
    print('hello')
    print(distinct([1,2,3,4,4,6,7,8]))


def linear_search(arr, x):
    """
    Performs linear search to find the index of `x` in `arr`.
    
    Parameters
    ----------
    arr : list of int
    x : int
    
    Returns
    -------
    int
        the index `i` such that `x == arr[i]` if such `i` exists,
        otherwise -1
    """
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    
    return -1
    


def binary_search(arr, x):
    """
    Performs binary search on already sorted list to find the index for `x` in `arr`.
    
    Parameters
    ----------
    arr : list of int
        already sorted in ascending order
    x : int
    
    Returns
    -------
    int
        the smallest index `i` such that `x < arr[i]` while assuming that
        the imaginary leftmost element of `arr` is negative infinity and
        the imaginary rightmost element of `arr` is positive infinity
        (if `x` is greater than or equal to every element in `arr`, then return the length of `arr`)
    """
    if x >= arr[len(arr) - 1]:
        return len(arr)

    left = 0
    right = len(arr) - 1
    mid = int((left + right) / 2)
    while(left < right):
        print(str(left) + " : " + str(right) + "\n")
        mid = int((left + right) / 2)
        if x >= arr[mid]:
            mid = mid + 1
            left = mid
        else:
            right = mid

    return mid

    
    
def distinct(arr):
    '''
    Tests whether all elements in given list are distinct or not.
    (Please implement it using hashing as in lecture slides.)
    
    Parameters
    ----------
    arr : list of int
        nonempty list whose length is at most 20,000 and whose elements are positive
    Returns
    -------
    bool
        `True` if all elements are distinct,
        `False` otherwise
    '''
    hash_table = [0 for i in range(20011)]
    for i in range(len(arr)):
        p = arr[i] % 20011
        while hash_table[p] != 0:
            if hash_table[p] == arr[i]:
                return False
            p = p + 1 % 20011
        hash_table[p] = arr[i]
    return True





if __name__ == "__main__":
    main()



