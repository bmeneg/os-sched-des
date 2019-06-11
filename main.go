package main

import (
    "fmt"
    "github.com/agoussia/godes"
)

const (
    NUM_TASKS = 10
    CTX_SWITCH_DURATION = 0.03 // avarage worst case Intel i7
    MAX_NICE = 19
    MIN_NICE = -20
)

// Probabilistic distribution definitions. Using "false" as argument on them
// asures they won't have the same seed per run, thus we have an IID system.
// Task related
var probTaskArrivalTime *godes.UniformDistr = godes.NewUniformDistr(false)
var probTaskExecTime *godes.ExpDistr = godes.NewExpDistr(false)
var probTaskNiceness *godes.UniformDistr = godes.NewUniformDistr(false)
var taskAvgExecTime float64 = 2000 // unit: ms

// Event related
var probSleepEvent *godes.ExpDistr = godes.NewExpDistr(false) // IO, IRQ, ...
var probAwakeEvent *godes.UniformDistr = godes.NewUniformDistr(false)

// Boolean control
var svFree *godes.BooleanControl = godes.NewBooleanControl()
var taskArrived *godes.BooleanControl = godes.NewBooleanControl()
var evTriggered *godes.BooleanControl = godes.NewBooleanControl()

// DES servers representing system cores
type Server struct {
    *godes.Runner
    c *core
}

var svCounter uint = 0

// DES entities representing tasks
type Entity struct {
    *godes.Runner
    t *task
}

// DES events. Core reference used to manage tasks therein.
type Event struct {
    *godes.Runner
    server *Server
}

var evCounter uint = 0

// How long the simulation lasts (minutes)
var simDuration float64 = 60 * 10

func placeNewTask(c *core) *task {
    // Set some task attributes randomly
    taskExecTime := uint(probTaskExecTime.Get(1 / taskAvgExecTime))
    taskNiceness := int(probTaskNiceness.Get(MIN_NICE, MAX_NICE))
    t := NewTask(GetProcId(), taskNiceness, taskExecTime)
    fmt.Printf("> [%-6.3f] task %d (task group %d) created\n",
        godes.GetSystemTime(), t.id, t.tg.id)
    fmt.Printf("    > exectime = %d\n", t.desExecTime)
    queueSize := c.Schedule(t)
    fmt.Printf("scheduler runqueue size: %d\n", queueSize)
    return t
}

// Core simulation running the following logic:
func (sv *Server) Run() {
    var lastSystemTime float64

    for {
        if svFree.GetState() {
            continue
        }
        lastSystemTime = godes.GetSystemTime()
        evTriggered.WaitAndTimeout(true, sv.c.timeslice)
        fmt.Printf("> systemtime: %f\n", godes.GetSystemTime())
        if evTriggered.GetState() {
            // Server released by an event 
            fmt.Println("> core released by event")
            sv.c.currRunning.vruntime += godes.GetSystemTime() - lastSystemTime
            godes.Advance(CTX_SWITCH_DURATION)
            sv.c.currRunning.state = INTERRUPTABLE
            evTriggered.Set(false)
        } else {
            // Server release by preemption
            sv.c.currRunning.vruntime += sv.c.timeslice
            godes.Advance(CTX_SWITCH_DURATION)
            sv.c.currRunning.state = READY
        }
        if sv.c.runqueue.Size() == 0 {
            svFree.Set(true)
            continue
        }
        if godes.GetSystemTime() > simDuration {
            break
        }
    }
}

// Event simulation running the following logic:
func (ev *Event) Run() {
    for {
        if sleepEv := probSleepEvent.Get(2); sleepEv > 1 {
            fmt.Printf("sleepEv = %f\n", sleepEv)
            evCounter++
            fmt.Printf("> [%-6.3f] event triggered\n", godes.GetSystemTime())
            evTriggered.Set(true)
            if svFree.GetState() {
                fmt.Println("> server is free")
                continue
            }
        } else {
            fmt.Printf("sleepEv = %f\n", sleepEv)
            fmt.Println("> event not generated")
        }
        if godes.GetSystemTime() > simDuration {
            break
        }
        godes.Yield()
    }
}

func main() {
    fmt.Println("# Preparing simulation environment...")

    // Core 0 instance. Single core simulation.
    server := &Server{&godes.Runner{}, NewCore()}
    godes.AddRunner(server)
    godes.AddRunner(&Event{&godes.Runner{}, server})
    svFree.Set(true)
    evTriggered.Set(false)
    taskArrived.Set(false)
    godes.Run()
    for i := 0; i < NUM_TASKS; i++ {
        if godes.GetSystemTime() > simDuration {
            break
        }

        //taskArrived.Set(true)
        _ = placeNewTask(server.c)
        fmt.Println("> running task")
        svFree.Set(false)
        godes.Advance(probTaskArrivalTime.Get(20, 50))
    }
    godes.WaitUntilDone()
    fmt.Println("# Simulation finished")
}
