from src.entities.errors.duplicateditemerror import DuplicatedItem
from src.usecases.errors.invalidusererror import InvalidUserError

class TodoList:
    def __init__(self, owner):
        self.owner = owner
        self.list = []

    def add(self, item):
        if self.find(item.description) != None:
            raise DuplicatedItem()
        self.list.append(item)
        self.sort()

    def get(self, index):
        return self.list[index]

    def get_owner(self):
        return self.owner

    def complete_item(self, index):
        self.list[index].complete()
        self.sort()

    def complete_by_description(self, item_description):
        item = self.find(item_description)
        if item:
            item.complete()
            self.sort()

    def remove(self, index):
        self.list.pop(index)

    def size(self):
        return len(self.list)

    def find(self, description):
        for item in self.list:
            if item.description == description:
                return item

    def sort(self):
        self.list.sort()

    def change_priority(self, index, new_priority):
        self.list[index].change_priority(new_priority)
        self.list.sort()

    def change_description(self,old_description, new_description):
        existing_item = self.find(new_description)
        if existing_item:
            raise DuplicatedItem()
        item = self.find(old_description)
        item.change_description(new_description)

    def show(self, owner):
        if owner != self.get_owner():
            raise InvalidUserError()
        else:
            for i in self.list:
                print(f'-> {i}')

