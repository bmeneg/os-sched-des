#!/usr/bin/env python3

# This project was divided into conceptual components to represent a computer
# system:
#   - model: that bring all the definitions around the simulation model;
#   - core: which represents the system processor core;
#   - task: representing the system tasks itself;
#   - task creator: the component responsible to create tasks randomly;
#   - interrupt: component that generates the interrupts for the tasks (i.e.
#   I/O request).

import simpy

from model import Profile, Model
from core import Core
from interrupt import Interrupt
from task import TaskCreator, TaskMonitor

# simulation environment and their components
sim_env = simpy.Environment()
profile = Profile()
profile.set_profile(Profile.SERVER)
Model.set_profile(profile)
core = Core(sim_env, Model)
task_creator = TaskCreator(sim_env, Model, core)
irq = Interrupt(sim_env, Model, core)

print(f"-- Starting simulation with duration = {Model.SIM_DURATION}")
sim_env.run(until=Model.SIM_DURATION)

print(f"idle: {core.monitor.idle_time}")
print(f"processing: {core.monitor.processing_time}")
print(f"ctx_switch: {core.monitor.ctx_switch_time}")

for p_item in core.sink.items:
    print(p_item.item.id)
    print(TaskMonitor.log_summary(p_item.item.monitor))
