package main

import (
    "fmt"

    rbt "github.com/emirpasic/gods/trees/redblacktree"
)

var processId uint = 1 // PID 0: init system, avoid to use it here
var taskId uint = 0 // for simplicity it'll be unique to the entire system

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

func NewCore() *core {
    var c *core
    c.id = uint(len(cores))
    c.timeslice = 100
    c.period = 48
    c.runqueue = rbt.NewWithIntComparator()
    cores = append(cores, c)
    fmt.Println("+ core %d has been created", c.id)
    return c
}
