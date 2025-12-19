from collections import deque

class Stack:
    def __init__(self, array=None):
        self._data = array if array is not None else []
    
    def push(self, item):
        """Добавить элемент в стек"""
        self._data.append(item)
    
    def pop(self):
        """Удалить и вернуть верхний элемент"""
        if self.is_empty():
            raise IndexError("Нельзя удалить из пустого стека")
        return self._data.pop()
    
    def peek(self):
        """Посмотреть верхний элемент без удаления"""
        if self.is_empty():
            return None
        return self._data[-1]
    
    def is_empty(self):
        """Проверить, пуст ли стек"""
        return len(self._data) == 0
    
    def __len__(self):
        """Вернуть количество элементов"""
        return len(self._data)
    
    def __str__(self):
        """Строковое представление стека"""
        return str(self._data)


class Queue:
    def __init__(self, array=None):
        self._data = deque(array if array is not None else [])
    
    def enqueue(self, item):
        """Добавить элемент в очередь"""
        self._data.append(item)
    
    def dequeue(self):
        """Удалить и вернуть первый элемент"""
        if self.is_empty():
            raise IndexError("Нельзя удалить из пустой очереди")
        return self._data.popleft()
    
    def peek(self):
        """Посмотреть первый элемент без удаления"""
        if self.is_empty():
            return None
        return self._data[0] 
    
    def is_empty(self):
        """Проверить, пуста ли очередь"""
        return len(self._data) == 0
    
    def __len__(self):
        """Вернуть количество элементов"""
        return len(self._data)
    
    def __str__(self):
        """Строковое представление очереди"""
        return str(list(self._data))


if __name__ == '__main__':
    print("Тестирование")
    s = Stack()
    s.push(8)
    print(f"Удален из стека: {s.pop()}")
    print(f"Просмотр пустого стека: {s.peek()}")
    print(f"Длина стека: {len(s)}")
    print(f"Стек пуст? {s.is_empty()}")
    que = Queue()
    que.enqueue(4)
    print(f"Удален из очереди: {que.dequeue()}")
    print(f"Просмотр пустой очереди: {que.peek()}")
    print(f"Длина очереди: {len(que)}")
    print(f"Очередь пуста? {que.is_empty()}")