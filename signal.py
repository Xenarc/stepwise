class Signal:
    def __init__(self, initial=0):
        self.value = initial
        self.next = initial

    def set(self, val):
        self.next = val

    def update(self):
        self.value = self.next

    def __call__(self):
        return self.value
