let currentQuestion = 1;
const totalQuestions = 5;

function nextQuestion(current) {
    // Validate current question before moving to next
    if (current === 1) {
        const firstName = document.getElementById("first-name").value;
        const lastName = document.getElementById("last-name").value;
        if (!firstName || !lastName) {
            alert("Please enter your full name.");
            return;
        }
    }

    if (current === 2) {
        const age = document.getElementById("age").value;
        const gender = document.querySelector('input[name="gender"]:checked');
        if (!age || !gender) {
            alert("Please enter your age and select your gender.");
            return;
        }
        if (age < 0 || age > 120) {
            alert("Please enter a valid age.");
            return;
        }
    }

    if (current === 3) {
        const currentAddress = document.getElementById("current-address").value;
        const permanentAddress = document.getElementById("permanent-address").value;
        if (!currentAddress || !permanentAddress) {
            alert("Please enter both current and permanent addresses.");
            return;
        }
    }

    if (current === 4) {
        const healthCondition = document.querySelector('input[name="health"]:checked');
        if (!healthCondition) {
            alert("Please select a health condition option.");
            return;
        }
        if (healthCondition.value === "Other") {
            const otherHealth = document.getElementById("health-other-input").value;
            if (!otherHealth) {
                alert("Please specify your health condition.");
                return;
            }
        }
    }

    // Hide current question
    document.getElementById(`q${current}`).classList.remove("active");
    currentQuestion++;
    document.getElementById(`q${currentQuestion}`).classList.add("active");
    updateProgress();
}

function previousQuestion(current) {
    document.getElementById(`q${current}`).classList.remove("active");
    currentQuestion--;
    document.getElementById(`q${currentQuestion}`).classList.add("active");
    updateProgress();
}

function updateProgress() {
    const progress = (currentQuestion / totalQuestions) * 100;
    document.getElementById("progress").style.width = progress + "%";
}

function handleHealthChange(value) {
    const otherInput = document.getElementById("health-other");
    if (value === "Other") {
        otherInput.classList.add("active");
    } else {
        otherInput.classList.remove("active");
    }
}

async function fetchLocations(query) {
    const suggestionsBox = document.getElementById("location-suggestions");
    suggestionsBox.innerHTML = "";
    if (query.length < 2) {
        suggestionsBox.style.display = "none";
        return;
    }

    try {
        const response = await fetch(`https://api.example.com/locations?q=${query}`);
        const data = await response.json();
        if (data.length > 0) {
            suggestionsBox.style.display = "block";
            data.forEach(location => {
                const suggestion = document.createElement("div");
                suggestion.classList.add("suggestion-item");
                suggestion.textContent = location.name;
                suggestion.onclick = () => selectLocation(location.name);
                suggestionsBox.appendChild(suggestion);
            });
        }
    } catch (error) {
        console.error("Error fetching locations:", error);
    }
}

function selectLocation(location) {
    const activeInput = document.activeElement;
    if (activeInput) {
        activeInput.value = location;
    }
    document.getElementById("location-suggestions").style.display = "none";
}

function submitForm() {
    // Validate emergency contact information
    const emergencyName = document.getElementById("emergency-name").value;
    const emergencyPhone = document.getElementById("emergency-phone").value;
    const emergencyRelation = document.getElementById("emergency-relation").value;

    if (!emergencyName || !emergencyPhone || !emergencyRelation) {
        alert("Please fill in all emergency contact information.");
        return;
    }

    // Phone number validation
    const phoneRegex = /^\d{10}$/;
    if (!phoneRegex.test(emergencyPhone)) {
        alert("Please enter a valid 10-digit phone number.");
        return;
    }

    // If all validations pass, show thank you message
    document.querySelector(".query-container").style.display = "none";
    document.getElementById("thank-you").style.display = "flex";
    
    // Here you would typically send the data to your backend
    const formData = {
        firstName: document.getElementById("first-name").value,
        lastName: document.getElementById("last-name").value,
        age: document.getElementById("age").value,
        gender: document.querySelector('input[name="gender"]:checked').value,
        currentAddress: document.getElementById("current-address").value,
        permanentAddress: document.getElementById("permanent-address").value,
        healthCondition: document.querySelector('input[name="health"]:checked').value,
        emergencyContact: {
            name: emergencyName,
            phone: emergencyPhone,
            relation: emergencyRelation
        }
    };

    console.log("Form Data:", formData);
}