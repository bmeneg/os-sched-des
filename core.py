import simpy


class Queue(simpy.PriorityStore):
    def __init__(self, env):
        self._amount_items = 0
        super().__init__(env)

    def __len__(self):
        return self._amount_items

    def put(self, priority, item):
        self._amount_items += 1
        super().put(simpy.PriorityItem(priority, item))

    def get(self):
        self._amount_items -= 1
        return super().get()


class Core:
    CTX_SWITCH_DURATION = 0.03
    DEFAULT_TIMESLICE = 100
    NICE_0_WEIGHT = 1024

    core_id = 0

    def __init__(self, env):
        self.env = env
        self.id = Core.core_id + 1
        self.timeslice = Core.DEFAULT_TIMESLICE
        self.runqueue = Queue(env)
        self.sleepqueue = Queue(env)
        self.curr_task = None
        print(f"@{self.id}: has been created")
        self.action = env.process(self.run())

    def schedule(self, task):
        task.scheduled()
        self.runqueue.put(task.vruntime, task)
        print(f"@{self.id}: task {task.id} scheduled, runqueue length "
              f"{len(self.runqueue)}")

    def sleep(self, task):
        task.sleep()
        self.sleepqueue.put(self.model.get_awake_event(), task)
        print(f"@{self.id}: task {self.curr_task} is now sleeping")

    def calc_vruntime(self, task):
        delta_exec = self.env.now - task.sum_exec_time
        delta_exec_weighted = delta_exec * (Core.NICE_0_WEIGHT/task.weight)
        return delta_exec_weighted

    def run(self):
        while True:
            if self.curr_task is None:
                queue_item = yield self.runqueue.get()
                self.curr_task = queue_item.item
                print(f"@{self.id}: processing task {self.curr_task.id} at "
                      f"{self.env.now}")

                if self.curr_task.exec_start == 0:
                    self.curr_task.exec_start = self.env.now
                else:
                    self.curr_task.sum_exec_time = self.env.now
            try:
                yield self.env.timeout(self.timeslice)
                print(f"@{self.id}: task {self.curr_task.id} preempted at "
                      f"{self.env.now}")
                self.schedule(self.curr_task)
            except simpy.Interrupt as irq:
                print(f"@{self.id}: interrupted by {irq.cause}")
                self.sleep(self.curr_task)

            self.curr_task.vruntime = self.calc_vruntime(self.curr_task)
            self.curr_task = None
            yield self.env.timeout(Core.CTX_SWITCH_DURATION)
