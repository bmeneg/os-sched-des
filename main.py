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

while sim_env.now < Model.SIM_DURATION:
    print("--------------")
    sim_env.run()
