# 计算智能(Computational Intelligence, CI)

## 算法列表

- 蚁群系统（Ant System，AS）
- 模拟退火（Simulated Annealing, SA）
- 禁忌搜索（Tabu Search, TS）

## 大作业

生产调度(JSP)问题

### 目标
调度所有订单的生产顺序，要求实现利润的最大化
### 要求
1. 总共有三条生产线，可以生产123三种类型的产品；
2. 三条产品线都可以生产3种类型的产品；
3. 一天的工作量分为正常上班时间以及加班时间；
4. 正常上班时间为上午4个小时，下午4个小时，加班时间为晚上4个小时；
5. 所有订单中的生产产品以4小时为单位，所有价格的单位为元；
6. 产品1每单位消耗成本为500，产品2每单位消耗成本为400，产品3每单位消耗成本为300；
7. 加班情况下产品1每单位消耗成本为600，产品2每单位消耗成本为500，产品3每单位消耗成本为400；
8. 订单金额包含订单中所有产品的钱，其中按照权重不同划分为不同的产品；
9. 产品1订单金额占比为50%，产品2占比30%，产品3占比20%；
8. 订单超时需要支付订单总金额的10%的罚金；
9. 订单时间用数字表示，单位为天；
10. 所有计算按整数向下取整；

### 订单格式

```
[订单编号,产品1生产数目,产品2生产数目,产品3生产数目,开始时间,结束时间,金额]
```
### 测试数据

```
0 10 20 30 1 40 32000
1 20 10 10 1 50 22000
2 10 0 7 1 30 17000
3 30 5 12 1 56 31000
4 16 12 0 1 52 35000
5 0 20 30 2 60 40000
6 20 13 6 2 59 44000
7 2 4 5 3 46 28000
8 3 4 5 4 60 27000
9 13 15 12 5 62 40000
10 20 34 10 6 70 50000
11 13 34 10 7 65 34000
12 23 3 5 8 50 38000
```
