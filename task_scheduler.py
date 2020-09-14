from scheduler import solver
from scheduler import models


def test_model(solver):
    m = models.Model(solver)

    zhangsan = models.Person("zhangsan", 0.9, False, False)
    lisi = models.Person("lisi", 0.8, True, False)
    wangwu = models.Person("wangwu", 0.6, True, True)
    m.persons = [zhangsan, lisi, wangwu]

    '''
    zhangsan: task1 task2
    lisi: task3 task4
    wangwu:     task5
    '''
    task1 = models.Task("task1", 5)
    task2 = models.Task("task2", 7, task_type="normal", assigner="lisi")
    task3 = models.Task("task3", 3)
    task4 = models.Task("task4", 10, task_type="review1")
    task5 = models.Task("task5", 7, task_type="review1")
    task6 = models.Task("task6", 12, task_type="review2")

    task2.dependencies = [task1]
    task4.dependencies = [task3, task2, task6]
    task5.dependencies = [task1, task2, task3, task4, task6]

    m.tasks = [task1, task2, task3, task4, task5, task6]

    return m


if __name__ == '__main__':
    s = solver.Slover()
    s.set_strategies(["LimitRange", "Dependency",
                      "NonOverlapping", "EnergyLimit"])
    model = test_model(s)
    if not model.solve():
        print("Solve Failed")
    else:
        print("最小开发周期为：{}".format(model._min))
        print("任务排期如下：")
        for _, task in model._tasks.items():
            print(task)
