window.onload = openConnection // open websoket connection

let form = document.getElementById('message-form')
form.addEventListener('submit', )
let formData = new FormData(form)
let messageText = formData.get('message_text')

function openConnection() {
    let websocket = new WebSocket(`ws://localhost:8000/chat/${chatPk}`)
    websocket.onopen = function(event) {
        alert('Connected');
        alert(messageText);
    }
    websocket.onerror = function(event) {
        alert('Error');
    }
}

// function sendMessage()