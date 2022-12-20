async function start_micro() {
    const audioContext = new AudioContext();

    let stream = await navigator.mediaDevices.getUserMedia({audio: true})
    const source = audioContext.createMediaStreamSource(stream);

    await audioContext.audioWorklet.addModule('/static/HomePage/js/worklet-processor.js');
    const audioWorkletNode = new AudioWorkletNode(audioContext, 'worklet-processor');
    source.connect(audioWorkletNode);
    audioWorkletNode.connect(audioContext.destination);

    audioWorkletNode.port.onmessage = (event) => {
        const inputData = event.data
        const message = {type: 'sound', 'content': inputData};
        webSocket.send(JSON.stringify(message));
    }
}

async function play_sound (data) {
    const audioContext = new AudioContext();

    const audioDataArray = new Float32Array(Object.values(data))
    const audioBuffer = audioContext.createBuffer(1, audioDataArray.length, audioContext.sampleRate);
    audioBuffer.copyToChannel(audioDataArray, 0, 0);

    const bufferSource = audioContext.createBufferSource();
    bufferSource.buffer = audioBuffer;
    bufferSource.connect(audioContext.destination);

    bufferSource.start();
}