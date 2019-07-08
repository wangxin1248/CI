"""
模拟退火算法进行生产调度优化
"""
import random
import math
import copy


class SA(object):
    def __init__(self, today_order, today_money):
        # 迭代次数
        self.iteration = 500
        # 初始温度
        self.initial_t = 1000
        # 最低温度
        self.low_t = 0.1
        # 温度强制降低指标
        self.max = 300
        # 所要调度的任务个数
        self.n = len(today_order)
        # 今天所有生产的产品单位数
        num = 0
        for data in today_order:
            num += data[2]
        self.num = num
        # 今天所需要调度的任务列表
        self.today_order = today_order
        # 今天所需要处理的任务对应的金额
        self.today_money = today_money
        # 最优解
        self.best_slove = []

    def init_slove(self, n):
        """
        随机生成初始解并返回
        0-8 9个工位，从0开始安排订单，678可以选择不安排，值为-1
        :param n:
        :return:
        """
        # 今天要生产的产品单位数大于9则可以全安排进行生产
        if self.num > 6:
            # 订单是否符合要求
            flag = False
            while not flag:
                slove_i = []
                for i in range(9):
                    if i < 6:
                        index = random.randint(0, n - 1)
                        slove_i.append(index)
                    else:
                        # 可以选择是否加班
                        index = random.randint(-1, n - 1)
                        slove_i.append(index)
                # 检查订单是否符合要求
                flag = self.check_slove(slove_i)
            return slove_i
        else:
            # 只安排num数量的，其他的设置为-1，表示不工作
            # 订单是否符合要求
            flag = False
            while not flag:
                slove_i = []
                for i in range(9):
                    if i < self.num:
                        index = random.randint(0, n - 1)
                        slove_i.append(index)
                    else:
                        # 其他的生产工位不工作
                        slove_i.append(-1)
                # 检查订单是否符合要求
                flag = self.check_slove(slove_i)
            return slove_i

    def slove_money(self, slove):
        """
        获取当前解所能获取的利润
        :param slove:
        :return:
        """
        money = 0
        # 获取今天的产品订单金额
        for i in range(9):
            if i < 6 and self.num > 6:
                # 正常生产
                if self.today_order[slove[i]][1] == 1:
                    # 产品1
                    money += (self.today_money.get((self.today_order[slove[i]][0], 1)) - 500)
                elif self.today_order[slove[i]][1] == 2:
                    # 产品2
                    money += (self.today_money.get((self.today_order[slove[i]][0], 2)) - 400)
                else:
                    # 产品3
                    money += (self.today_money.get((self.today_order[slove[i]][0], 3)) - 300)
            elif self.num > 6 and i >= 6:
                # 加班生产
                if slove[i] != -1 and self.today_order[slove[i]][1] == 1:
                    # 产品1
                    money += (self.today_money.get((self.today_order[slove[i]][0], 1)) - 600)
                elif slove[i] != -1 and self.today_order[slove[i]][1] == 2:
                    # 产品2
                    money += (self.today_money.get((self.today_order[slove[i]][0], 2)) - 500)
                elif slove[i] != -1 and self.today_order[slove[i]][1] == 3:
                    # 产品3
                    money += (self.today_money.get((self.today_order[slove[i]][0], 3)) - 400)
            elif self.num < 6:
                # 正常生产
                if slove[i] != -1 and self.today_order[slove[i]][1] == 1:
                    # 产品1
                    money += (self.today_money.get((self.today_order[slove[i]][0], 1)) - 500)
                elif slove[i] != -1 and self.today_order[slove[i]][1] == 2:
                    # 产品2
                    money += (self.today_money.get((self.today_order[slove[i]][0], 2)) - 400)
                elif slove[i] != -1 and self.today_order[slove[i]][1] == 3:
                    # 产品3
                    money += (self.today_money.get((self.today_order[slove[i]][0], 3)) - 300)
        return money

    def get_slove(self, slove_i):
        """
        根据当前解生成新的邻域解
        :param slove_i:
        :return:
        """
        flag = False
        while not flag:
            slove_j = slove_i[:]
            i = 0
            j = 0
            while i == j:
                if self.num > 6:
                    i = random.randint(0, 8)
                    j = random.randint(0, 8)
                else:
                    i = random.randint(0, 6)
                    j = random.randint(0, 6)
            if self.num > 6:
                slove_j[i] = random.randint(0, self.n-1)
                slove_j[j] = random.randint(0, self.n-1)
            else:
                slove_j[i] = random.randint(-1, self.n-1)
                slove_j[j] = random.randint(-1, self.n-1)
            flag = self.check_slove(slove_j)
        return slove_j

    def check_slove(self, slove):
        """
        判断当前解是否满足要求
        :param slove:
        :return:
        """
        order = copy.deepcopy(self.today_order)
        for i in range(9):
            # 检查是否在全满工位上出现-1
            if slove[i] == -1 and self.num > 6 and i < 6:
                return False
            elif slove[i] != -1:
                # 检查同一订单被多次生产超标的问题
                order[slove[i]][2] -= 1
                if order[slove[i]][2] < 0:
                    return False
        return True

    def slove(self):
        """
        模拟退火处理
        :return:
        """
        slove_i = self.init_slove(self.n)
        self.best_slove = slove_i
        current_money = self.slove_money(slove_i)
        current_t = self.initial_t
        K = 0

        # ===========开始退火求解===========
        # 外循环，改变温度
        while current_t > self.low_t:
            # m计数器
            count_m = 0
            # 迭代次数计数器
            counter_iter = 0
            # 内循环，连续多次不接受新的状态或者迭代多次跳出
            while count_m < self.max and counter_iter < self.iteration:
                # 根据当前解生成一个邻域解
                slove_j = self.get_slove(slove_i)
                # 计算新解的价值
                money_j = self.slove_money(slove_j)
                if money_j > current_money:
                    # 新解较优，接受新解
                    slove_i = slove_j
                    current_money = money_j
                    self.best_slove = slove_j
                elif money_j < current_money:
                    # 新解较劣，按概率接受
                    probability = math.exp((money_j - current_money) / self.initial_t)
                    random_i = random.random()
                    if random_i < probability:
                        slove_i = slove_j
                        current_money = money_j
                        self.best_slove = slove_j
                else:
                    count_m += 1
                counter_iter += 1
            # 降温
            K += 1
            current_t = current_t/math.log2(1+K)

        return self.best_slove
