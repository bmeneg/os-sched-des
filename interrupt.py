class Interrupt:
    def __init__(self, env):
        self.env = env
        self.triggered_tim = env.now
