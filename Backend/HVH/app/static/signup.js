document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signupForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        if (validateForm()) {
            const userData = {
                username: document.getElementById('username').value,
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
            };

            // Send data to the backend
            fetch('http://localhost:3000/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
            })
                .then(response => {
                    if (response.ok) {
                        alert('Sign up successful!');
                        form.reset();
                    } else {
                        return response.json().then(data => {
                            alert(data.message || 'An error occurred during sign up.');
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Failed to sign up. Please try again later.');
                });
        }
    });
});

// The validateForm function remains unchanged


function validateForm() {
    // Reset errors
    document.querySelectorAll('.error').forEach(error => error.style.display = 'none');
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    let isValid = true;
    
    // Username validation
    if (username.length < 3) {
        showError('username-error', 'Username must be at least 3 characters long');
        isValid = false;
    }
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showError('email-error', 'Please enter a valid email address');
        isValid = false;
    }
    
    // Password validation
    if (password.length < 6) {
        showError('password-error', 'Password must be at least 6 characters long');
        isValid = false;
    }
    
    // Confirm password validation
    if (password !== confirmPassword) {
        showError('confirm-password-error', 'Passwords do not match');
        isValid = false;
    }
    
    if (!isValid) {
        shakeForm();
    }
    
    return isValid;
}

function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

function shakeForm() {
    const container = document.querySelector('.container');
    container.classList.add('shake');
    setTimeout(() => container.classList.remove('shake'), 300);
}

function handleSuccessfulSignup() {
    const container = document.querySelector('.container');
    container.classList.add('success');
    
    // Show success message
    alert('Sign up successful!');
    
    // Reset form
    document.getElementById('signupForm').reset();
    
    // Remove success animation
    setTimeout(() => container.classList.remove('success'), 500);
}

function redirectToLogin() {
    alert('Redirecting to login page...');
    // Add your login page redirect logic here
    // window.location.href = 'login.html';
}

function forgotPassword() {
    alert('Redirecting to password reset page...');
    // Add your forgot password logic here
    // window.location.href = 'reset-password.html';
}