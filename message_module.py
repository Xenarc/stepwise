from signal import Signal
from module import Module
from typing import TypeVar, Generic

T = TypeVar("T")


class MessageModule(Module):
    def __init__(self):
        super().__init__()
        self.msg: Signal[T | None] = self.signal(None)
        self._message_hooks = []

    def on_message(self, fn):
        """Register a function to run on message arrival."""
        self._message_hooks.append(fn)
        return fn

    def process_message(self, msg: T):
        print(f"[MessageModule] Received: {msg}")
        self.msg.set(msg)
        self.step()
        self.msg.update()
        for hook in self._message_hooks:
            hook(msg)
