from abc import ABC


class Repo(ABC):
    def create_exercise(self):
        raise NotImplementedError

    def update_exercise(self):
        raise NotImplementedError
