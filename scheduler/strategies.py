''' strategies for solver '''

import z3


def get_strategies(strategies):
    _strategies = {
        "LimitRange": LimitRangeStrategy(),
        "Dependency": DependencyStrategy(),
        "NonOverlapping": NonOverlappingStrategy(),
    }
    res = []
    for s in strategies:
        res.append(_strategies[s])
    return set(res)


def default_strategies():
    return set([LimitRangeStrategy(), DependencyStrategy(), NonOverlappingStrategy()])


class Strategy:
    ''' strategy class '''

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class DependencyStrategy(Strategy):
    ''' dependency strategy class '''

    def __init__(self):
        super().__init__("dependency strategy")

    def constraints(self, solver, vars, model):
        for task in model.tasks:
            if len(task.dependencies) == 0:
                continue
            for dtask in task.dependencies:
                _task_start = vars["{}_start".format(task.name)]
                _dtask_start = vars["{}_start".format(dtask.name)]
                _dtask_length = dtask.length
                solver.add(_task_start >= _dtask_start + _dtask_length)


class LimitRangeStrategy(Strategy):
    ''' limit range strategy class '''

    def __init__(self):
        super().__init__("limit range stractegy")

    def constraints(self, solver, vars, model):
        _members = len(model.persons)
        for _, task in model.tasks.items():
            _task_start = vars["{}_start".format(task.name)]
            solver.add(_task_start >= 0)
            if task.assigner == "":
                _task_assigner = vars["{}_assigner".format(task.name)]
                solver.add(_task_assigner >= 0)
                solver.add(_task_assigner < _members)


class NonOverlappingStrategy(Strategy):
    ''' non-overlapping strategy class '''

    def __init__(self):
        super().__init__("non-overlapping strategy")

    def constraints(self, solver, vars, model):
        for i in range(len(model.tasks)):
            _task1 = model.tasks[i]
            if _task1.assigner != "":
                continue
            for j in range(i+1, len(model.tasks)):
                _task2 = model.tasks[j]
                if _task2.assigner != "":
                    continue
                #
                _task1_start = vars["{}_start".format(_task1.name)]
                _task1_length = _task1.length
                _task1_assinger = vars["{}_assigner".format(_task1.name)]
                _task2_start = vars["{}_start".format(_task2.name)]
                _task2_length = _task2.length
                _task2_assinger = vars["{}_assigner".format(_task2.name)]
                solver.add(z3.If(
                    _task1_assinger == _task2_assinger,
                    z3.Or((_task1_start >= _task2_start + _task2_length),
                          (_task2_start >= _task1_start + _task1_length)),
                    True))
