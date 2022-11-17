from src.usecases.ports.todolistrepository import TodoListRepository

class InMemoryTodoListRepository(TodoListRepository):
    def __init__(self):
        self.todolist = []

    def add(self, todolist):
        self.todolist.append(todolist)

    def find_by_email(self, email):
        for todolist in self.todolist:
            if todolist.owner.email == email:
                return todolist
