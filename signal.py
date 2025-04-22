from typing import TypeVar, Generic

T = TypeVar("T")


class Signal(Generic[T]):
    def __init__(self, initial: T):
        self.value: T = initial
        self.next: T = initial

    def set(self, val):
        self.next = val

    def update(self):
        self.value: T = self.next

    def __call__(self) -> T:
        return self.value
