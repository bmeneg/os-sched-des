import random

from task import Task


class Model:
    SIM_DURATION = 500
    NUM_TASKS = 10

    @staticmethod
    def get_task_arrival():
        return random.uniform(50, 100)

    @staticmethod
    def get_task_exec_time():
        return random.expovariate(1 / Task.EXEC_TIME_AVG)

    @staticmethod
    def get_task_niceness():
        return random.uniform(Task.MIN_NICE, Task.MAX_NICE)

    @staticmethod
    def get_sleep_event():
        return random.expovariate(1)

    @staticmethod
    def get_awake_event():
        return random.uniform(0, 5)
