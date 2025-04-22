from module import Module


class AndGate(Module):
    def __init__(self):
        super().__init__()
        self.a = self.signal(0)
        self.b = self.signal(0)
        self.out = self.signal(0)

        self.always(self.logic)

    def logic(self):
        self.out.set(self.a() & self.b())


class Top(Module):
    def __init__(self):
        super().__init__()

        self.and1 = self.submodule(AndGate())
        self.and2 = self.submodule(AndGate())

        # Wire things manually
        self.and1.a.set(1)
        self.and1.b.set(1)

        self.and2.a = self.and1.out  # Forward signal
        self.and2.b.set(1)

        self.out = self.and2.out  # Expose result


def main():
    top = Top()

    for _ in range(2):
        top.step()

    print(f"AND2 output: {top.out()}")  # Should print 1


if __name__ == "__main__":
    main()
