
class Stack:

    def __init__(self, iterable_list = []):
        self.__storage = iterable_list

    def __str__(self):
        return "\n\n".join(element.__str__() for element in self.__storage) if self.__storage else None.__str__()

    def is_empty(self):
        return len(self.__storage) == 0

    def push(self, data):
        self.__storage.append(data)
        return self

    def pop(self):
        return self.__storage.pop()

    def peek(self):
        return self.__storage[-1]

    def reverse(self):
        self.__storage = self.__storage[::-1]
        return self

    def reversed(self):
        return Stack(self.__storage[::-1])

    def to_list(self):
        return self.__storage
