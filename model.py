import random

from task import Task


class Profile:
    SERVER = 0
    WORKSTATION = 1

    def __init__(self, profile=0):
        self.profile = profile
        self.min_timeslice = 0
        self.avg_niceness = 0

    def set_profile(self, profile):
        self.profile = profile
        if self.profile == Profile.SERVER:
            self.min_timeslice = 10
            self.avg_niceness = -10
        elif self.profile == Profile.WORKSTATION:
            self.min_timeslice = 1
            self.avg_niceness = 0

    def get_min_timeslice(self):
        return self.min_timeslice

    def get_avg_niceness(self):
        return self.avg_niceness


class Model:
    SIM_DURATION = 10000  # simulation time in miliseconds
    NUM_TASKS = -1  # limit number of tasks to be created

    profile = None

    @classmethod
    def set_profile(cls, profile):
        cls.profile = profile

    @staticmethod
    def get_task_arrival():
        return int(random.uniform(500, 1000))

    @staticmethod
    def get_task_exec_time():
        return int(random.expovariate(1 / Task.EXEC_TIME_AVG))

    @staticmethod
    def get_task_niceness():
        return int(random.triangular(Task.MIN_NICE, Task.MAX_NICE,
                                     Model.profile.get_avg_niceness()))

    @staticmethod
    def get_sleep_event_time():
        return (random.expovariate(1 / 300))

    @staticmethod
    def get_awake_event_priority():
        return int(random.uniform(0, 100))

    @staticmethod
    def get_awake_event_time():
        return int(random.expovariate(1 / 100))
