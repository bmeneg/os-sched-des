class Interrupt:
    def __init__(self, env, model, core):
        self.env = env
        self.model = model
        self.core = core
        self.triggered_time = self.env.now
        self.action = env.process(self.run())

    def run(self):
        while True:
            self.core.action.interrupt()
            yield self.env.timeout(self.model.get_sleep_event())
