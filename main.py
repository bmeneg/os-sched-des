#!/usr/bin/env python3

import simpy

from model import Model
from core import Core
from interrupt import Interrupt
from task import TaskCreator


sim_env = simpy.Environment()
core = Core(sim_env, Model)
task_creator = TaskCreator(sim_env, Model, core)
irq = Interrupt(sim_env, Model, core)

print(f"-- Starting simulation with duration = {Model.SIM_DURATION}")
sim_env.run(until=Model.SIM_DURATION)

for action in irq.actions:
    action.interrupt("end")
task_creator.action.interrupt("end")
core.action.interrupt("end")
