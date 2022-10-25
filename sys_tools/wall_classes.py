class wall:
    def __init__(self, texter):
        self.texter = texter
    
    def get_type(self):
        return "wall"

class door:
    def __init__(self, texter, lock=False, key=None):
        self.texter = texter
        self.lock = lock
        self.key = key

        if self.lock:
            self.open = False
        else:
            self.open = True

    def get_type(self):
        return "door"

    def open_door(self, key=None):
        if self.lock and not self.open:
            if self.key == key:
                self.open = True
                return "open"
            else:
                return "wrong key"
        else:
           return "open"
