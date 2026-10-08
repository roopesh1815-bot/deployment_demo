const registrationForm = document.getElementById("registrationForm");

const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirmPassword");

const togglePassword = document.getElementById("togglePassword");
const toggleConfirmPassword = document.getElementById("toggleConfirmPassword");

const registrationMessage = document.getElementById("registrationMessage");

// Show / hide password
togglePassword.addEventListener("click", () => {
    passwordInput.type =
        passwordInput.type === "password" ? "text" : "password";
});

toggleConfirmPassword.addEventListener("click", () => {
    confirmPasswordInput.type =
        confirmPasswordInput.type === "password" ? "text" : "password";
});


// Registration
registrationForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const rollno = document.getElementById("rollno").value.trim();
    const name = document.getElementById("name").value.trim();
    const className = document.getElementById("class").value.trim();
    const mobileno = document.getElementById("mobileno").value.trim();
    const emailid = document.getElementById("emailid").value.trim();
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    // Check passwords
    if (password !== confirmPassword) {
        registrationMessage.textContent = "Passwords do not match.";
        registrationMessage.style.color = "red";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                rollno: rollno,
                name: name,
                class_name: className,
                mobileno: mobileno,
                emailid: emailid,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            registrationMessage.textContent = data.message;
            registrationMessage.style.color = "green";

            // Redirect to login page
            setTimeout(() => {
                window.location.href = "index.html";
            }, 1000);

        } else {
            registrationMessage.textContent =
                data.detail || "Registration failed.";
            registrationMessage.style.color = "red";
        }

    } catch (error) {
        console.error("Registration error:", error);

        registrationMessage.textContent =
            "Unable to connect to the server.";
        registrationMessage.style.color = "red";
    }
});