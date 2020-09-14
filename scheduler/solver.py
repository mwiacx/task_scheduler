""" z3 slover """

import time
import z3
import typing
import re

from scheduler import strategies


class Slover:
    """ slover class """

    def __init__(self):
        self._solver = z3.Optimize()
        self._strategies = strategies.default_strategies()
        # z3 vars
        self._vars = {}

    def __build_vars(self, model):
        '''build solver vars'''
        # obj
        self._vars["min"] = z3.Real("min")
        # task start time and assinger vars
        for _, task in model.tasks.items():
            _var_name = "{}_start".format(task.name)
            self._vars[_var_name] = z3.Int(_var_name)
            _var_name = "{}_assigner".format(task.name)
            self._vars[_var_name] = z3.Int(_var_name)

    def __build_constraints(self, model):
        '''build constraints'''
        # setup strategy constraints
        for strategy in self._strategies:
            strategy.constraints(self._solver, self._vars, model)
        # set objctive
        for _, task in model.tasks.items():
            _task_start = self._vars["{}_start".format(task.name)]
            _task_length = task.length
            self._solver.add(self._vars["min"] >= _task_start + _task_length)
        self._solver.minimize(self._vars["min"])

    def set_strategies(self, strategy_strings):
        self._strategies = strategies.get_strategies(strategy_strings)

    def solve(self, model):
        self.__build_vars(model)
        self.__build_constraints(model)

        res = self._solver.check()

        if res != z3.sat:
            return False

        return True

    def parse_result(self, model):
        # get z3 model
        z3_model = self._solver.model()
        #
        for _var_name, _var in self._vars.items():
            if _var_name == "min":
                _fraction = z3_model[self._vars["min"]].as_fraction()
                _numerator = _fraction.numerator
                _denominator = _fraction.denominator
                if _numerator % _denominator == 0:
                    model._min = _numerator // _denominator
                else:
                    model._min = _numerator // _denominator + 1
                continue
            _res = re.search(r'_start$', _var_name)
            if _res != None:
                _index, _ = _res.span()
                _task_name = _var_name[:_index]
                model.tasks[_task_name].start_time = int(
                    str(z3_model.get_interp(_var)))
                continue
            _res = re.search(r'_assigner$', _var_name)
            if _res != None:
                _index, _ = _res.span()
                _task_name = _var_name[:_index]
                _person_index = int(str(z3_model.get_interp(_var)))
                model.tasks[_task_name].assigner = model.get_assigner(
                    _person_index).name
                continue
            print('Warnning(solver.parse_result): unknown z3 var: {}'.format(_var_name))
