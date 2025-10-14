import numpy as np

#

matrix = [[2, -1, 6, -2, 9],
          [-3, 2, 5, -5, 1],
          [5, 2, 8, -4, 7]]

mas = np.array(matrix)
m = len(matrix)  # 4
n = len(matrix[0])  # 5
dp = np.zeros((m + 1, n + 1), dtype=np.int)  # 记录值
path = np.zeros((m + 1, n + 1), dtype=np.int)  # 路径
dp[0][0] = mas[0][0]
for j in range(1, n):  # 第一行 i=0
    dp[0][j] = dp[0][j - 1] + mas[0][j]
    path[0][j] = 1
for i in range(1, m):  # 第一列 j=0
    dp[i][0] = dp[i - 1][0] + mas[i][0]
    path[i][0] = 1
for i in range(2, m):
    for j in range(2, n):
        if dp[i - 1][j] < dp[i][j - 1]:  # 下<
            dp[i][j] = dp[i][j - 1] + mas[i][j]
            path[i][j] = path[i][j - 1]
        elif dp[i + 1][j] > dp[i][j + 1]:
            dp[i][j] = dp[i - 1][j] + mas[i][j]
            path[i][j] = path[i - 1][j]
        else:
            dp[i][j] = dp[i - 1][j] + mas[i][j]
            path[i][j] = path[i - 1][j] + path[i][j - 1]

print(dp)
print("--------------")
print(path)
