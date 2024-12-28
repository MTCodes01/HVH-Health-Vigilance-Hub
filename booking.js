document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const vaccineCheckboxes = document.querySelectorAll('.vaccine-checkbox');
    const progressFill = document.querySelector('.progress-fill');
    const progressText = document.querySelector('.progress-text');
    const form = document.getElementById('vaccinationForm');

    // Create and add reset button
    const resetButton = document.createElement('button');
    resetButton.textContent = 'Reset All Vaccinations';
    resetButton.className = 'reset-button';
    document.querySelector('.container').appendChild(resetButton);

    // Initialize the tracker
    initializeTracker();
    updateProgress();
    startDateCheck();

    // Event Listeners
    vaccineCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', handleVaccineChange);
    });

    resetButton.addEventListener('click', confirmReset);
    form.addEventListener('submit', handleFormSubmit);

    // Functions
    function initializeTracker() {
        const savedStatus = JSON.parse(localStorage.getItem('vaccinationStatus')) || {};
        
        vaccineCheckboxes.forEach(checkbox => {
            if (savedStatus[checkbox.id]?.completed) {
                const vaccineItem = checkbox.closest('.vaccine-item');
                const dateSpan = vaccineItem.querySelector('.date-completed');
                
                checkbox.checked = true;
                checkbox.disabled = true;
                vaccineItem.classList.add('completed');
                dateSpan.textContent = savedStatus[checkbox.id].completedDate;
            } else if (savedStatus[checkbox.id]?.scheduledDate) {
                const dateSpan = checkbox.closest('.vaccine-item').querySelector('.date-completed');
                dateSpan.textContent = `Scheduled: ${new Date(savedStatus[checkbox.id].scheduledDate).toLocaleDateString()}`;
            }
        });
        updateVaccineOptions();
    }

    function startDateCheck() {
        // Check for due vaccinations every minute
        setInterval(checkScheduledVaccinations, 60000);
        // Also check immediately on load
        checkScheduledVaccinations();
    }

    function checkScheduledVaccinations() {
        const savedStatus = JSON.parse(localStorage.getItem('vaccinationStatus')) || {};
        const currentDate = new Date();
        
        vaccineCheckboxes.forEach(checkbox => {
            const vaccineStatus = savedStatus[checkbox.id];
            if (vaccineStatus?.scheduledDate && !vaccineStatus.completed) {
                const scheduledDate = new Date(vaccineStatus.scheduledDate);
                const vaccineItem = checkbox.closest('.vaccine-item');
                
                // Enable checkbox if scheduled date has passed
                if (scheduledDate <= currentDate) {
                    checkbox.disabled = false;
                    vaccineItem.style.backgroundColor = '#e8f5e9';
                    const dateSpan = vaccineItem.querySelector('.date-completed');
                    dateSpan.textContent = `Ready for completion (Scheduled: ${scheduledDate.toLocaleDateString()})`;
                }
            }
        });
    }

    function handleVaccineChange(e) {
        const checkbox = e.target;
        if (checkbox.checked) {
            const savedStatus = JSON.parse(localStorage.getItem('vaccinationStatus')) || {};
            const vaccineStatus = savedStatus[checkbox.id];
            
            if (!vaccineStatus?.scheduledDate) {
                e.preventDefault();
                checkbox.checked = false;
                alert('Please schedule this vaccination first.');
                return;
            }

            const scheduledDate = new Date(vaccineStatus.scheduledDate);
            const currentDate = new Date();
            
            if (scheduledDate > currentDate) {
                e.preventDefault();
                checkbox.checked = false;
                alert(`This vaccination cannot be marked as complete until ${scheduledDate.toLocaleDateString()}`);
                return;
            }

            markVaccine(checkbox, currentDate.toISOString());
        } else {
            e.preventDefault();
            checkbox.checked = true;
        }
    }

    function markVaccine(checkbox, completedDate) {
        const vaccineItem = checkbox.closest('.vaccine-item');
        const dateSpan = vaccineItem.querySelector('.date-completed');

        const formattedDate = new Date(completedDate).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });

        vaccineItem.classList.add('completed');
        checkbox.disabled = true;
        dateSpan.textContent = `Completed: ${formattedDate}`;

        saveVaccinationCompletion(checkbox.id, formattedDate, completedDate);
        updateProgress();
        updateVaccineOptions();
    }

    function updateProgress() {
        const total = vaccineCheckboxes.length;
        const completed = document.querySelectorAll('.vaccine-checkbox:checked').length;
        const percentage = (completed / total) * 100;

        progressFill.style.width = `${percentage}%`;
        progressText.textContent = `${completed} of ${total} vaccines completed (${percentage.toFixed(1)}%)`;
    }

    function updateVaccineOptions() {
        const select = document.getElementById('nextVaccine');
        select.innerHTML = '<option value="">Choose vaccine...</option>';

        const savedStatus = JSON.parse(localStorage.getItem('vaccinationStatus')) || {};
        
        vaccineCheckboxes.forEach(checkbox => {
            if (!checkbox.checked && !savedStatus[checkbox.id]?.scheduledDate) {
                const label = checkbox.nextElementSibling.textContent;
                const option = document.createElement('option');
                option.value = checkbox.id;
                option.textContent = label;
                select.appendChild(option);
            }
        });
    }

    function saveVaccinationCompletion(vaccineId, displayDate, completedDate) {
        const savedStatus = JSON.parse(localStorage.getItem('vaccinationStatus')) || {};
        savedStatus[vaccineId] = {
            ...savedStatus[vaccineId],
            completedDate: displayDate,
            completed: true
        };
        localStorage.setItem('vaccinationStatus', JSON.stringify(savedStatus));
    }

    function confirmReset() {
        if (confirm('Are you sure you want to reset all vaccination records? This cannot be undone.')) {
            resetAllVaccinations();
        }
    }

    function resetAllVaccinations() {
        localStorage.removeItem('vaccinationStatus');
        
        vaccineCheckboxes.forEach(checkbox => {
            const vaccineItem = checkbox.closest('.vaccine-item');
            const dateSpan = vaccineItem.querySelector('.date-completed');
            
            checkbox.checked = false;
            checkbox.disabled = false;
            vaccineItem.classList.remove('completed');
            vaccineItem.style.backgroundColor = '';
            dateSpan.textContent = '';
        });

        updateProgress();
        updateVaccineOptions();
        alert('All vaccination records have been reset.');
    }

    function handleFormSubmit(e) {
        e.preventDefault();
        
        const childName = document.getElementById('childName').value;
        const vaccineId = document.getElementById('nextVaccine').value;
        const scheduledDate = document.getElementById('appointmentDate').value;

        if (vaccineId && scheduledDate) {
            // Validate that scheduled date is not in the past
            const selectedDate = new Date(scheduledDate);
            const currentDate = new Date();
            currentDate.setHours(0, 0, 0, 0); // Reset time part for proper date comparison

            if (selectedDate < currentDate) {
                alert('Please select a future date for the vaccination.');
                return;
            }

            const savedStatus = JSON.parse(localStorage.getItem('vaccinationStatus')) || {};
            savedStatus[vaccineId] = {
                scheduledDate: scheduledDate,
                childName: childName,
                completed: false
            };
            localStorage.setItem('vaccinationStatus', JSON.stringify(savedStatus));

            const vaccineItem = document.getElementById(vaccineId).closest('.vaccine-item');
            const dateSpan = vaccineItem.querySelector('.date-completed');
            dateSpan.textContent = `Scheduled: ${selectedDate.toLocaleDateString()}`;
        }
        
        updateVaccineOptions();
        form.reset();
        alert(`Vaccination scheduled for ${childName} on ${new Date(scheduledDate).toLocaleDateString()}`);
    }
});