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
            if (savedStatus[checkbox.id]) {
                const vaccineItem = checkbox.closest('.vaccine-item');
                const dateSpan = vaccineItem.querySelector('.date-completed');
                
                checkbox.checked = true;
                checkbox.disabled = true;
                vaccineItem.classList.add('completed');
                dateSpan.textContent = savedStatus[checkbox.id].date;
            }
        });
        updateVaccineOptions();
    }

    function handleVaccineChange(e) {
        const checkbox = e.target;
        if (checkbox.checked) {
            markVaccine(checkbox);
        } else {
            e.preventDefault();
            checkbox.checked = true;
        }
    }

    function markVaccine(checkbox) {
        const vaccineItem = checkbox.closest('.vaccine-item');
        const dateSpan = vaccineItem.querySelector('.date-completed');
        const completedDate = new Date().toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });

        vaccineItem.classList.add('completed');
        checkbox.disabled = true;
        dateSpan.textContent = `Completed: ${completedDate}`;

        saveVaccinationStatus(checkbox.id, completedDate);
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

        vaccineCheckboxes.forEach(checkbox => {
            if (!checkbox.checked) {
                const label = checkbox.nextElementSibling.textContent;
                const option = document.createElement('option');
                option.value = checkbox.id;
                option.textContent = label;
                select.appendChild(option);
            }
        });
    }

    function saveVaccinationStatus(vaccineId, date) {
        const savedStatus = JSON.parse(localStorage.getItem('vaccinationStatus')) || {};
        savedStatus[vaccineId] = {
            date: date
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
            dateSpan.textContent = '';
        });

        updateProgress();
        updateVaccineOptions();
        alert('All vaccination records have been reset.');
    }

    function handleFormSubmit(e) {
        e.preventDefault();
        const vaccineId = document.getElementById('nextVaccine').value;
        if (vaccineId) {
            const checkbox = document.getElementById(vaccineId);
            if (checkbox) {
                checkbox.checked = true;
                markVaccine(checkbox);
            }
        }
        form.reset();
    }
});