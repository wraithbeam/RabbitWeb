const webSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/meeting/'
    + getLink()
    + '/'
);

webSocket.onopen = function () {
    //Sending webcam
    setInterval(() => {
        webSocket.send(JSON.stringify({
            'type': 'webcam',
            'webcam': getFrame(),
            'person_initials': getPersonInitials(),
            'person_name': getPersonName(),
            'meeting': getLink(),
        }));
    }, 1000 / FPS);
}

webSocket.onmessage = async function (e) {
    const dataJson = JSON.parse(e.data);
    switch (dataJson.type) {
        case 'webcam':
            fillWebcams(dataJson.content)
            break
        case 'delete':
            updateWebcams()
            break
        case 'sound':
            await play_sound(dataJson.content)
            break
        case 'message':
            show_message(dataJson.content)
            break
    }
};