"""scheduler models"""

from enum import Enum


class Model:
    """schedule model"""

    def __init__(self, solver):
        self._solver = solver
        self._persons = {}
        self._tasks = {}
        self._assigner_map = {}

    @property
    def persons(self):
        return self._persons

    @persons.setter
    def persons(self, persons):
        count = 0
        for _p in persons:
            self._persons[_p.name] = _p
            self._assigner_map[count] = _p.name
            count += 1

    @property
    def tasks(self):
        return self._tasks

    @tasks.setter
    def tasks(self, tasks):
        for _t in tasks:
            self._tasks[_t.name] = _t

    def first_reviewers(self):
        res = []
        for person in self._persons:
            if person.is_first_reviewer:
                res.append(person)
        return res

    def final_reviewers(self):
        res = []
        for person in self._persons:
            if person.is_final_reviewer:
                res.append(person)
        return res

    def get_assigner(self, id):
        _name = self._assigner_map[id]
        return self._persons[_name]

    def get_assigner_id(self, name):
        _map = self._assigner_map
        return list(_map.keys())[list(_map.values()).index(name)]

    def solve(self):
        self._solver.solve(self)
        self._solver.parse_result(self)

    def draw(self):
        pass


class Person:
    """staff members"""

    def __init__(self, name, energy, is_first_reviewer=False, is_final_reviewer=False):
        assert(energy >= 0 and energy <= 1)
        self._name = name
        self._energy = energy
        self._is_first_reviewer = is_first_reviewer
        self._is_final_reviewer = is_final_reviewer

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, energy):
        self._energy = energy

    @property
    def is_first_reviewer(self):
        return self._is_first_reviewer

    @is_first_reviewer.setter
    def is_first_reviewer(self, is_first_reviewer):
        self._is_first_reviewer = is_first_reviewer

    @property
    def is_final_reviewer(self):
        return self._is_final_reviewer

    @is_final_reviewer.setter
    def is_final_reviewer(self, is_final_reviewer):
        self._is_final_reviewer = is_final_reviewer


class Task:
    """task class"""

    def __init__(self, name, length, assigner=""):
        self._name = name
        self._length = length
        self._assigner = assigner
        self._dependencies = []

    def __str__(self):
        return "Task<name: {}, start: {}, length: {}, assigner: {}>".format(
            self.name, self.start_time, self.length, self.assigner)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def task_type(self):
        return self._task_type

    @task_type.setter
    def task_type(self, task_type):
        self._task_type = task_type

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        self._length = length

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @property
    def finish_time(self):
        return self._finish_time

    @finish_time.setter
    def finish_time(self, finish_time):
        self._finish_time = finish_time

    @property
    def assigner(self):
        return self._assigner

    @assigner.setter
    def assigner(self, assigner):
        self._assigner = assigner

    @property
    def dependencies(self):
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies):
        self._dependencies = dependencies
