import random

from task import Task


class Profile:
    SERVER = 0
    WORKSTATION = 1

    def __init__(self, profile=0):
        self.profile = profile
        self.min_timeslice = 0
        self.avg_niceness = 0
        self.min_arrival = 0
        self.exec_time_avg = 0

    def set_profile(self, profile):
        self.profile = profile
        if self.profile == Profile.SERVER:
            self.min_timeslice = 10
            self.avg_niceness = -10
            self.min_arrival = 250
            self.exec_time_avg = 700
        elif self.profile == Profile.WORKSTATION:
            self.min_timeslice = 1
            self.avg_niceness = 0
            self.min_arrival = 500
            self.exec_time_avg = 1400

    def get_min_timeslice(self):
        return self.min_timeslice

    def get_avg_niceness(self):
        return self.avg_niceness

    def get_min_arrival(self):
        return self.min_arrival

    def get_exec_time_avg(self):
        return self.exec_time_avg


class Model:
    EXPERIMENTS = 50
    SIM_DURATION = 100000  # simulation time in miliseconds

    profile = None

    @classmethod
    def set_profile(cls, profile):
        cls.profile = profile

    @staticmethod
    def get_task_arrival():
        return int(random.uniform(Model.profile.get_min_arrival(), 1000))

    @staticmethod
    def get_task_exec_time():
        return int(random.expovariate(1 / Model.profile.get_exec_time_avg()))

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
