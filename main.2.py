import random
import time
from module import Module


class Message:
    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b

    def __repr__(self):
        return f"Message(a={self.a}, b={self.b})"


class MessageModule(Module):
    def __init__(self):
        super().__init__()
        self.msg = self.signal({})
        self._message_hooks = []

    def on_message(self, fn):
        """Register a function to run on message arrival."""
        self._message_hooks.append(fn)
        return fn

    def process_message(self, msg: dict):
        print(f"[MessageModule] Received: {msg}")
        self.msg.set(msg)
        self.step()
        self.msg.update()
        for hook in self._message_hooks:
            hook(msg)


class Top(Module):
    def __init__(self):
        super().__init__()
        self.messages = self.submodule(MessageModule())
        self.sum_out = self.signal(0)
        self.message_count = self.signal(0)

        self.always(self.run)

        @self.messages.on_message
        def handle_msg(msg: Message):
            self.validate_message(msg)

    def validate_message(self, msg: Message):
        if not isinstance(msg, Message):
            raise ValueError("Message must be an instance of the Message class")

    def run(self):
        msg = self.messages.msg()
        a = msg.a  # Access 'a' directly from the Message class
        b = msg.b  # Access 'b' directly from the Message class
        self.sum_out.set(a + b)
        self.message_count.set(self.message_count() + 1)


def main():
    top = Top()

    for msg in [
        Message(a=1, b=2),
        Message(a=10, b=5),
        Message(a=3, b=7),
    ]:
        try:
            top.messages.process_message(msg)
            top.step()
            print(f"→ msg={msg} ⇒ sum_out={top.sum_out()}, count={top.message_count()}")
            time.sleep(0.8)
        except Exception as e:
            print(f"✖ Error: {e}")


if __name__ == "__main__":
    main()
