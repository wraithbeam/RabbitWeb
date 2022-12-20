let input_message = document.getElementById('message-input')
let send_button = document.getElementById('bi-send-fill')
let messages = document.getElementById('messages')


const show_message = function (dataJson) {
    let initials = dataJson.initials
    let message = dataJson.message
    let id = dataJson.personId

    let outgoing = id === getPersonId();

    let newMessage = document.createElement('div')
    let newMessageSender = document.createElement('div')
    let newMessageInitials = document.createElement('div')
    let newMessageText = document.createElement('div')

    newMessage.classList.add('message')
    newMessageSender.classList.add('message-sender')
    newMessageInitials.classList.add('message-initials')
    newMessageText.classList.add('message-text')

    if (outgoing) {
        newMessage.classList.add('to-right')
        newMessageText.classList.add('send')
    } else {
        newMessage.classList.add('to-left')
        newMessageText.classList.add('receive')
    }

    newMessageText.innerText = message
    newMessageInitials.innerText = initials

    messages.appendChild(newMessage)
    newMessage.appendChild(newMessageSender)
    newMessage.appendChild(newMessageText)
    newMessageSender.appendChild(newMessageInitials)
}

send_button.onclick = function () {
    send_message()
}

input_message.addEventListener('keyup', function (e) {
    if (e.key === "Enter") {
        send_message()
    }
})

const send_message = function () {
    let text = input_message.value
    input_message.value = ''
    webSocket.send(JSON.stringify(
        {
            'type': 'message',
            'content': {
                'initials': getPersonInitials(),
                'message': text,
                'personId': getPersonId()
            }
        }
    ))
}