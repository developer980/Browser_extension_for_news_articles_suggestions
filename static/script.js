// const request = require('request')

console.log("Oh, Hi there!")
displayMessage("Searching...");
// document.addEventListener('DOMContentLoaded', () => {
//     displayMessage("Hello there!");
// })

// chrome.tabs.onUpdated.addListener(console.log("Hellloooooo!"))

let message_width = 200

function displayMessage(message) {
    let div = document.createElement('div');
    console.log("HELLO THERE!")
    div.id = 'ext'
    div.className = "extension-body"
    div.style.zIndex = 9998;
    div.innerHTML = 
    `<div style = 'position:relative'>
        <button id = "close-message" class = "close-button" style = '' >     
            X
        </button>
        <div>
            ${message}
        </div>
    </div>`
    document.body.appendChild(div)
    console.log(document.URL)
    url = document.URL
    // request(url, (err, res, html) => {
    //     if (!err && response.statusCode == 200) {
    //         const $ = cheerio.load(html)

    //     }
    // })

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
            console.log(data)
            // percentage = math
            div.innerHTML = 
            `<div style = 'position:relative'>
                <button id = "close-message" class = "close-button"> 
                    X
                </button>
                <div class = 'extension-content'>
                    <div>
                        This article seems ${Math.round(data.percentage)} % similar to this article: <a href = "${data.highest_perc.href}">${data.highest_perc.text}</a>
                    </div>
                    <div class = 'title'>
                        Here are some related articles:
                    </div>
                    <div id = "list">
                    </div>
                </div>
            </div>`
            document.body.appendChild(div)
            for (let i = 0; i < data.suggestions.length; i++){
                let link = data.suggestions[i]
                let item = document.createElement('div')
                let punctuation = ';'
                if (i == data.suggestions.length - 1) {
                    punctuation = ""
                }

                item.className = 'list-item'
                item.innerHTML = `
                    <a href = "${link.link_href}">${link.link_text}${punctuation}</a>
                `
                document.getElementById('list').appendChild(item)
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