import simpy
from .model import Model


class Core:
    core_id = 0

    def __init__(self, env):
        self.env = env
        self.id = Core.core_id + 1
        self.timeslice = Model.CORE_DEFAULT_TIMESLICE
        self.runqueue = simpy.PriorityStore(env)
        self.runqueue_len = 0
        self.curr_task = None

    def schedule(self, task):
        self.runqueue.put(simpy.PriorityItem(task.vruntime, task))
        self.runqueue_len += 1
