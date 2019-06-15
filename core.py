import simpy


class Core:
    CTX_SWITCH_DURATION = 0.03
    DEFAULT_TIMESLICE = 100

    core_id = 0

    def __init__(self, env):
        self.env = env
        self.id = Core.core_id + 1
        self.timeslice = Core.DEFAULT_TIMESLICE
        self.runqueue = simpy.PriorityStore(env)
        self.runqueue_len = 0
        self.curr_task = None
        print(f"+ core {self.id} has been created")
        self.action = env.process(self.run())

    def schedule(self, task):
        self.runqueue.put(simpy.PriorityItem(task.vruntime, task))
        self.runqueue_len += 1
        print(f"@ task {task.id} scheduled on core {self.id}, runqueue " +
              f"length {self.runqueue_len}")

    def run(self):
        while True:
            print(f"> core {self.id} started running at {self.env.now}")
            try:
                yield self.env.timeout(self.timeslice)
            except simpy.Interrupt as irq:
                print(f"! core {self.id} got interrupted by {irq.cause}")
