# sched-des
Discrete Event Simulator for Linux operating system scheduler

The idea is to build an OS scheduler simulator using Discrete Events principles
and also Linux Scheduler as reference, which uses the _Completely Fair
Scheduling_ (CFS), which in turn is based on the Weighted Fair Queue (WFQ),
wherein the available CPU cycles is divided among the threads to be processed
based on its weight, this division is done through a _timeslice_, which is an
amount of time units each thread has to run.

Each thread has some properties that define how and when they are chosen to be
processed by the CPU. The most important one is the _niceness_ which defines
the weight of that thread. The bigger niceness a thread has the lower is it
weight. You can think it as "_how nice a task is_".
