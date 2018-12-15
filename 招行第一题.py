#coding=utf-8
import sys
#sys.setrecursionlimit(1000000) #例如这里设置为一百万




def get_count( money,coins ):
    if money < 0 :
        return 0
    if money == 0:
        return 1
    if money < min(coins):
        return 0
    count = 0
    for coin in coins:
        temp = get_count( money-coin, coins )
        if get_count( money-coin, coins )>0:
            count+=temp
    #print("money:%d"%money)
    #print("count%d"%count)
    return( count )


if __name__ == "__main__":
    # 读取第一行的n
    t = int(sys.stdin.readline().strip())
    for i in range(t):
        ans = 0
        # 读取每一行
        line = sys.stdin.readline().strip()
        # 把每一行的数字分隔后转化成int列表
        values = list(map(int, line.split()))
        kind = values[0]
        total_money = values[1]
        line = sys.stdin.readline().strip()
        coins = list(map(int, line.split()))
        clins=list(reversed(coins))
        ans = get_count( total_money,coins )

        print(ans)