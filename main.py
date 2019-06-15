#!/usr/bin/env python3

import simpy

from model import Model
from core import Core
from task import Task

sim_env = simpy.Environment()
core = Core(sim_env)

while sim_env.now < Model.SIM_DURATION:
    task = Task(sim_env, Model.get_task_arrival(), Model.get_task_niceness(),
                Model.get_task_exec_time())
    core.schedule(task)
    sim_env.step()
