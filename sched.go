package main

type taskState uint8

const (
    Running taskState = 0
    Interruptable taskState = 1
    Stopped taskState = 2
)

