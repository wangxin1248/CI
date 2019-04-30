# 模拟退火算法实现01背包问题
import random
import numpy as np
import math

c = 8# 背包容量
n = 5# 物体个数
w = [2, 3, 5, 1, 4]# 重量
v = [2, 5, 8, 3, 6]# 价值
initial_t = 100# 初始温度
lowest_t = 0.001# 最低温度
max_m = 100#当连续多次都不接受新的状态，开始改变温度
iteration = 100#设置迭代次数

def get_current_value(solve):
    """
    计算当前解的物品价值
    """
    value = 0
    for i in range(len(solve)):
        if solve[i] == 1:
            value += v[i]
    return value

def get_current_weight(solve):
    """
    计算当前解的物品重量
    """
    weight = 0
    for i in range(len(solve)):
        if solve[i] == 1:
            weight += w[i]
    return weight

# ============初始化============

# 初始温度
current_t = initial_t
# 初始解
# flag_first = False
# while not flag_first:
#     solve_i = np.random.randint(2, size=n)
#     if get_current_weight(solve_i) <= c:
#         flag_first = True
solve_i = [1, 1, 0, 0, 1]
print("初始解：", solve_i)
# 最优解
solve_best = solve_i
# 初始解的物品价值
current_value = get_current_value(solve_i)

# ============开始循环============

# 外循环，改变温度
while current_t > lowest_t:
    # m计数器
    count_m = 0
    # 迭代次数计数器
    count_iter = 0

    # 内循环，连续多次不接受新的状态或者是迭代多次,跳出内循环
    while count_m < max_m and count_iter < iteration:
        # 根据当前解生成一个邻域解(随机交换某两位的0/1值)
        flag = False
        while not flag:
            i = 0
            j = 0
            while i == j:
                i = random.randint(0, n-1)
                j = random.randint(0, n-1)
            solve_j = solve_i
            solve_j[i], solve_j[j] = solve_j[j], solve_j[i]

            # 舍弃非法解
            if get_current_weight(solve_j) > c:
                flag = False
            else:
                flag = True
        
        # 计算新解的适应值
        j_value = get_current_value(solve_j)
        if j_value > current_value:
            # 新解价值大则接受新解
            solve_i = solve_j
            current_value = j_value
            solve_best = solve_j
        elif j_value < current_value:
            # 新解价值小则按照一定的概率接受劣解
            probability = math.exp((j_value-current_value)/initial_t)
            random_i = random.random()
            if random_i < probability:
                solve_i = solve_j
                current_value = j_value
                solve_best = solve_j
        else:
            count_m += 1
        count_iter += 1
    # 降温
    current_t *= 0.99

# 外循环结束，打印结果
print("最优解", solve_best)
print("最优解对应的价值", get_current_value(solve_best))
