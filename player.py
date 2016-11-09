class player(object):
    def __init__(self, name, position, per):
        self.name = name
        self.position = position
        self.per = per

    def __str__(self):
        return self.name
