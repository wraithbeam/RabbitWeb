const FPS = 5 //4
const scroller = document.getElementById('item-0')

const getFrame = () => {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    const data = canvas.toDataURL('image/png');
    return data;
}

const fillWebcams = (data) => {
    var dataJson = JSON.parse(data)
    for (var elem in dataJson) {
        let somePersonWebcam = document.getElementById(elem)
        if (somePersonWebcam == null) {
            let newPersonWebcam = document.createElement('img')
            newPersonWebcam.classList.add('people-webcam')
            newPersonWebcam.id = elem
            newPersonWebcam.src = dataJson[elem].webcam_meta
            scroller.appendChild(newPersonWebcam)
        }
        else {
            somePersonWebcam.src = dataJson[elem].webcam_meta
        }
    }
    // let newElement = document.createElement('img');
    // console.log(data['webcam_meta'])
    // newElement.src = data['webcam_meta']
    // scroller.appendChild(newElement)
}
