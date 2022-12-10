var mic_io = document.getElementById('mic-io')
var mic_on_icon = document.getElementById('mic-icon-on')
var mic_off_icon = document.getElementById("mic-icon-off")
var is_mic_on = false

var disconnect = document.getElementById('call-off-io')

mic_io.onclick = function () {
    is_mic_on = !is_mic_on
    if (is_mic_on) {
        mic_on_icon.style.display = "none"
        mic_off_icon.style.display = "block"
    } else {
        mic_on_icon.style.display = "block"
        mic_off_icon.style.display = "none"
    }
}

disconnect.onclick = function () {
    window.location.href = 'http://localhost:8000';
}