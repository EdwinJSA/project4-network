function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(';').shift();
}


function saveChanges(id){
    const textareaValue = document.getElementById(`textarea_${id}`).value;
    fetch(`/edit/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({'content': textareaValue})
    })
    .then(response => {
        console.log(response);
        if (!response.ok) {
            console.error(`Network response was not ok. Status: ${response.status}`);
            return response.text();
        }
        return response.json();
    })
    .then(result => {
        console.log(result);
    })
    .catch(error => {
        console.error('Error during fetch:', error);
    });
    
    
} 
