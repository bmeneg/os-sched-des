import random


class Model:
    NUM_TASKS = 10

    TASK_EXEC_TIME_AVG = 2000
    TASK_CTX_SWITCH_DURATION = 0.03
    TASK_MAX_NICE = 19
    TASK_MIN_NICE = -20

    CORE_DEFAULT_TIMESLICE = 100

    task_arrival_rdm = random.uniform(20, 50)
    task_exec_time_rdm = random.expovariate(1 / TASK_EXEC_TIME_AVG)
    task_niceness_rdm = random.uniform(TASK_MIN_NICE, TASK_MAX_NICE)

    event_sleep_rdm = random.expovariate(1)
    event_awake_rdm = random.uniform(0, 5)
