package main

import (
    "fmt"

    des "github.com/agoussia/godes"
)

const MAX_NICE = 19
const MIN_NICE = -20

// Probabilistic distribution definitions. Using "false" as argument on them
// asures they won't have the same seed per run, thus we have an IID system.
// Task related
var probTaskArrivalTime *des.UniformDistr = des.NewUniformDistr(false)
var probTaskExecTime *des.ExpDistr = des.NewExpDistr(false)
var probTaskNiceness *des.UniformDistr = des.NewUniformDistr(false)
var taskAvgExecTime float64 = 2000 // unit: ms

// Event related
var probSleepEvent *des.ExpDistr = des.NewExpDistr(false) // IO, IRQ, ...
var probAwakeEvent *des.UniformDistr = des.NewUniformDistr(false)

// Server active/idle control
var svFree *des.BooleanControl = des.NewBooleanControl()

// DES servers representing system cores
type Server struct {
    *des.Runner
    c *core
}

var svCounter uint = 0

// DES events. Core reference used to manage tasks therein.
type Event struct {
    *des.Runner
    c *core
}

var evCounter uint = 0

// How long the simulation lasts (minutes)
var simDuration float64 = 60 * 10

// Core simulation running the following logic:
func (sv *Server) Run() {
    for {
        svFree.Wait(true)
        taskExecTime := uint(probTaskExecTime.Get(1 / taskAvgExecTime))
        taskNiceness := int(probTaskNiceness.Get(MIN_NICE, MAX_NICE))
        t := NewTask(GetProcId(), taskNiceness, taskExecTime)
        fmt.Printf("> [%-6.3f] task %d (task group %d) created\n",
            des.GetSystemTime(), t.id, t.tg.id)
        fmt.Printf("    > exectime = %d\n", t.desExecTime)
        svFree.Set(false)

        if des.GetSystemTime() > simDuration {
            break
        }
    }
}

// Event simulation running the following logic:
func (ev *Event) Run() {

}

func main() {
    fmt.Println("# Preparing simulation environment...")

    // Core 0 instance. Single core simulation.
    c := NewCore()
    des.AddRunner(&Server{&des.Runner{}, c})
    des.AddRunner(&Event{&des.Runner{}, c})
    des.Run()
    for {
        if des.GetSystemTime() > simDuration {
            break
        }

        svFree.Set(true)
        fmt.Println("advancing")
        des.Advance(probTaskArrivalTime.Get(0, 70))
    }
    des.WaitUntilDone()
    fmt.Println("# Simulation finished")
}
