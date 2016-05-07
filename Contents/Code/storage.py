class Storage():
    def __init__(self):
        self.data = []

    def items(self):
        return self.data

    def clear(self):
        self.data = []

    def exist(self):
        return True

    def add(self, item):
        self.data.append(item)

    def remove(self, item):
        self.data.remove(item)

    def load(self):
        self.clear()

        if self.exist():
            self.data = self.load_storage()

    def save(self):
        self.save_storage(self.data)

    def load_storage(self):
        pass

    def save_storage(self, data):
        self.data = data

