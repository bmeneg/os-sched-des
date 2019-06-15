class Interrupt:
    def __init__(self, env, model, core):
        self.env = env
        self.model = model
        self.core = core
        self.irqs = []
        env.process(self.sleep())
        env.process(self.awake())

    def sleep(self):
        while True:
            yield self.env.timeout(self.model.get_sleep_event_time())
            if self.core.curr_task is not None:
                self.core.action.interrupt()
                self.irqs.append(self.env.now)

    def awake(self):
        while True:
            yield self.env.timeout(self.model.get_awake_event_time())
            if len(self.core.sleepqueue):
                queue_item = yield self.core.sleepqueue.get()
                task = queue_item.item
                print(f"!AWAKE: task {task.id}")
                self.core.schedule(task)
