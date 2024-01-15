function Like(id, youLiked){
    const button = document.getElementById(`${id}`)
    button.classList.remove('fa-thumbs-up')
    button.classList.remove('fa-thumbs-down')

    if(youLiked.includes(id)){
        var liked = true
    } else {
        var liked = false
    }

    if (liked === true){
        console.log(id + "Entro al IF")
        fetch(`/unlike/${id}`)
        .then(response=>{
            return response.text()
        }).then(result => { // ejecuta
            console.log(result);
            //button.classList.add('fa-thumbs-up')
        })
    } else {
        console.log(id + "Entro al ELSE")
        fetch(`/like/${id}`)
        .then(response=>response.json())
        .then(result => {
            button.classList.add('fa-thumbs-down')
        }) // haber ejecutalo
    }
    liked = !liked
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(';').shift();
}


function saveChanges(id){
    const textareaValue = document.getElementById(`textarea_${id}`).value;
    const mariconada = document.getElementById(`content_${id}`);
    const modal = document.getElementById(`modal_edit_post_${id}`);

    fetch(`/edit/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({content: textareaValue})
    })
    .then(result => {
        console.log(result)
        console.log(textareaValue)
        mariconada.innerHTML = textareaValue
        modal.classList.remove('show')
        modal.setAttribute('aria-hidden', 'true')
        modal.setAttribute('style', 'display: none')

        const modalsBackdrops = document.getElementsByClassName('modal-backdrop')
        for (let i = 0; i < modalsBackdrops.length; i++) {
            document.body.removeChild(modalsBackdrops[i])
        }
    })
} 

