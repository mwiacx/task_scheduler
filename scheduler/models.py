"""scheduler models"""

from enum import Enum


class Model:
    """schedule model"""

    def __init__(self, solver):
        self._solver = solver
        self._persons = {}
        self._tasks = {}
        self._assigner_map = {}
        self._min = 0

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
        for _, person in self._persons.items():
            if person.is_first_reviewer:
                res.append(person)
        return res

    def final_reviewers(self):
        res = []
        for _, person in self._persons.items():
            if person.is_final_reviewer:
                res.append(person)
        return res

    def get_assigner(self, aid):
        _name = self._assigner_map[aid]
        return self._persons[_name]

    def get_assigner_id(self, name):
        _map = self._assigner_map
        return list(_map.keys())[list(_map.values()).index(name)]

    def person_tasks(self, person_name):
        res = []
        for _, task in self._tasks.items():
            if task.assigner == person_name:
                res.append(task)
        return res

    def solve(self):
        success = self._solver.solve(self)
        if not success:
            return False
        self._solver.parse_result(self)
        # update finish time
        for _, task in self._tasks.items():
            task.finish_time = task.start_time + task.length - 1

        return True

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

    def __str__(self):
        return "Person<name: {}>".format(self.name)

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

    def __init__(self, name, length, task_type="normal", assigner=None, parent=None):
        assert(task_type == "normal" or task_type ==
               "review1" or task_type == "review2")
        self._name = name
        self._start_time = None
        self._length = length
        self._assigner = assigner
        self._dependencies = []
        self._task_type = task_type
        if self._task_type == "review1" or self._task_type == "review2":
            assert(parent != None)
            self._parent = parent
        elif self._task_type == "normal":
            assert(assigner != None)
        else:
            assert(0)

    def __str__(self):
        return "Task<name: {}, start: {}, deadline: {}, length: {}, assigner: {}>".format(
            self.name, self.start_time+1, self.finish_time+1, self.length, self.assigner)

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
        assert(task_type == "normal" or task_type ==
               "review1" or task_type == "review2")
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
