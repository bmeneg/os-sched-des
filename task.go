package main

import (
    "fmt"
    "time"
)

// Task groups represents applications with multiple threads running.
// Within Linux each user thread is converted to a kernel thread (task) and
// a group is necessary to make fairly use of CPU's timeslices.
type taskGroup struct {
    id uint
    // Last task ID assigned to this group, starting from 0
    length uint
    vruntime uint
}


// Available task states
const (
    RUNNING = 0
    INTERRUPTABLE = 1 
    TERMINATED = 2
)

// Global task id to simplify things
var taskId uint = 0

// This task structure considers only small amount of properties that are
// necessary for single core machines. Other than that, there are bunch of
// other properties to allow, i.e., multiple scheduler algorithms, which is not
// considered here.
type task struct {
    id uint
    state uint8
    nice int
    birthTime time.Time
    totalRunTime uint // unit: ms
    timesSched uint
    vruntime uint // unit: ms
    tg *taskGroup 

    // Simulation specific field: the value is used as the amount of time
    // needed to the task be considered complete, it is basically compared to
    // totalRuntime, if it's greater or equal, terminates the task.
    desExecTime uint
}

func (tg *taskGroup) Length() uint {
    return uint(tg.length + 1)
}

func NewTask(procId uint, niceness int, execTime uint) *task {
    t := new(task)
    t.id = taskId + 1
    taskId++
    t.tg = new(taskGroup)
    t.tg.id = procId
    t.tg.length++
    t.state = RUNNING
    t.nice = niceness
    t.birthTime = time.Now()
    t.desExecTime = execTime
    fmt.Printf("+ task %d has been created\n", t.id)
    return t
}
