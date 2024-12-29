document.addEventListener('DOMContentLoaded', () => {
    // Define the keys expected in localStorage based on the provided storage structure
    const keys = [
        "USERNAME", "firstName", "lastName", "age", "gender", "currentAddress", "permanentAddress", "healthCondition", "emergencyContact"
    ];

    // Check if the keys exist in localStorage and update the profile sections
    keys.forEach(key => {
        const value = localStorage.getItem(key);

        if (value) {
            if (key === "emergencyContact") {
                // Parse emergency contact information
                const emergencyContact = JSON.parse(value);
                document.querySelector('[data-key="emergency-name"]').textContent = emergencyContact.name;
                document.querySelector('[data-key="emergency-phone"]').textContent = emergencyContact.phone;
                document.querySelector('[data-key="emergency-relation"]').textContent = emergencyContact.relation;
            } else {
                const element = document.querySelector(`[data-key="${key}"]`);
                if (element) {
                    element.textContent = value;
                }
            }
        }
    });
});
