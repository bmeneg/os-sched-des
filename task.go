package main

type Task struct {
    state taskState
    niceness uint8
    totalRuntime uint64
    vruntime uint64
    
    taskGroup struct {
        id uint32
        vruntime uint64
    }

    desExecTime uint64
}
