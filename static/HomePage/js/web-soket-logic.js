const webSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/meeting/'
    + "aue"
    + '/'
);

webSocket.onopen = function () {
    //Sending webcam
    setInterval(() => {
        webSocket.send(JSON.stringify({
            'webcam': getFrame()
        }));
    }, 1000 / FPS);
}

webSocket.onmessage = function (e) {

};

webSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};
