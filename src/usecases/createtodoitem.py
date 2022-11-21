from src.entities.todoitem import TodoItem
from src.usecases.errors.invalidusererror import InvalidUserError # Atividade dia 21

class CreateTodoItem:
    def __init__(self, user_repo, todolist_repo):
      self.user_repo = user_repo
      self.todolist_repo = todolist_repo

    def perform(self, user_email, item_description, item_priority):
      todolist = self.todolist_repo.find_by_email(user_email)
      todoitem = TodoItem(item_description, item_priority)
      if todolist == None : # Atividade dia 21
        raise InvalidUserError
      todolist.add(todoitem)
      self.todolist_repo.update(user_email, todolist) 