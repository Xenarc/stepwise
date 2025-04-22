from signal import Signal


class Module:
    def __init__(self):
        self._signals = []
        self._logic_blocks = []
        self._submodules = []

        # Register signal/logic from child class
        self._init_submodules()

    def signal(self, initial=0):
        sig = Signal(initial)
        self._signals.append(sig)
        return sig

    def submodule(self, mod):
        self._submodules.append(mod)
        return mod

    def _init_submodules(self):
        for attr in dir(self):
            member = getattr(self, attr)
            if isinstance(member, Module):
                self._submodules.append(member)

    def always(self, fn):
        self._logic_blocks.append(fn)
        return fn

    def step(self):
        # Evaluate logic in self
        for logic in self._logic_blocks:
            logic()
        # Propagate to submodules
        for sub in self._submodules:
            sub.step()
        # Update all signals (self only)
        for s in self._signals:
            s.update()
