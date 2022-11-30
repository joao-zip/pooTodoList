from src.entities.todoitem import TodoItem
from src.entities.user import User
from src.entities.todolist import TodoList
from src.entities.priority import Priority
import pytest
from src.entities.errors.duplicateditemerror import DuplicatedItem

def test_done():
    item = TodoItem('make bed', Priority.LOW)
    item.complete()
    assert item.is_done() == True

def test_undone():
    item = TodoItem('make bed', Priority.LOW)
    item.complete()
    item.undo()
    assert item.is_done() == False

def test_change_description():
    item = TodoItem('make bed', Priority.LOW)
    item.change_description('change bed')
    assert item.description == 'change bed'

def test_one_todo_list():
    owner = User('Joe Doe', 'joe@doe.com', '1234')
    list = TodoList(owner)
    item = TodoItem('make bed', Priority.LOW)
    list.add(item)
    assert list.get(0) == item
    assert list.get_owner() == owner

def test_complete_item_from_todo_list():
    owner = User('Joe Doe', 'joe@doe.com', '1234')
    list = TodoList(owner)
    item = TodoItem('make bed', Priority.LOW)
    list.add(item)
    list.complete_item(0)
    assert item.is_done() == True

def test_remove_item_from_todo_list():
    owner = User('Joe Doe', 'joe@doe.com', '1234')
    list = TodoList(owner)
    item = TodoItem('make bed', Priority.LOW)
    list.add(item)
    list.remove(0)
    assert list.size() == 0

def test_search_item_by_description():
    owner = User('Joe Doe', 'joe@doe.com', '1234')
    list = TodoList(owner)
    item1 = TodoItem('make bed', Priority.LOW)
    item2 = TodoItem('withdraw cash', Priority.LOW)
    list.add(item1)
    list.add(item2)
    assert list.find('withdraw cash') == item2

def test_items_sorted_by_priority():
    item1 = TodoItem('make bed', Priority.LOW)
    item2 = TodoItem('withdraw cash', Priority.MEDIUM)
    item3 = TodoItem('call mom', Priority.HIGH)
    owner = User('Joe Doe', 'joe@doe.com', '1234')
    list = TodoList(owner)
    list.add(item1)
    list.add(item2)
    list.add(item3)
    assert list.get(0).description == item3.description
    assert list.get(1).description == item2.description
    assert list.get(2).description == item1.description

def test_change_priority_resorts():
    item1 = TodoItem('make bed', Priority.LOW)
    item2 = TodoItem('withdraw cash', Priority.MEDIUM)
    item3 = TodoItem('call mom', Priority.HIGH)
    owner = User('Joe Doe', 'joe@doe.com', '1234')
    list = TodoList(owner)
    list.add(item1)
    list.add(item2)
    list.add(item3)
    list.change_priority(0, Priority.LOW)
    list.change_priority(2, Priority.HIGH)
    assert list.get(0).description == item1.description
    assert list.get(1).description == item2.description
    assert list.get(2).description == item3.description

def test_should_not_have_two_items():
    item1 = TodoItem('make bed', Priority.LOW)
    item2 = TodoItem('make bed', Priority.MEDIUM)
    owner = User('Joe Doe', 'joe@doe.com', '1234')
    list = TodoList(owner)
    list.add(item1)
    with pytest.raises(DuplicatedItem):
        list.add(item2)

def test_change_description_in_todolist():
    item1 = TodoItem('make bed', Priority.LOW)
    item2 = TodoItem('withdraw cash', Priority.MEDIUM)
    item3 = TodoItem('call mom', Priority.HIGH)
    owner = User('Joe Doe', 'joe@doe.com', '1234')
    list = TodoList(owner)
    list.add(item1)
    list.add(item2)
    list.add(item3)
    list.change_description('make bed', 'clean bedroom')
    assert list.find('clean bedroom') != None
    assert list.find('make bed') == None

def test_change_description_in_todolist_duplicate_item():
    item1 = TodoItem('make bed', Priority.LOW)
    item2 = TodoItem('withdraw cash', Priority.MEDIUM)
    item3 = TodoItem('call mom', Priority.HIGH)
    owner = User('Joe Doe', 'joe@doe.com', '1234')
    list = TodoList(owner)
    list.add(item1)
    list.add(item2)
    list.add(item3)
    with pytest.raises(DuplicatedItem):
        list.change_description('make bed', 'call mom')

def test_complete_item_goes_to_end_of_list():
    item1 = TodoItem('make bed', Priority.LOW)
    item2 = TodoItem('withdraw cash', Priority.MEDIUM)
    item3 = TodoItem('call mom', Priority.HIGH)
    owner = User('Joe Doe', 'joe@doe.com', '1234')
    list = TodoList(owner)
    list.add(item1)
    list.add(item2)
    list.add(item3)
    list.complete_by_description('call mom')
    assert item3.is_done() == True
    assert list.list[2] == item3

def test_complete_item_goes_to_end_of_list_2():
    item1 = TodoItem('make bed', Priority.LOW)
    item2 = TodoItem('withdraw cash', Priority.MEDIUM)
    item3 = TodoItem('call mom', Priority.HIGH)
    owner = User('Joe Doe', 'joe@doe.com', '1234')
    list = TodoList(owner)
    list.add(item1)
    list.add(item2)
    list.add(item3)
    list.complete_item(0)
    assert item3.is_done() == True
    assert list.list[2] == item3