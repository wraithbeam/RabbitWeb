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
        if (webSocket.OPEN) {
            webSocket.send(JSON.stringify({
                'webcam': getFrame(),
                'person': getPerson(),
                'meeting': getLink()
            }));
        } else {
            return
        }
    }, 1000 / FPS);
}

webSocket.onmessage = function (e) {
    fillWebcams(e.data)
};

webSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};
