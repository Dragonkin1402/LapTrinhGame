import time

class Skill:
    def __init__(self, cooldown):
        self.cooldown = cooldown
        self.last_used = 0

    def can_use(self):
        return time.time() - self.last_used > self.cooldown

    def use(self):
        self.last_used = time.time()