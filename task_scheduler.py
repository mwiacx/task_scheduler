from scheduler import solver
from scheduler import models


def test_model(solver):
    m = models.Model(solver)

    zhangsan = models.Person(False, False)
    lisi = models.Person(True, False)
    wangwu = models.Person(True, True)
    m.persons = [zhangsan, lisi, wangwu]

    '''
    zhangsan: task1 task2
    lisi: task3 task4
    wangwu:     task5
    '''
    task1 = models.Task("task1", 5)
    task2 = models.Task("task2", 7)
    task3 = models.Task("task3", 3)
    task4 = models.Task("task4", 10)
    task5 = models.Task("task5", 7)
    task6 = models.Task("task6", 12)

    task2.dependencies = [task1]
    task4.dependencies = [task3, task2, task6]
    task5.dependencies = [task1, task2, task3, task4, task6]

    m.tasks = [task1, task2, task3, task4, task5, task6]

    return m


if __name__ == '__main__':
    s = solver.Slover()
    s.set_strategies(["LimitRange", "Dependency", "NonOverlapping"])
    model = test_model(s)
    model.solve()
    for task in model.tasks:
        print(task)
