2D Range Counting
Given NN integer points and QQ rectangles on xy-plane, find the number of points for each rectangle.

Instructions
Your task is to fill in two methods within the class Solution: __init__() and query().

__init__(points) takes the points and initializes Solution.
query(rect) takes the rectangle and returns the answer.
Your submittion will be tested in a similar way below.

sol = Solution(points)
if sol.query(rect) == answer:
    print('passed')
else:
    print('wrong answer')
Copy
You’re allowed to

add/edit functions and classes
use Python standard library https://docs.python.org/3/library/, and
use your source code from the previous homework
You’re NOT allowed to

use any 3rd party plug-ins including but not limited to numpy, and
plagiarize someone else’s code
The score of the last submission is your final score.

Input
All values are integers.

points
List of points
[ [x1,y1], [x2,y2], … , [xN, yN] ]
It may contain duplicate points.

rect
Rectangle [x_L,x_R]\times [y_L,y_R][x 
L
​	
 ,x 
R
​	
 ]×[y 
L
​	
 ,y 
R
​	
 ] represented by

[ [xL,xR], [yL,yR] ]

with xL <= xR and yL <= yR.
It may have an area of 0. See the samples below.

Output
query(rect) must return the number of points within rect, inclusive.

Test Sets
Each test set will initialize Solution with N points and call query(rect) Q times with changing rect.

IMPORTANT
The time limit only applies to query().

Each set will be tested only if your code passed the previous one. For example, if your code failed on test set 2, then test set 3 and 4 won’t be tested.

Test Set 1 (10pts)
N=5
Q=10
Time limit for all queries = 2s
Copy
Test Set 2 (20pts)
N=1000
Q=1000
Time limit for all queries = 4s
Copy
Test Set 3 (30pts)
N=5000
Q=20000
Time limit for all queries = 6s
Copy
Test Set 4 (40pts)
N=20000
Q=50000
Time limit for all queries = 15s
Copy
Samples
Sample 1
points = [[1, 1], [3, 3], [2, 2], [1, 3]]
query([[1,3], [1,3]]) must return 4
query([[1,5], [2,5]]) must return 3
Copy
Explanation
We have four points (1,1)(1,1), (3,3)(3,3), (2,2)(2,2) and (1,3)(1,3).
The first query asks the number of points (x,y)(x,y) such that 1\leq x \leq 31≤x≤3 and 1\leq y \leq 31≤y≤3, hence the answer is 4.
The second query asks the number of points (x,y)(x,y) such that 1\leq x \leq 51≤x≤5 and 2\leq y \leq 52≤y≤5, hence the answer is 3.
Sample 2
points = [[-2, 1], [0, 1], [2, 1], [-2, -1], [0, -1], [2, -1]]
query([[0, 0], [-2, 2]]) must return 2
query([[1, 2], [0, 0]]) must return 0
Copy
Sample 3
points = [[0, 0], [0, 0], [0, 0]]
query([[0, 0], [0, 0]]) must return 3
