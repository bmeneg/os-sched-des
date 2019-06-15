class TaskCreator:
    def __init__(self, env, model, core):
        self.env = env
        self.model = model
        self.core = core
        self.action = env.process(self.run())

    def run(self):
        # for task_num in range(self.model.NUM_TASKS):
        while True:
            task = Task(self.env, self.model.get_task_niceness(),
                        self.model.get_task_exec_time())
            self.core.schedule(task)
            yield self.env.timeout(self.model.get_task_arrival())


class Task:
    STATE_RUNNING = 0
    STATE_READY = 1
    STATE_INTERRUPTABLE = 2
    STATE_TERMINATED = 3
    MAX_NICE = 19
    MIN_NICE = -20
    EXEC_TIME_AVG = 2000

    task_id = 0

    def __init__(self, env, niceness, exec_time):
        self.env = env
        self.id = Task.task_id + 1
        Task.task_id += 1
        self.state = Task.STATE_READY
        self.nice = niceness
        self.weight = int(1024 / pow(1.25, self.nice))
        self.birth_time = self.env.now
        self.exec_start = 0
        self.sum_exec_time = 0
        self.prev_exec_time = 0
        self.vruntime = 0
        self.exec_time = exec_time
        print(f"+{self.id}: arrival = {self.birth_time}, nice = {self.nice},"
              f" exec_time = {self.exec_time}")

    def scheduled(self):
        self.state = Task.STATE_READY

    def running(self):
        self.state = Task.STATE_RUNNING

    def sleep(self):
        self.state = Task.STATE_INTERRUPTABLE

    def terminated(self):
        self.state = Task.STATE_TERMINATED
