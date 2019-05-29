package main

import (
    "fmt"

    rbt "github.com/emirpasic/gods/trees/redblacktree"
)

var processId uint = 1 // PID 0: init system, avoid to use it here

type core struct {
    id uint
    timeslice uint // unit: ms
    period uint // unit: ms
    runqueue *rbt.Tree
}

var cores []*core

func (c *core) NumReadyTasks() uint {
    return uint(c.runqueue.Size() + 1)
}

func GetCore(id uint) *core {
    return cores[id]
}

func GetProcId() uint {
    procId := processId
    processId++
    return procId
}

func NewCore() *core {
    c := new(core)
    c.id = uint(len(cores))
    c.timeslice = 100
    c.period = 48
    c.runqueue = rbt.NewWithIntComparator()
    cores = append(cores, c)
    fmt.Printf("+ core %d has been created\n", c.id)
    return c
}
