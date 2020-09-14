''' strategies for solver '''

import z3


def get_strategies(strategies):
    _strategies = {
        "LimitRange": LimitRangeStrategy(),
        "Dependency": DependencyStrategy(),
        "NonOverlapping": NonOverlappingStrategy(),
        "EnergyLimit": EnergyLimitStrategy(),
        "Review": ReviewStrategy(),
    }
    res = []
    for s in strategies:
        res.append(_strategies[s])
    return set(res)


def default_strategies():
    return set([LimitRangeStrategy(), DependencyStrategy(),
                NonOverlappingStrategy(), EnergyLimitStrategy(),
                ReviewStrategy()])


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
        for _, task in model.tasks.items():
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
            _task_assigner = vars["{}_assigner".format(task.name)]
            if task.start_time != None:
                solver.add(_task_start == task.start_time)
            else:
                solver.add(_task_start >= 0)
            if task.assigner != None:
                solver.add(_task_assigner ==
                           model.get_assigner_id(task.assigner))
            else:
                solver.add(_task_assigner >= 0)
                solver.add(_task_assigner < _members)
                if task.task_type == "review1":
                    _ids = [x for x in range(_members)]
                    for _review1 in model.first_reviewers():
                        _ids.remove(model.get_assigner_id(_review1.name))
                    for _id in _ids:
                        solver.add(_task_assigner != _id)
                elif task.task_type == "review2":
                    _ids = [x for x in range(_members)]
                    for _review2 in model.final_reviewers():
                        _ids.remove(model.get_assigner_id(_review2.name))
                    for _id in _ids:
                        solver.add(_task_assigner != _id)
                elif task.task_type == "normal":
                    pass
                else:
                    assert(False)


class NonOverlappingStrategy(Strategy):
    ''' non-overlapping strategy class '''

    def __init__(self):
        super().__init__("non-overlapping strategy")

    def constraints(self, solver, vars, model):
        visited = {}
        for _, _task1 in model.tasks.items():
            for _, _task2 in model.tasks.items():
                if _task2.name == _task1.name or "{}_{}".format(_task1.name, _task2.name) in visited.keys():
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
                visited["{}_{}".format(_task1.name, _task2.name)] = True
                visited["{}_{}".format(_task2.name, _task1.name)] = True
        visited = {}


class EnergyLimitStrategy(Strategy):
    ''' energy limit strategy '''

    def __init__(self):
        super().__init__("energy limit strategy")

    def constraints(self, solver, vars, model):
        for _person_name, _person in model.persons.items():
            _cost_time = 0
            for _, _task in model.tasks.items():
                _cost_time += z3.If(
                    vars["{}_assigner".format(_task.name)] == model.get_assigner_id(
                        _person_name), _task.length, 0)
            #solver.add(vars["min"] >= _cost_time * (1 / _person.energy))
            solver.add(vars["min"] / (1 / _person.energy) >= _cost_time)


class ReviewStrategy(Strategy):
    ''' review task strategy '''

    def __init__(self):
        super().__init__("review task strategy")

    def constraints(self, solver, vars, model):
        for _, _task in model.tasks.items():
            if _task.task_type != "review1" and _task.task_type != "review2":
                continue
            assert(_task._parent in model.tasks.keys())
            _parent = model.tasks[_task._parent]
            assert(_parent.assigner != None)
            # constraints
            _task_assinger = vars["{}_assigner".format(_task.name)]
            solver.add(_task_assinger !=
                       model.get_assigner_id(_parent.assigner))
