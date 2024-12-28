document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Reset error messages
    document.querySelectorAll('.error-message').forEach(error => {
        error.style.display = 'none';
    });

    let isValid = true;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Validate username
    if (!username) {
        showError('username-error', 'Username is required');
        isValid = false;
    } else if (username.length < 3) {
        showError('username-error', 'Username must be at least 3 characters long');
        isValid = false;
    }

    // Validate password
    if (!password) {
        showError('password-error', 'Password is required');
        isValid = false;
    } else if (password.length < 6) {
        showError('password-error', 'Password must be at least 6 characters long');
        isValid = false;
    }

    if (isValid) {
        // Here you would typically send the data to your server
        const formData = {
            username,
            password,
            remember: document.getElementById('remember').checked
        };
        
        console.log('Form submitted:', formData);
        alert('Login successful!');
        
        // Optional: Clear form after successful submission
        this.reset();
    }
});

// Helper function to show error messages
function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

// Add input event listeners for real-time validation
document.getElementById('username').addEventListener('input', function() {
    if (this.value.length >= 3) {
        document.getElementById('username-error').style.display = 'none';
    }
});

document.getElementById('password').addEventListener('input', function() {
    if (this.value.length >= 6) {
        document.getElementById('password-error').style.display = 'none';
    }
});