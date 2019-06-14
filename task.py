class Task:
    RUNNING = 0
    READY = 1
    INTERRUPTABLE = 2
    TERMINATED = 3

    task_id = 0

    def __init__(self, env, niceness, exec_time):
        self.env = env
        self.id = Task.task_id + 1
        self.state = Task.READY
        self.nice = niceness
        self.birth_time = env.now
        self.vruntime = 0.0
        self.task_group = None
        self.exec_time = exec_time
        print(f"+ task {self.id} has been created")
