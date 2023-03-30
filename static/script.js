const button = document.getElementById('post')
const input = document.getElementById('url_input')
let url = ''

input.addEventListener('input', () => {
    url = document.getElementById('url_input').value
    console.log(url)
})

button.addEventListener('click', () => {
    console.log(url)
    fetch("http://127.0.0.1:5000/post", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'url': url})
    }).then(() => {
        fetch("http://127.0.0.1:5000/post")
            .then(response => response.json())
            .then(data => console.log(data))
    })
})