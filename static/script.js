console.log("Oh, Hi there!")
displayMessage("Hello there!");
// document.addEventListener('DOMContentLoaded', () => {
//     displayMessage("Hello there!");
// })

chrome.tabs.onUpdated.addListener(console.log("Searching..."))

let message_width = 200

function displayMessage(message) {
    let div = document.createElement('div');
    div.style.zIndex = 9999;
    div.innerHTML = 
    `<div class = "extension-body" style = 'position:relative'>
        <button id = "close-message" class = "close-button" style = 'position:fixed; top:11px; right:11px; width:20px' > 
            X
        </button>
        <div>
            <b>${message}</b>
        </div>
    </div>`
    document.body.appendChild(div)
    console.log(document.URL)


    fetch('http://127.0.0.1:5000/post', {
        method: 'POST',
        headers: {
            "Content-type":"application/json"
        },
        body: JSON.stringify({
            url:document.URL
        })
    })
        .then(response => response.json())
        .then(data => {
            div.innerHTML = 
            `<div style = 'position:relative'>
                <button id = "close-message" class = "close-button" style = 'position:fixed; top:11px; right:11px; width:20px' > 
                    X
                </button>
                <div>
                    <b>${data.data}</b>
                </div>
            </div>`
            document.body.appendChild(div)

            document.getElementById('close-message').addEventListener('click', () => {
                message_width ? message_width = 0 : message_width = 400
                div.style.width = `${message_width}px`
                document.body.appendChild(div)
                console.log('pressed')
            })
        })
}