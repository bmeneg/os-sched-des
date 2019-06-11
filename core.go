package main

import (
    "fmt"
    "github.com/emirpasic/gods/trees/redblacktree"
    "github.com/emirpasic/gods/utils"
)

var processId uint = 1 // PID 0: init system, avoid to use it here

type core struct {
    id uint
    timeslice float64 // unit: ms
    period uint // unit: ms
    runqueue *redblacktree.Tree
    currRunning *task
}

var cores []*core

func GetCore(id uint) *core {
    return cores[id]
}

func GetProcId() uint {
    procId := processId
    processId++
    return procId
}

func (c *core) Schedule(t *task) int {
        c.runqueue.Put(t.id, t.vruntime)
        return c.runqueue.Size()
}

func NewCore() *core {
    c := new(core)
    c.id = uint(len(cores))
    // For simplification we're going to set the timeslice to the
    // SCHED_RR_TIMESLICE value, which is 100ms.
    c.timeslice = 100
    c.period = 48
    c.runqueue = redblacktree.NewWith(utils.UIntComparator)
    cores = append(cores, c)
    fmt.Printf("+ core %d has been created\n", c.id)
    return c
}
