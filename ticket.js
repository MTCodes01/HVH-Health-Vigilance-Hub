// Hospital departments data
const departments = {
    'city-general': ['General Medicine', 'Cardiology', 'Orthopedics', 'Pediatrics'],
    'apollo': ['General Medicine', 'Neurology', 'Dermatology', 'ENT'],
    'fortis': ['General Medicine', 'Oncology', 'Gynecology', 'Psychiatry']
};

// Doctors data
const doctors = {
    'general-medicine': ['Dr. John Smith', 'Dr. Sarah Johnson', 'Dr. Michael Brown'],
    'cardiology': ['Dr. Robert Wilson', 'Dr. Emily Davis'],
    'orthopedics': ['Dr. James Anderson', 'Dr. Lisa Taylor'],
    'pediatrics': ['Dr. David Miller', 'Dr. Jennifer White'],
    'neurology': ['Dr. Richard Lee', 'Dr. Mary Clark'],
    'dermatology': ['Dr. Thomas Moore', 'Dr. Patricia Hall'],
    'ent': ['Dr. Charles Wilson', 'Dr. Elizabeth Martin'],
    'oncology': ['Dr. William Turner', 'Dr. Susan Adams'],
    'gynecology': ['Dr. Karen Lewis', 'Dr. Margaret Wright'],
    'psychiatry': ['Dr. Joseph Baker', 'Dr. Nancy Green']
};

// Event Listeners
document.getElementById('hospital').addEventListener('change', updateDepartments);
document.getElementById('department').addEventListener('change', updateDoctors);
document.getElementById('preferredDate').addEventListener('change', checkAvailability);
document.getElementById('ticketForm').addEventListener('submit', handleFormSubmit);

// Update departments based on selected hospital
function updateDepartments() {
    const hospitalSelect = document.getElementById('hospital');
    const departmentSelect = document.getElementById('department');
    const selectedHospital = hospitalSelect.value;

    departmentSelect.innerHTML = '<option value="">Select department</option>';

    if (selectedHospital) {
        departments[selectedHospital].forEach(dept => {
            const option = document.createElement('option');
            option.value = dept.toLowerCase().replace(' ', '-');
            option.textContent = dept;
            departmentSelect.appendChild(option);
        });
    }
}

// Update doctors based on selected department
function updateDoctors() {
    const departmentSelect = document.getElementById('department');
    const doctorSelect = document.getElementById('doctor');
    const selectedDepartment = departmentSelect.value;

    doctorSelect.innerHTML = '<option value="">Select doctor</option>';

    if (selectedDepartment && doctors[selectedDepartment]) {
        doctors[selectedDepartment].forEach(doc => {
            const option = document.createElement('option');
            option.value = doc.toLowerCase().replace(' ', '-');
            option.textContent = doc;
            doctorSelect.appendChild(option);
        });
    }
}

// Generate time slots
function generateTimeSlots() {
    const slots = [];
    for (let hour = 9; hour <= 16; hour++) {
        slots.push(`${hour}:00`);
        slots.push(`${hour}:30`);
    }
    return slots;
}

// Check availability and show time slots
function checkAvailability() {
    const hospital = document.getElementById('hospital').value;
    const department = document.getElementById('department').value;
    const date = document.getElementById('preferredDate').value;

    if (hospital && department && date) {
        const availabilitySection = document.getElementById('availabilitySection');
        const timeSlotsDiv = document.getElementById('timeSlots');
        availabilitySection.style.display = 'block';
        timeSlotsDiv.innerHTML = '';

        const timeSlots = generateTimeSlots();
        timeSlots.forEach(slot => {
            const slotDiv = document.createElement('div');
            slotDiv.className = 'time-slot';
            slotDiv.textContent = slot;
            slotDiv.onclick = function() {
                document.querySelectorAll('.time-slot').forEach(s => s.classList.remove('selected'));
                this.classList.add('selected');
            };
            timeSlotsDiv.appendChild(slotDiv);
        });
    }
}

// Generate unique ticket number
function generateTicketNumber() {
    const prefix = 'OP';
    const timestamp = new Date().getTime().toString().slice(-6);
    const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
    return `${prefix}-${timestamp}-${random}`;
}

// Handle form submission
function handleFormSubmit(e) {
    e.preventDefault();
    
    const selectedTimeSlot = document.querySelector('.time-slot.selected');
    if (!selectedTimeSlot) {
        alert('Please select a time slot');
        return;
    }

    // Get form values
    const formData = {
        hospital: document.getElementById('hospital'),
        department: document.getElementById('department'),
        doctor: document.getElementById('doctor'),
        firstName: document.getElementById('firstName').value,
        lastName: document.getElementById('lastName').value,
        dob: document.getElementById('dob').value,
        gender: document.getElementById('gender').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value,
        address: document.getElementById('address').value,
        symptoms: document.getElementById('symptoms').value,
        date: document.getElementById('preferredDate').value,
        timeSlot: selectedTimeSlot.textContent
    };

    // Get selected conditions
    const selectedConditions = Array.from(document.querySelectorAll('input[name="conditions"]:checked'))
        .map(checkbox => checkbox.value)
        .join(', ');
}