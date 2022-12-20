class WorkletProcessor extends AudioWorkletProcessor {
    process(inputs, outputs){
        this.port.postMessage(inputs[0][0])
        return true
    }
}

registerProcessor('worklet-processor', WorkletProcessor)