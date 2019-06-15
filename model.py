import random

from task import Task


class Model:
    SIM_DURATION = 50000  # simulation time in miliseconds
    NUM_TASKS = -1  # limit number of tasks to be created

    @staticmethod
    def get_task_arrival():
        return int(random.uniform(500, 1000))

    @staticmethod
    def get_task_exec_time():
        return int(random.expovariate(1 / Task.EXEC_TIME_AVG))

    @staticmethod
    def get_task_niceness():
        return int(random.uniform(Task.MIN_NICE, Task.MAX_NICE))

    @staticmethod
    def get_sleep_event_time():
        return int(random.expovariate(1 / 300))

    @staticmethod
    def get_awake_event_priority():
        return int(random.uniform(0, 100))

    @staticmethod
    def get_awake_event_time():
        return int(random.expovariate(1 / 100))
