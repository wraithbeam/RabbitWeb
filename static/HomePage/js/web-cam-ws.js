const FPS = 16 //4
const scroller = document.getElementById('item-0')

const getFrame = () => {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth / 2;
    canvas.height = video.videoHeight / 2;
    let ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0, video.videoWidth / 2, video.videoHeight / 2);
    return canvas.toDataURL('image/jpeg', 0.6);
}

const fillWebcams = (dataJson) => {
    let webcam_content;
    for (const elem in dataJson) {
        let somePersonWebcam = document.getElementById(elem + "-container")
        if (somePersonWebcam == null) {
            let newPersonWebcamContainer = document.createElement('div')
            newPersonWebcamContainer.id = elem + "-container"
            newPersonWebcamContainer.classList.add("webcam-container")

            if (dataJson[elem].webcam_meta === "data:,") {
                createProfilePic(dataJson[elem], elem, newPersonWebcamContainer)
            } else {
                webcam_content = document.createElement('img')
                webcam_content.id = elem
                webcam_content.src = dataJson[elem].webcam_meta
                webcam_content.classList.add("people-webcam")
                newPersonWebcamContainer.appendChild(webcam_content)
            }
            scroller.appendChild(newPersonWebcamContainer)
        } else {
            webcam_content = document.getElementById(elem)
            if (dataJson[elem].webcam_meta === "data:,") {
                if (webcam_content.tagName !== 'DIV') {
                    webcam_content.remove()
                    createProfilePic(dataJson[elem], elem, somePersonWebcam)
                    scroller.appendChild(somePersonWebcam)
                }
            } else {
                if (webcam_content.tagName !== 'IMG') {
                    webcam_content.remove()
                    webcam_content = document.createElement('IMG')

                    webcam_content.id = elem
                    webcam_content.classList.add("people-webcam")
                    somePersonWebcam.appendChild(webcam_content)
                    scroller.appendChild(somePersonWebcam)
                }
                webcam_content.src = dataJson[elem].webcam_meta
            }
        }
    }
}

const createProfilePic = function (data, elem, containerWebcam) {
    let initials = document.createElement('div')
    initials.classList.add('initials')
    initials.innerText = data.initials
    initials.id = elem
    containerWebcam.appendChild(initials)
}

const updateWebcams = function () {
    for (let i = 0; i < scroller.children.length; i++) {
        scroller.children.item(i).remove()
    }
}