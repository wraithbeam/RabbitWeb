const webSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/meeting/'
    + getLink()
    + '/'
    // + getPerson()
    // + '/'
);

webSocket.onopen = function () {
    //Sending webcam
    console.log("Open")
    setInterval(() => {
        if (webSocket.OPEN) {
            webSocket.send(JSON.stringify({
                'webcam': getFrame(),
                'person_initials': getPersonInitials(),
                'person_name' : getPersonName(),
                'meeting': getLink(),
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
    console.error('Chat socket closed unexpectedly', e);
};