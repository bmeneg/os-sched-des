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
import csv
import random

from model import Profile, Model
from core import Core
from interrupt import Interrupt
from task import TaskCreator

# Experiment's variables of interest
exp_num_tasks = 0
exp_max_num_tasks = 0
exp_min_num_tasks = 0
exp_core_idle_time = 0
exp_max_core_idle_time = 0
exp_core_proc_time = 0
exp_max_core_proc_time = 0
exp_core_ctx_switch_time = 0
exp_max_core_ctx_switch_time = 0
exp_task_run_time = 0
exp_max_task_run_time = 0
exp_task_rdy_time = 0
exp_max_task_rdy_time = 0
exp_task_int_time = 0
exp_max_task_int_time = 0

with open("result_server_disc.csv", "w+", newline='') as csv_fd:
    w = csv.writer(csv_fd)
    for experiment in range(Model.EXPERIMENTS):
        random.seed()
        w.writerow([f"Experiment #{experiment}"])
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

        exp_core_idle_time += core.monitor.idle_time
        exp_max_core_idle_time = max((exp_max_core_idle_time,
                                      core.monitor.idle_time))
        exp_core_proc_time += core.monitor.processing_time
        exp_max_core_proc_time = max((exp_max_core_proc_time,
                                      core.monitor.processing_time))
        exp_core_ctx_switch_time += core.monitor.ctx_switch_time
        exp_max_core_ctx_switch_time = max((exp_max_core_ctx_switch_time,
                                            core.monitor.ctx_switch_time))
        task_run_row = ["running time"]
        task_rdy_row = ["ready time"]
        task_int_row = ["sleep time"]
        for p_item in core.sink.items:
            exp_num_tasks += 1
            task_run_row.append(p_item.item.monitor.running_time)
            task_rdy_row.append(p_item.item.monitor.ready_time)
            task_int_row.append(p_item.item.monitor.interruptable_time)
            exp_task_run_time += p_item.item.monitor.running_time
            exp_max_task_run_time = max((exp_max_task_run_time,
                                        p_item.item.monitor.running_time))
            exp_task_rdy_time += p_item.item.monitor.ready_time
            exp_max_task_rdy_time = max((exp_max_task_rdy_time,
                                        p_item.item.monitor.ready_time))
            exp_task_int_time += p_item.item.monitor.interruptable_time
            exp_max_task_int_time = \
                max((exp_max_task_int_time,
                     p_item.item.monitor.interruptable_time))

        w.writerow(task_run_row)
        w.writerow(task_rdy_row)
        w.writerow(task_int_row)
        w.writerow([])

        core_runqueue_timestamp = []
        core_runqueue_size = []
        for i in core.runqueue.monitor.queue:
            core_runqueue_timestamp.append(i[0])
            core_runqueue_size.append(i[1])

        w.writerow(core_runqueue_timestamp)
        w.writerow(core_runqueue_size)
        w.writerow([])

        core_sleepqueue_timestamp = []
        core_sleepqueue_size = []
        for i in core.sleepqueue.monitor.queue:
            core_sleepqueue_timestamp.append(i[0])
            core_sleepqueue_size.append(i[1])

        w.writerow(core_sleepqueue_timestamp)
        w.writerow(core_sleepqueue_size)
        w.writerow([])

# Get the mean of each variable based on the mean avg number of tasks
exp_num_tasks = int(exp_num_tasks / Model.EXPERIMENTS) + 1
exp_core_idle_time = exp_core_idle_time / Model.EXPERIMENTS
exp_core_proc_time = exp_core_proc_time / Model.EXPERIMENTS
exp_core_ctx_switch_time = exp_core_ctx_switch_time / Model.EXPERIMENTS
exp_total_task_run_time = exp_task_run_time / Model.EXPERIMENTS
exp_total_task_rdy_time = exp_task_rdy_time / Model.EXPERIMENTS
exp_total_task_int_time = exp_task_int_time / Model.EXPERIMENTS
exp_total_task_life_time = (exp_total_task_run_time + exp_total_task_rdy_time +
                            exp_total_task_int_time)
exp_task_run_time = exp_task_run_time / exp_num_tasks / Model.EXPERIMENTS
exp_task_rdy_time = exp_task_rdy_time / exp_num_tasks / Model.EXPERIMENTS
exp_task_int_time = exp_task_int_time / exp_num_tasks / Model.EXPERIMENTS
exp_task_life_time = (exp_task_run_time + exp_task_rdy_time +
                      exp_task_int_time)

with open("result_server.csv", "w+", newline='') as csv_fd:
    w = csv.writer(csv_fd)
    w.writerow(["core", f"{core.id}"])
    w.writerow(["idle time", exp_core_idle_time, exp_max_core_idle_time])
    w.writerow(["processing time", exp_core_proc_time, exp_max_core_proc_time])
    w.writerow(["context switch time", exp_core_ctx_switch_time,
                exp_max_core_ctx_switch_time])
    w.writerow([])

    task_id_row = [f"tasks = {exp_num_tasks}", "total avg", "individual avg",
                   "individual max"]
    task_run_row = ["running time", exp_total_task_run_time, exp_task_run_time,
                    exp_max_task_run_time]
    task_rdy_row = ["ready time", exp_total_task_rdy_time, exp_task_rdy_time,
                    exp_max_task_rdy_time]
    task_int_row = ["sleep time", exp_total_task_int_time, exp_task_int_time,
                    exp_max_task_int_time]
    task_life_row = ["life time", exp_total_task_life_time, exp_task_life_time]
    w.writerow(task_id_row)
    w.writerow(task_run_row)
    w.writerow(task_rdy_row)
    w.writerow(task_int_row)
    w.writerow(task_life_row)
