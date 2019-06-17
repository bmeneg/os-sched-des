import simpy


class QueueMonitor:
    def __init__(self):
        self.queue = []

    def log_queue(self, timestamp, queue_len):
        self.queue.append((timestamp, queue_len))


class Queue(simpy.PriorityStore):
    def __init__(self, env, name):
        super().__init__(env)
        self.env = env
        self.monitor = QueueMonitor()
        self.name = name
        self.highest = 0
        self.smallest = 0
        self.weight = 0

    def __len__(self):
        return len(self.items)

    def put(self, priority, item):
        super().put(simpy.PriorityItem(priority, item))
        self.monitor.log_queue(self.env.now, len(self))
        id_list = [p_item.item.id for p_item in self.items]
        print(f">q_{self.name}: {id_list}")
        self.highest = self.items[-1].priority
        self.smallest = self.items[0].priority

    def get(self):
        return super().get()


class CoreMonitor:
    def __init__(self):
        self.prev_timestamp = 0
        self.idle_time = 0
        self.processing_time = 0
        self.ctx_switch_time = 0

    def log_idle(self, timestamp):
        self.idle_time += timestamp - self.prev_timestamp
        self.prev_timestamp = timestamp

    def log_processing(self, timestamp):
        self.processing_time += timestamp - self.prev_timestamp
        self.prev_timestamp = timestamp

    def log_ctx_switch(self, timestamp):
        self.ctx_switch_time += timestamp - self.prev_timestamp
        self.prev_timestamp = timestamp


class Core:
    CTX_SWITCH_DURATION = 0.03
    DEFAULT_TIMESLICE = 100
    DEFAULT_PERIOD = 48
    NICE_0_WEIGHT = 1024

    core_id = 0

    def __init__(self, env, model):
        self.monitor = CoreMonitor()
        self.env = env
        self.model = model
        self.id = Core.core_id + 1
        self.timeslice = Core.DEFAULT_TIMESLICE
        self.period = Core.DEFAULT_PERIOD
        self.min_timeslice = self.model.profile.get_min_timeslice()
        self.runqueue = Queue(env, "run")
        self.sleepqueue = Queue(env, "sleep")
        self.sink = Queue(env, "sink")
        self.curr_task = None
        print(f"@c_{self.id}: has been created")
        self.action = env.process(self.run())

    def schedule(self, task):
        task.scheduled()
        if task.vruntime == 0:
            task.vruntime = self.runqueue.highest
        elif task.interrupted:
            task.vruntime = self.runqueue.smallest

        self.runqueue.put(task.vruntime, task)
        self.runqueue.weight += task.weight
        if len(self.runqueue) > 8:
            self.period = len(self.runqueue) * 6
        else:
            self.period = Core.DEFAULT_PERIOD

        print(f"@c_{self.id}: task {task.id} (vruntime = {task.vruntime}) "
              f"scheduled, runqueue length {len(self.runqueue)}")

    def sleep(self, task):
        task.sleep()
        self.sleepqueue.put(self.model.get_awake_event_priority(), task)
        print(f"@c_{self.id}: task {task.id} interrupted")

    def terminate(self, task):
        task.terminated()
        self.sink.put(0, task)

    def set_vruntime(self, task):
        delta_exec = self.env.now - task.exec_start
        task.sum_exec_time += delta_exec
        delta_exec_weighted = delta_exec * (Core.NICE_0_WEIGHT / task.weight)
        task.vruntime += delta_exec_weighted

    def run(self):
        while True:
            if self.curr_task is None:
                queue_item = yield self.runqueue.get()
                self.curr_task = queue_item.item
                self.monitor.log_idle(self.env.now)

                new_timeslice = self.period * (self.curr_task.weight /
                                               self.runqueue.weight)
                if new_timeslice < self.min_timeslice:
                    self.timeslice = self.min_timeslice
                else:
                    self.timeslice = new_timeslice

                self.runqueue.weight -= self.curr_task.weight
                termination = self.curr_task.sum_exec_time + self.timeslice
                if self.curr_task.exec_time < termination:
                    self.timeslice = (1 + self.curr_task.exec_time -
                                      self.curr_task.sum_exec_time)
                self.curr_task.exec_start = self.env.now
                self.curr_task.running()
                print(f"@c_{self.id}: processing task {self.curr_task.id} at "
                      f"{self.env.now} with timeslice = {self.timeslice}")

            try:
                yield self.env.timeout(self.timeslice)
                self.monitor.log_processing(self.env.now)
                print(f"@c_{self.id}: task {self.curr_task.id} preempted at "
                      f"{self.env.now}")
                self.set_vruntime(self.curr_task)
                if self.curr_task.exec_time <= self.curr_task.sum_exec_time:
                    self.terminate(self.curr_task)
                else:
                    self.schedule(self.curr_task)
            except simpy.Interrupt:
                self.set_vruntime(self.curr_task)
                self.sleep(self.curr_task)

            self.curr_task = None
            yield self.env.timeout(Core.CTX_SWITCH_DURATION)
            self.monitor.log_ctx_switch(self.env.now)
