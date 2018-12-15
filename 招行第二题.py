#coding=utf-8
import sys

if __name__ == "__main__":
    # 读取第一行的n
    t = int(sys.stdin.readline().strip())
    for i in range(t):
        ans = 0
        line = sys.stdin.readline().strip()
        n = int(line)
        line = sys.stdin.readline().strip()
        values = list(map(int, line.split()))
        #print(values)
        #print(t)
        buy_num = []
        for count in range(0,n):
            buy_num.append(1)
        stop = 100
        while buy_num.count(1)>0:# and stop>0:
            #rint("ca")
            max_index = values.index(max(values))
            ans += max(values)
            values[max_index] = -1
            buy_num[max_index] = 0
            if max_index==0:
                buy_num[1] = 0
                values[1] = -1
                buy_num[n-1] = 0
                values[n-1] = -1
            elif max_index==n-1:
                buy_num[n-2] = 0
                values[n-2] = -1
                buy_num[0] = 0
                values[0] = -1
            else:
                buy_num[max_index-1] = 0
                values[max_index-1] = -1
                buy_num[max_index+1] = 0
                values[max_index+1] = -1
            #stop -= 1
        print(ans)

