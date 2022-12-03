// Grab elements, create settings, etc.
var video = document.getElementById('chosen-webcam-id');
var video_io = document.getElementById('webcam-io')
var is_webcam_on = false
var web_stream = null

video_io.onclick = function () {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        is_webcam_on = !is_webcam_on
        if (is_webcam_on) {
            navigator.mediaDevices.getUserMedia({video: true}).then(function (stream) {
                web_stream = stream
                video.srcObject = stream;
                video.classList.add("person-webcam")
                video.play()
            });
        } else {
            if (web_stream != null && web_stream.active) {
                web_stream.getTracks().forEach(function (track) {
                    track.stop()
                })
            }
            video.srcObject = null
        }
    } else {
        alert("Пожалуйста, разрешите использование веб камеры на сайте.")
    }
}


