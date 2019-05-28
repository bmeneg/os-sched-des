package main

import (
    "fmt"
    "time"
)

// Task groups represents applications with multiple threads running.
// Within Linux each user thread is converted to a kernel thread (task) and
// a group is necessary to make fairly use of CPU's timeslices.
type taskGroup struct {
    Id uint
    // Last task ID assigned to this group, starting from 0
    TaskId uint
    Vruntime uint
}


// Available task states
const (
    Running = 0
    Interruptable = 1 
    Stopped = 2
)

// This task structure considers only small amount of properties that are
// necessary for single core machines. Other than that, there are bunch of
// other properties to allow, i.e., multiple scheduler algorithms, which is not
// considered here.
type Task struct {
    Id uint
    State uint8
    Nice int
    BirthTime time.Time
    TotalRunTime uint // unit: ms
    TimesSched uint
    Vruntime uint // unit: ms
    Tg *taskGroup 

    // Simulation specific field: the value is used as the amount of time
    // needed to the task be considered complete, it is basically compared to
    // totalRuntime, if it's greater or equal, terminates the task.
    DesExecTime uint
}

func (tg *taskGroup) Length() uint {
    return uint(tg.TaskId + 1)
}

func NewTask(procId uint, niceness int, execTime uint) *Task {
    var t *Task
    
    t.Id = ThreadId + 1
    ThreadId++
    t.Tg.Id = procId
    t.State = Running
    t.Nice = niceness
    t.BirthTime = time.Now()
    t.DesExecTime = execTime
    fmt.Println("+ task %d has been created", t.Id)
    
    return t
}
