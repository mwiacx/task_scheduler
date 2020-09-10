""" z3 slover """

import time
import z3
import typing
from scheduler import strategies


class Slover:
    """ slover class """

    def __init__(self, model):
        self._solver = z3.Optimize()
        self._model = model
        self._vars = self.__build_var()

    def __build_var(self):
        '''build solver vars'''
        _vars = {}
        # obj var
        _vars['min'] = z3.Int('min')
        # task start time and assinger vars
        for task in self._model.tasks:
            _var_name = "{}_start".format(task.name)
            _vars[_var_name] = z3.Int(_var_name)
            if task.assigner == "":
                _var_name = "{}_assigner".format(task.name)
                _vars[_var_name] = z3.Int(_var_name)

        return _vars

    def __build_constraints(self):
        '''build constraints'''

        for strategy in self._strategies:
            strategy.constraints(self._solver, self._vars, self._model)

        # set objctive
        _min = self._vars["min"]
        for task in self._model.tasks:
            _task_start = self._vars["{}_start".format(task.name)]
            _task_length = task.length
            self._solver.add(_min >= _task_start + _task_length)
        h = self._solver.minimize(_min)
        return h

    def set_strategies(self, strategy_strings):
        self._strategies = strategies.get_strategies(strategy_strings)

    def slove(self):
        self.__build_constraints()

        res = self._solver.check()

        if res != z3.sat:
            print(res)
            return None

        model = self._solver.model()

        return model
