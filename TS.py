# 使用禁忌搜索算法实现旅行商问题

num_city = 4# 城市总数
location=[
    [0, 1, 0.5, 1], 
    [1, 0, 1, 1], 
    [1.5, 5, 0, 1], 
    [1, 1, 1, 0]
    ]# 距离矩阵
tabu_table={}# 禁忌表
tabu_tenure = 2# 禁忌期限
iterator = 10# 迭代次数控制

def cal_solve_distance(solve):
    """
    计算当前解的距离代价
    """
    result = 0
    for i in range(len(solve)):
        if i == len(solve)-1:
            result += location[solve[i]][0]
        else:
            result += location[solve[i]][solve[i+1]]
    return result

def search_tabu_table(a):
    """
    判断当前两个元素是否存在于禁忌表中
    """
    return not tabu_table.__contains__(a)


def neighbor_solve_set(solve):
    """
    根据当前的禁忌条件下生成对应的邻域解空间
    """
    result = []
    for i in range(1, len(solve)):
        for j in range(i+1, len(solve)):
            solve_new = solve[:]
            # 不存在于禁忌表中则生成新解
            if search_tabu_table((solve[i], solve[j])) and search_tabu_table((solve[j], solve[i])):
                solve_new[i], solve_new[j] = solve_new[j], solve_new[i]
                result.append(solve_new)
    return result 

def get_best_solve(solve_set):
    """
    从邻域解空间中获取效果最好的解
    """
    best_solve = solve_set[0]
    best_score = cal_solve_distance(best_solve)
    for i in range(1, len(solve_set)):
        solve = solve_set[i]
        score = cal_solve_distance(solve)
        if score < best_score:
            best_solve = solve
            best_score = score
    return best_solve

def set_tabu_table():
    """
    将禁忌表中所有元素的值减一，并将减为0的元素移除禁忌表
    """
    global tabu_table
    # 将所有元素减一
    for key in tabu_table.keys():
        tabu_table[key] -= 1
    # 将元素值为0的元素移除
    tabu_table_copy = dict(tabu_table)
    for key in tabu_table.keys():
        if tabu_table[key] == 0:
            tabu_table_copy.pop(key)
    tabu_table = tabu_table_copy

def find_change_elements(solve_a, solve_b):
    """
    寻找出两个解之间改变了的元素
    """
    result = []
    for i in range(len(solve_a)):
        if solve_a[i] != solve_b[i]:
            result.append(solve_a[i])
    return result[0], result[1]

# ============初始化============

# 初始解([0,1,2,3]表示a->b->c->d->a)
solve_i = list(range(num_city))
# 计算初始解所对应的距离
current_distance = cal_solve_distance(solve_i)
# 最优解
solve_best = solve_i
# 计算最优解所对应的距离
best_distance = cal_solve_distance(solve_best)
# 迭代次数
k = 0

# ============禁忌搜索============

while k < iterator:
    # 先将禁忌表中已有的元素减1
    set_tabu_table()
    # 构造当前解所对应的邻域并选择其中效果最好的解
    solve_set = neighbor_solve_set(solve_i)
    solve_j = get_best_solve(solve_set)
    # 更新禁忌表，找出更改了的两个元素，将其加入到禁忌表中
    element_a, element_b = find_change_elements(solve_i, solve_j)
    tabu_table[(element_a, element_b)] = tabu_tenure
    tabu_table[(element_b, element_a)] = tabu_tenure
    # 选择最优解
    solve_i = solve_j
    current_distance = cal_solve_distance(solve_i)
    if current_distance < best_distance:
        solve_best = solve_i
        best_distance = cal_solve_distance(solve_best)
    # 搜索结束，进入下一代搜索
    print("第%d次迭代结果：%s"%(k, str(solve_best)))
    k += 1

# 搜索结束，打印结果
print("最优解为：",solve_best)
print("最优解对应的价值：",cal_solve_distance(solve_best))
