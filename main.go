package main

import (
    "fmt"

    des "github.com/agoussia/godes"
)

var entityArrival *des.UniformDistr = des.NewUniformDistr(true)

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
    fmt.Println("> entity %ud associated to task %ud (task group %ud)", et.cnt,
        et.t.id, et.t.tg.id)
}

func main() {
    var shutdownTime float64 = 60 * 8
    fmt.Println("# Preparing simulation code...")
    des.Run()
    for {
        if des.GetSystemTime() < shutdownTime {
            var t *task
            des.AddRunner(&Entity{&des.Runner{}, t, entityCnt})
            des.Advance(entityArrival.Get(0, 70))
            entityCnt++
        } else {
            break
        }
    }
    des.WaitUntilDone()
}
