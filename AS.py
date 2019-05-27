# 蚁群优化算法求解TSP问题
import random
import math
import numpy as np

location=[
    [-1,3,1,2],
    [3,-1,5,4],
    [1,5,-1,2],
    [2,4,2,-1]
]# 城市距离矩阵
num_ant=3# 蚂蚁个数
num_city=4# 城市个数
alpha=1# 信息素影响因子
beta=2# 期望影响因子
p=0.5# 信息素的挥发率
Q=1 # 常数
count_iter = 0# 迭代次数计数器
iter_max = 100# 总共迭代次数


#计算两个城市之间的距离
def distance_p2p_mat():
    dis_mat=[]
    for i in range(num_city):
        dis_mat_each=[]
        for j in range(num_city):
            dis=math.sqrt(pow(location[i][0]-location[j][0],2)+pow(location[i][1]-location[j][1],2))
            dis_mat_each.append(dis)
        dis_mat.append(dis_mat_each)
    return dis_mat

#计算所有路径对应的距离
def cal_newpath(dis_mat,path_new):
    dis_list=[]
    for each in path_new:
        dis=0
        for j in range(num_city-1):
            dis=dis_mat[each[j]][each[j+1]]+dis
        dis=dis_mat[each[num_city-1]][each[0]]+dis
        dis_list.append(dis)
    return dis_list

# ============初始化============
#点对点距离矩阵
dis_list=distance_p2p_mat()
dis_mat=np.array(dis_list)#转为矩阵
#期望矩阵
e_mat_init=1.0/(dis_mat+np.diag([10000]*num_city))#加对角阵是因为除数不能是0
diag=np.diag([1.0/10000]*num_city)
e_mat=e_mat_init-diag#还是把对角元素变成0
#初始化每条边的信息素浓度，全1矩阵
pheromone_mat=np.ones((num_city,num_city))
#初始化每只蚂蚁路径，都从0城市出发
path_mat=np.zeros((num_ant,num_city)).astype(int)

# ============开始循环============
while count_iter < iter_max:
    # 每次一只蚂蚁去搜寻
    for ant in range(num_ant):
        #默认从0城市出发
        visit=0
        #记录未访问的城市
        un_visit_list=list(range(1,num_city))
        for j in range(1,num_city):
            #轮盘法选择下一个城市
            trans_list=[]
            tran_sum=0
            trans=0
            for k in range(len(un_visit_list)):
                trans +=np.power(pheromone_mat[visit][un_visit_list[k]],alpha)*np.power(e_mat[visit][un_visit_list[k]],beta)
                trans_list.append(trans)
                tran_sum =trans
            #产生随机数
            rand=random.uniform(0,tran_sum)

            for t in range(len(trans_list)):
                if(rand <= trans_list[t]):
                    visit_next=un_visit_list[t]
                    break
                else:
                    continue
            #填路径矩阵
            path_mat[ant,j]=visit_next
            #更新禁忌表
            un_visit_list.remove(visit_next)
            #更新该蚂蚁所要访问的下一个城市
            visit=visit_next

    #所有蚂蚁的路径表填满之后，算每只蚂蚁的总距离
    dis_allant_list=cal_newpath(dis_mat,path_mat)

    #每次迭代更新最短距离和最短路径        
    if count_iter == 0:
        dis_new=min(dis_allant_list)
        path_new=path_mat[dis_allant_list.index(dis_new)].copy()      
    else:
        if min(dis_allant_list) < dis_new:
            dis_new=min(dis_allant_list)
            path_new=path_mat[dis_allant_list.index(dis_new)].copy() 

    # 更新信息素矩阵
    pheromone_change=np.zeros((num_city,num_city))
    for i in range(num_ant):
        for j in range(num_city-1):
            pheromone_change[path_mat[i,j]][path_mat[i,j+1]] += Q/dis_mat[path_mat[i,j]][path_mat[i,j+1]]
        pheromone_change[path_mat[i,num_city-1]][path_mat[i,0]] += Q/dis_mat[path_mat[i,num_city-1]][path_mat[i,0]]
    pheromone_mat=(1-p)*pheromone_mat+pheromone_change
    
    #迭代计数+1，进入下一次
    count_iter += 1 


print('最优解：',path_new)      
print('最优解对应的距离：',dis_new)
