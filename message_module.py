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
