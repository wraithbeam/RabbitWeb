let selectedWebcam = document.getElementById('chosen-webcam-img-id')
let chosenWebcam = document.getElementById('chosen-webcam-id')
let cancelButton = document.getElementById('cancel-button')
let observer

function changeWebcam(webcamNode) {
    if (observer){
        observer.disconnect()
    }

    selectedWebcam.style.display = 'block'
    chosenWebcam.style.display = 'none'
    cancelButton.style.display = 'block'

    observer = new MutationObserver((changes) => {
        changes.forEach(change => {
            if (change.attributeName.includes('src')) {
                selectedWebcam.src = webcamNode.src
            }
        });
    });
    observer.observe(webcamNode, {attributes: true});
}

cancelButton.onclick = function (){
    selectedWebcam.style.display = 'none'
    chosenWebcam.style.display = 'block'
    cancelButton.style.display = 'none'
}
