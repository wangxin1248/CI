import SA


# 今天日期
day = 1


def read_data():
    """
    从文件中读取测试数据
    :return:
    """
    order_list = []
    order_money = []
    with open('data/data.txt', 'r') as f:
        data = f.readlines()
        for i in range(len(data)):
            data_list = data[i].split(' ')
            # 获取订单金额
            order_money.append(int(data_list[-1]))
            # 添加订单到订单队列中
            list_temp = []
            for j in range(len(data_list)):
                list_temp.append(int(data_list[j]))
            order_list.append(list_temp)
    return order_list, order_money


def select_today(order_list):
    """
    从订单队列中获取今天要处理的订单信息
    今天要处理的订单信息包括：
        今天开始的订单
        之前未完成的订单
    :return:
    """
    today_order = []
    today_money = {}
    for order in order_list:
        # 今天要处理的订单添加之前还未处理完以及今天开始需要处理的订单
        if int(order[4]) <= day:
            if int(order[1]) != 0:
                today_order.append([int(order[0]), 1, int(order[1])])
                money = int((int(order[-1]) * 0.5) / int(order[1]))
                today_money[(int(order[0]), 1)] = money

            if int(order[2]) != 0:
                today_order.append([int(order[0]), 2, int(order[2])])
                money = int((int(order[-1])*0.3)/int(order[2]))
                today_money[(int(order[0]), 2)] = money

            if int(order[3]) != 0:
                today_order.append([int(order[0]), 3, int(order[3])])
                money = int((int(order[-1])*0.2)/int(order[3]))
                today_money[(int(order[0]), 3)] = money
    return today_order, today_money


def update_order(result, order_list, order_money, today_order):
    """
    根据当前的订单生产结果更新订单队列
    :param result:
    :param order_list:
    :param order_money:
    :param today_order:
    :return:
    """
    for i in range(9):
        if result[i] == -1:
            continue
        order_id = today_order[result[i]][0]
        order_num = today_order[result[i]][1]
        for m in range(len(order_list)):
            if order_list[m][0] == order_id:
                if order_list[m][order_num] > 0:
                    order_list[m][order_num] -= 1
                else:
                    order_list[m][order_num] = 0

    # 有订单被处理完删除该订单
    for data in order_list:
        if data[1] == 0 and data[2] == 0 and data[3] == 0:
            # 逾期订单，罚款处理
            if data[5] < day:
                order_money[data[0]] -= int(order_money[data[0]]*0.1)
            order_list.remove(data)
    for data in order_list:
        if data[1] == 0 and data[2] == 0 and data[3] == 0:
            # 逾期订单，罚款处理
            if data[5] < day:
                order_money[data[0]] -= int(order_money[data[0]]*0.1)
            order_list.remove(data)


def update_lost(result, order_money, today_order):
    """
    根据当前的订单生产结果更新订单消耗成本列表
    :param result:
    :param order_money:
    :param today_order:
    :return:
    """
    for i in range(9):
        if i < 6:
            if result[i] != -1 and today_order[result[i]][1] == 1:
                order_money[today_order[result[i]][0]] -= 500
            if result[i] != -1 and today_order[result[i]][1] == 2:
                order_money[today_order[result[i]][0]] -= 400
            if result[i] != -1 and today_order[result[i]][1] == 3:
                order_money[today_order[result[i]][0]] -= 300
        else:
            if result[i] != -1 and today_order[result[i]][1] == 1:
                order_money[today_order[result[i]][0]] -= 600
            if result[i] != -1 and today_order[result[i]][1] == 2:
                order_money[today_order[result[i]][0]] -= 500
            if result[i] != -1 and today_order[result[i]][1] == 3:
                order_money[today_order[result[i]][0]] -= 400


def main():
    # 读取订单数据,订单总金额列表
    order_list, order_money = read_data()
    # 当订单队列不为空的时候按天数进行订单处理
    while len(order_list) > 0:
        global day
        # 选取今天的订单组成订单矩阵
        today_order, today_money = select_today(order_list)
        # 对今天的订单矩阵进行优化调度
        sa = SA.SA(today_order, today_money)
        result = sa.slove()
        print('%s天调度结果:%s' % (str(day), str(result)))
        # 根据调度处理更新订单队列
        update_order(result, order_list, order_money, today_order)
        print('%s天调度结束后订单队列:%s' % (str(day), str(order_list)))
        # 根据调度结果更新订单消耗成本
        update_lost(result, order_money, today_order)
        # 天数加一
        day += 1

    # 计算最终收益
    total_money = 0
    for i in range(len(order_money)):
        total_money += order_money[i]
    print("最终利益为：%d" % total_money)


if __name__ == '__main__':
    main()

