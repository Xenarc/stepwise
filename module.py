from typing import List, Callable, Tuple, Any
from signal import Signal


class Module:
    def __init__(self):
        self._signals = []
        self._always_blocks = []
        self._always_on_blocks: List[Tuple[Callable[[Any], Any], List[Signal]]] = []
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

    def always(self, fn: Callable[[Any], Any]):
        self._always_blocks.append(fn)
        return fn

    def always_on(self, fn: Callable[[Any], Any], when_signals: List[Signal]):
        self._always_on_blocks.append((fn, when_signals))
        return fn

    def step(self):
        # Evaluate always
        for logic in self._always_blocks:
            logic()
        # Propagate to submodules
        for sub in self._submodules:
            sub.step()
        # Evaluate always on
        for logic, signals in self._always_on_blocks:
            if any([s.value != s.next for s in signals]):
                logic()
        # Update all signals (self only)
        for s in self._signals:
            s.update()
