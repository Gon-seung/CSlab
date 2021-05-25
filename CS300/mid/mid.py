




class Solution(object):
    
    def __init__(self, points):
        """
        Initialize this class instance.

        Parameters
        ----------
        points : list of integer coordinates, each of form [x,y], that is
                 [[x1,y1], [x2,y2], ... , [xN,yN]]
        """
        self.Wid_min = points[0][0]
        self.Wid_max = points[0][0]
        self.Hei_min = points[0][1]
        self.Hei_max = points[0][1]
        self.Exist_list = []
        self.Sort_list = self.sort1(points)
        self.exist()

        self.DP = []
        tmp = [[]] * (self.Wid_max - self.Wid_min + 1)
        for i in range(len(self.Exist_list)):
            self.DP += [[[]]]
            for j in range(len(self.Exist_list) - 1):
                self.DP[i] += [[]]
        self.makedp()
        
    def adddp(self, start, end):
        if len(self.DP[start][end]) != 0:
            return 0
        if start + 1 == end:
            self.DP[start][end] = self.DP[start][end-1] + self.DP[end][end]
            self.DP[start][end].sort()
            return 0
        avg = int ((start + end) / 2)
        self.adddp(start,avg)
        self.adddp(avg + 1 , end)
        self.DP[start][end] = self.DP[start][avg] + self.DP[avg + 1][end]
        self.DP[start][end].sort()
        return 0

    def makedp(self):
        sort_pos = 0
        for pos in range(len(self.Exist_list)):
            i = self.Exist_list[pos]
            while sort_pos < len(self.Sort_list) and i == self.Sort_list[sort_pos][0]:
                self.DP[pos][pos] += [self.Sort_list[sort_pos][1]]
                sort_pos += 1

        self.adddp(0, len(self.Exist_list) - 1)

    def exist(self):
        for i in self.Sort_list:
            
            if len(self.Exist_list) == 0 or self.Exist_list[-1] != i[0]:
                self.Exist_list += [i[0]]

    def sort1(self, x):

        ##print(x)
        if len(x) == 1:
            if x[0][0] > self.Wid_max:
                self.Wid_max = x[0][0]
            if x[0][0] < self.Wid_min:
                self.Wid_min = x[0][0]
            if x[0][1] > self.Hei_max:
                self.Hei_max = x[0][1]
            if x[0][1] < self.Hei_min:
                self.Hei_min = x[0][1]
            return x
        x1 = x[: int (len(x) / 2)]
        x2 = x[int (len(x) / 2) :]
        x1 = self.sort1(x1)
        x2 = self.sort1(x2)
        ans = []
        pos1 = 0
        pos2 = 0
        for i in range(len(x)):
            if pos2 == len(x2):
                ans.append(x1[pos1])
                pos1 +=1
            elif pos1 == len(x1):
                ans.append(x2[pos2])
                pos2 +=1
            elif x1[pos1][0] > x2[pos2][0]:
                ans.append(x2[pos2])
                pos2 +=1
            elif x1[pos1][0] < x2[pos2][0]:
                ans.append(x1[pos1])
                pos1 +=1
            elif x1[pos1][1] > x2[pos2][1]:
                ans.append(x2[pos2])
                pos2 +=1
            else:
                ans.append(x1[pos1])
                pos1 +=1

        return ans
    
    def find_min(self, x , y, num):
        newlist = self.DP[x][y]
        min = -1
        max = len(newlist)
        while min + 1 < max:
            avg = int ((min + max) / 2)
            #print(min , max, points[avg][xy])
            if newlist[avg] < num:
                min = avg
            else:
                max = avg
        return min + 1

    def find_max(self, x , y, num):
        newlist = self.DP[x][y]
        min = -1
        max = len(newlist)
        while min + 1 < max:
            avg = int ((min + max) / 2)
            #print(min , max, points[avg][xy])
            if newlist[avg] <= num:
                min = avg
            else:
                max = avg
        return min
    
    def find_min1(self, num):
        min = -1
        max = len(self.Exist_list)
        while min + 1 < max:
            avg = int ((min + max) / 2)
            #print(min , max, points[avg][xy])
            if self.Exist_list[avg] <= num:
                min = avg
            else:
                max = avg
        return min
    
    def find_ans(self,start, end, pos1, pos2, starth, endh):
        avg = int ((pos1 + pos2) / 2)
        if start == end:
            return self.find_max(start,end, endh) - self.find_min(start,end, starth) + 1
        if start == pos1 and end == pos2 and len(self.DP[pos1][pos2]) != 0:
            return self.find_max(start,end, endh) - self.find_min(start,end, starth) + 1
        if start <= avg and avg < end:
            return self.find_ans(start,avg,pos1,avg, starth, endh) + self.find_ans(avg + 1 , end, avg + 1 , pos2, starth, endh)
        if start <= avg and avg >= end:
            return self.find_ans(start,end,pos1,avg, starth, endh)
        return self.find_ans(start,end,avg + 1,pos2, starth, endh)


    def query(self, rect) -> int:
        startw = rect[0][0]
        endw = rect[0][1]
        starth = rect[1][0]
        endh = rect[1][1]

        if startw < self.Wid_min:
            startw = self.Wid_min
        if endw > self.Wid_max:
            endw = self.Wid_max
        if starth < self.Hei_min:
            starth = self.Hei_min
        if endh > self.Hei_max:
            endh = self.Hei_max
        answer = 0
        pos1 = self.find_min1(startw)
        pos2 = self.find_min1(endw)
        if (self.Exist_list[pos1] < startw): pos1 += 1
        print(pos1, ":", pos2)
        if startw > self.Wid_max or endw < self.Wid_min or starth > self.Hei_max or endh < self.Hei_min or pos2  < pos1:
            return 0
        return self.find_ans(pos1,pos2,0,len(self.Exist_list) - 1, starth, endh)


        """
        Find the number of points within the given rectangle

        Parameters
        ----------
        rect: [[xL,xR], [yL,yR]]
              where xL, xR, yL and yR are integers with xL <= xR and yL <= yR

        Returns
        -------
        int
            the number of point (x, y)
            such that xL <= x <= xR and yL <= y <= yR
        """
    
    


    

if __name__ == "__main__":

    points = [[1,1], [3,3], [2,2], [1,3]]
    sol = Solution(points)
    print(sol.Sort_list)
    print(sol.DP)
    print(sol.Exist_list)
    print(sol.query([[1,3], [1,3]]))       # 4
    print(sol.query([[1,5], [2,5]]))       # 3
    
    points = [[-2, 1], [0, 1], [2, 1], [-2, -1], [0, -1], [2, -1]]
    sol = Solution(points)
    print(sol.Sort_list)
    print(sol.DP)
    print(sol.Exist_list)
    print(sol.query([[0, 0], [-2, -1]])) 
    #must return 2
    print(sol.query([[-5, 2], [0, 1]]))
    #0

    
    asdf = [[0,0], [0,0], [0,0]]
    sol = Solution(asdf)
    print(sol.Sort_list)
    #print(sol.DP)
    print(sol.query([[0, 0], [-1, 0]])) #must return 3
    
    
