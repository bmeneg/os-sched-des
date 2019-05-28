package main

import (
    "fmt"

    rbt "github.com/emirpasic/gods/trees/redblacktree"
)

var ProcessId uint = 1 // PID 0: init system, avoid to use it here
var ThreadId uint = 0 // for simplicity it'll be unique to the entire system

type Core struct {
    Id uint
    Timeslice uint // unit: ms
    Period uint // unit: ms
    Runqueue *rbt.Tree
}

var cores []*Core

func (c *Core) NumReadyTasks() uint {
    return uint(c.Runqueue.Size() + 1)
}

func GetCore(id uint) *Core {
    return cores[id]
}

func NewCore() *Core {
    var core *Core

    core.Id = uint(len(cores))
    core.Timeslice = 100
    core.Period = 48
    core.Runqueue = rbt.NewWithIntComparator()
    append(cores, core)
    fmt.Println("+ core %d has been created", core.Id)
    
    return core
}
