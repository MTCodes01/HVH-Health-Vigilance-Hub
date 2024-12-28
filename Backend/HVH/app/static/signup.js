document.getElementById('signupForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/signup/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken() // Include CSRF token
        },
        body: JSON.stringify({ username, email, password })
    });

    const result = await response.json();

    if (response.ok) {
        console.log(result);
        localStorage.setItem('LOGGED_IN', 'true');
        localStorage.setItem('USERNAME', username);
        window.location.href = '/query/';
    } else {
        alert(result.error || 'An error occurred.');
    }
});

// Function to get CSRF token
function getCSRFToken() {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
}
