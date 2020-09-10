"""scheduler models"""


class Model:
    """schedule model"""

    def __init__(self):
        pass

    @property
    def persons(self):
        return self._persons

    @persons.setter
    def persons(self, persons):
        self._persons = persons

    @property
    def tasks(self):
        return self._tasks

    @tasks.setter
    def tasks(self, tasks):
        self._tasks = tasks

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

    def draw(self):
        pass


class Person:
    """staff members"""

    def __init__(self, is_first_reviewer, is_final_reviewer):
        self._is_first_reviewer = is_first_reviewer
        self._is_final_reviewer = is_final_reviewer

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
    """tasks"""

    def __init__(self, name, length, assigner=""):
        self._name = name
        self._length = length
        self._assigner = assigner
        self._dependencies = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

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
