document.addEventListener('DOMContentLoaded', () => {
    // Load stored form data
    const formData = JSON.parse(localStorage.getItem("formData")) || {};
    
    // Map form data to input fields
    if (formData) {
        // Personal Information
        if (formData.firstName) document.getElementById('firstName').value = formData.firstName;
        if (formData.lastName) document.getElementById('lastName').value = formData.lastName;
        // if (formData.dob) document.getElementById('dob').value = formData.dob;
        if (formData.gender) {
            const genderSelect = document.getElementById('gender');
            const options = Array.from(genderSelect.options).map(option => option);
            for (const option of options) {
                if (option.value === formData.gender) {
                    option.setAttribute('selected'); 
                    break;
                }
            }
        }
        if (formData.emergencyContact.phone) document.getElementById('phone').value = formData.emergencyContact.phone;
        if (localStorage.getItem('EMAIL')) document.getElementById('email').value = localStorage.getItem('EMAIL');
        if (formData.permanentAddress) document.getElementById('address').value = formData.permanentAddress;
        
        // Medical Information
        // if (formData.symptoms) document.getElementById('symptoms').value = formData.symptoms;
        // if (formData.previousHistory) document.getElementById('previousHistory').value = formData.previousHistory;
    }

    // Save form data to localStorage when form fields change
    // const formElements = document.querySelectorAll('#ticketForm input, #ticketForm select, #ticketForm textarea');
    // formElements.forEach(element => {
    //     element.addEventListener('change', () => {
    //         const currentFormData = {
    //             // Appointment Details
    //             hospital: document.getElementById('hospital').value,
    //             preferredDate: document.getElementById('preferredDate').value,
                
    //             // Personal Information
    //             firstName: document.getElementById('firstName').value,
    //             lastName: document.getElementById('lastName').value,
    //             dob: document.getElementById('dob').value,
    //             gender: document.getElementById('gender').value,
    //             phone: document.getElementById('phone').value,
    //             email: document.getElementById('email').value,
    //             address: document.getElementById('address').value,
                
    //             // Medical Information
    //             symptoms: document.getElementById('symptoms').value,
    //             previousHistory: document.getElementById('previousHistory').value
    //         };
            
    //         localStorage.setItem("formData", JSON.stringify(currentFormData));
    //     });
    // });

    // Handle ticket generation
    const handleTicketGeneration = async (formData) => {
        try {
            const response = await fetch('/ticket/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Failed to save ticket data');
            }

            const data = await response.json();
            
            // Replace page content with generated ticket
            document.body.innerHTML = `
                <div class="ticket-view-container">
                    <div class="ticket-card">
                        <div class="header">
                            <h1>Hospital OP Ticket</h1>
                            <div class="ticket-number">Ticket #${data.ticket_id}</div>
                        </div>
                        
                        <div class="info-section">
                            <h2>Appointment Details</h2>
                            <div class="info-grid">
                                <div class="info-item">
                                    <label>Hospital</label>
                                    <span>${formData.hospital}</span>
                                </div>
                                <div class="info-item">
                                    <label>Appointment Date</label>
                                    <span>${new Date(formData.preferredDate).toLocaleDateString()}</span>
                                </div>
                            </div>
                            
                            <h2>Personal Information</h2>
                            <div class="info-grid">
                                <div class="info-item">
                                    <label>Name</label>
                                    <span>${formData.firstName} ${formData.lastName}</span>
                                </div>
                                <div class="info-item">
                                    <label>Date of Birth</label>
                                    <span>${new Date(formData.dob).toLocaleDateString()}</span>
                                </div>
                                <div class="info-item">
                                    <label>Gender</label>
                                    <span>${formData.gender}</span>
                                </div>
                                <div class="info-item">
                                    <label>Phone</label>
                                    <span>${formData.phone}</span>
                                </div>
                                <div class="info-item">
                                    <label>Email</label>
                                    <span>${formData.email}</span>
                                </div>
                                <div class="info-item">
                                    <label>Address</label>
                                    <span>${formData.address}</span>
                                </div>
                            </div>
                            
                            <h2>Medical Information</h2>
                            <div class="info-grid">
                                <div class="info-item">
                                    <label>Symptoms</label>
                                    <span>${formData.symptoms}</span>
                                </div>
                                <div class="info-item">
                                    <label>Previous Medical History</label>
                                    <span>${formData.previousHistory || 'None'}</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="footer">
                            <div class="timestamp">Generated on: ${new Date().toLocaleString()}</div>
                            <div class="actions">
                                <button onclick="window.print()" class="print-btn">Print Ticket</button>
                                <button onclick="window.location.reload()" class="new-btn">New Ticket</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        } catch (error) {
            console.error('Error generating ticket:', error);
            alert('Failed to generate ticket. Please try again.');
        }
    };

    // Handle form submission
    const ticketForm = document.getElementById('ticketForm');
    if (ticketForm) {
        ticketForm.addEventListener('submit', (event) => {
            event.preventDefault();
            
            // Collect current form data
            const formData = {
                hospital: document.getElementById('hospital').value,
                preferredDate: document.getElementById('preferredDate').value,
                firstName: document.getElementById('firstName').value,
                lastName: document.getElementById('lastName').value,
                dob: document.getElementById('dob').value,
                gender: document.getElementById('gender').value,
                phone: document.getElementById('phone').value,
                email: document.getElementById('email').value,
                address: document.getElementById('address').value,
                symptoms: document.getElementById('symptoms').value,
                previousHistory: document.getElementById('previousHistory').value
            };

            const ticketEndpoint = '/ticket/';
            navigator.geolocation.getCurrentPosition((position) => {
                fetch(ticketEndpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken() // Include CSRF token
                    },
                    body: JSON.stringify({
                        symptoms: formData.symptoms,
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude
                    })
                })
            .then((response) => response.json())
            .then((data) => {
                console.log('Ticket generated:', data);
            })
            .catch((error) => {
                console.error('Error generating ticket:', error);
            });

            // Generate ticket
            handleTicketGeneration(formData);
            });
        });
    }
});

function getCSRFToken() {
    const cookie = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : null;
}
