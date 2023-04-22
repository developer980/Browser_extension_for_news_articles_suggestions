// const request = require('request')

// document.addEventListener('DOMContentLoaded', () => {
//     displayMessage("Hello there!");
// })

// chrome.tabs.onUpdated.addListener(console.log("Hellloooooo!"))
console.log("Oh, Hi there!")
displayMessage("Searching...");

let message_width = 200

function displayMessage(message) {
    let div = document.createElement('div');
    console.log("HELLO THERE!")
    div.id = 'ext'
    div.className = "extension-body"
    div.style.zIndex = 9998;
    url = document.URL

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
            console.log("data:")
            console.log(data)
        // percentage = math
            const image = document.createElement('img')
            
            img_url = chrome.runtime.getURL('static/icons/x.svg')
                
            image.src = img_url
            console.log("URL: " + img_url)

            if (data.message != 'none') {
                div.innerHTML =
                    `<div style = 'position:relative'>
                    <button id = "close-message" class = "close-button">
                    </button>
                    <div class = 'extension-content'>
                            <div>
                                This article seems <b>${Math.round(data.percentage)} %</b> similar to this article: <a class = "suggestion-link" href = "${data.highest_perc.href}">${data.highest_perc.text}</a>
                            </div>
                            <div class = 'title'>
                                <div><b>Here are some related articles taken from trusted sources:</b></div>
                            </div>
                            <div id = "list">
                            </div>
                    </div>
                </div>`



                document.body.appendChild(div)

                document.getElementById('close-message').appendChild(image)

                // document.getElementById('close-message').appendChild(image)

                for (let i = 0; i < data.suggestions.length; i++) {
                    let link = data.suggestions[i]
                    let item = document.createElement('div')
                    let punctuation = ';'
                    if (i == data.suggestions.length - 1) {
                        punctuation = "."
                    }

                    item.className = 'list-item'
                    item.style.color = "rgb(56, 70, 95)";
                    // item
                    item.innerHTML = `
                        <a class = "suggestion-link" href = "${link.link_href}">${link.link_text}</a>${punctuation}
                    `
                    document.getElementById('list').appendChild(item)
                }
            }

            else {
                // div.innerHTML = "<p>Doesn't seem to be a news article</p>"
                document.body.removeChild(div)
            }

            document.getElementById('close-message').addEventListener('click', () => {
                document.getElementById('ext').style.display = 'none'
                // message_width ? message_width = 0 : message_width = 400
                // div.style.width = `${message_width}px`
                // document.body.appendChild(div)
                // console.log('pressed')
            })
        })
}