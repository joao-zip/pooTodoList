from abc import ABC, abstractmethod

class TodoListRepository(ABC):
    @abstractmethod
    def add(self, todo_list):
        raise (NotImplementedError)

    @abstractmethod
    def find_by_email(self, user_email):
        raise (NotImplementedError)