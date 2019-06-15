class Task:
    STATE_RUNNING = 0
    STATE_READY = 1
    STATE_INTERRUPTABLE = 2
    STATE_TERMINATED = 3
    MAX_NICE = 19
    MIN_NICE = -20
    EXEC_TIME_AVG = 2000

    task_id = 0

    def __init__(self, env, arrival, niceness, exec_time):
        self.env = env
        self.id = Task.task_id + 1
        self.state = Task.STATE_READY
        self.nice = int(niceness)
        self.arrival_eta = int(arrival)
        self.vruntime = 0
        self.task_group = None
        self.exec_time = int(exec_time)
        print(f"+ task {self.id} has been created")
        print(f"    > arrival = {self.arrival_eta}, nice = {self.nice}, " +
              f"exec_time = {self.exec_time}")
        self.action = env.process(self.arrive())

    def arrive(self):
        yield self.env.timeout(self.arrival_eta)
        self.birth_time = self.env.now + self.arrival_eta
        print(f"+ {self.id} self generated at {self.birth_time}")
