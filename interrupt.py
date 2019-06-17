class InterruptMonitor:
    def __init__(self):
        self.sleep = []
        self.awake = []

    def __len__(self):
        return len(self.mon_sleep), len(self.mon_awake)

    def log_sleep(self, ev_timestamp):
        self.sleep.append(ev_timestamp)

    def log_awake(self, ev_timestamp):
        self.awake.append(ev_timestamp)


class Interrupt:
    def __init__(self, env, model, core):
        self.monitor = InterruptMonitor()
        self.env = env
        self.model = model
        self.core = core
        self.irqs = []
        self.actions = [env.process(self.sleep()), env.process(self.awake())]

    def sleep(self):
        while True:
            yield self.env.timeout(self.model.get_sleep_event_time())
            if self.core.curr_task is not None:
                self.core.action.interrupt()
                self.monitor.log_sleep(self.env.now)

    def awake(self):
        while True:
            yield self.env.timeout(self.model.get_awake_event_time())
            if len(self.core.sleepqueue):
                queue_item = yield self.core.sleepqueue.get()
                task = queue_item.item
                print(f"!AWAKE: task {task.id}")
                self.core.schedule(task)
                self.monitor.log_awake(self.env.now)
