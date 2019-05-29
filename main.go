package main

import (
    "fmt"

    des "github.com/agoussia/godes"
)

// Probabilistic distribution definitions. Using "false" as argument on them
// asures they won't have the same seed per run, thus we have an IID system.
var entityArrival *des.UniformDistr = des.NewUniformDistr(false)
var entityExecTime *des.ExpDistr = des.NewExpDistr(false)
var entitySleepTime *des.ExpDistr = des.NewExpDistr(false)

var avgExecTime float64 = 2000 // unit: ms

type Entity struct {
    *des.Runner
    t *task
    cnt uint
}

var entityCnt uint = 0

type Server struct {
    *des.Runner
    c *core
    cnt uint
}

func (et *Entity) Run() {
    fmt.Printf("> [%-6.3f] entity %d associated to task %d (task group %d)\n",
        des.GetSystemTime(), et.cnt, et.t.id, et.t.tg.id)
    fmt.Printf("    > task %d: exectime = %d\n", et.t.id, et.t.desExecTime)
}

func main() {
    var shutdownTime float64 = 60 * 8
    fmt.Println("# Preparing simulation code...")
    des.Run()
    for {
        if des.GetSystemTime() < shutdownTime {
            etExecTime := uint(entityExecTime.Get(1 / avgExecTime))
            t := NewTask(GetProcId(), 0, etExecTime)
            des.AddRunner(&Entity{&des.Runner{}, t, entityCnt})
            des.Advance(entityArrival.Get(0, 70))
            entityCnt++
        } else {
            break
        }
    }
    des.WaitUntilDone()
}
