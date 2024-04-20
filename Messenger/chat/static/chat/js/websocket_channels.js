const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/chat/'
    + chatPk
    + '/'
);

window.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('messages-container')
    messagesContainer.scroll({ top: messagesContainer.scrollHeight, behavior: 'smooth' })
})

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data)
    const messagesContainer = document.getElementById('messages-container')    
    messagesContainer.insertAdjacentHTML('beforeend', `
    <div class="w-75 d-flex flex-row ms-auto justify-content-end mt-1 mb-2 me-1" style="min-height: 50px;">
        <div class="d-flex flex-column justify-content-end" style="max-width: 80%;">
            <p class="mb-0 border rounded bg-secondary text-break">${data.messageText}</p>
            <p class="mb-0 align-self-end">${data.messageTime}</p>
        </div>
        <div class="d-flex flex-column flex-end align-items-center" style="width: 20%">
            <img class="rounded-circle" src="${data.userAvatarPath}" alt="user's avatar" style="width: 50px; height: 50px;">
            <p class="mb-0 text-break" style="font-size: smaller;">${data.username}</p>
        </div>
    </div>
    `)
    messagesContainer.scroll({ top: messagesContainer.scrollHeight, behavior: 'smooth' })
    const message_text = document.getElementById('message_text')
    message_text.value = ''
}

let submitBtn = document.getElementById('message_send')
submitBtn.addEventListener('click', () => {
    let messageText = document.getElementById('message_text').value
    chatSocket.send(JSON.stringify({
        'messageText': messageText,
        'chatPk': chatPk
    }))
})