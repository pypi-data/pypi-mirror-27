from collections import deque


# Object that allows traversal through a queue without modifying it.
class QueueIter:

    def __init__(self, queue, index: int = 0):

        self.queue = queue
        self.index = index

    def is_empty(self):

        return self.index >= len(self.queue)

    def dequeue(self):

        item = self.queue[self.index]
        self.index += 1
        return item

    def requeue(self):

        self.index -= 1
        item = self.queue[self.index]
        return item


class Queue(deque):

    def __init__(self, iterable=[], maxlen=None):
        super().__init__(iterable, maxlen)

    def __str__(self):
        return "\n\n".join(element.__str__() for element in self) if self else None.__str__()

    def is_empty(self):
        return len(self) == 0

    def enqueue(self, element):
        self.append(element)
        return self

    def dequeue(self):
        return self.popleft()

    def first(self):
        return self[0]

    def last(self):
        return self[-1]

    # Creates an interator object that allows queue-like traversal through the current Queue without modifying it.
    def iter(self, index: int = 0):

        return QueueIter(self, index)
