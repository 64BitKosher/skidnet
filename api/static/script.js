function handleSubmit(event) {
    event.preventDefault();
    let code = document.getElementById('code').value;
    console.log('Submitted code:', code);
    
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code }),
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        console.log('Response:', data);
        window.location.href = '/view/' + data.snippet_id;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    let submitButton = document.getElementById('submit-button');
    if (submitButton) {
        submitButton.addEventListener('click', handleSubmit);
    }
});