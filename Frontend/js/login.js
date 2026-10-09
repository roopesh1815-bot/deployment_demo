const loginForm = document.getElementById("loginForm");
const rollnoInput = document.getElementById("rollno");
const passwordInput = document.getElementById("password");
const rememberMeInput = document.getElementById("rememberMe");
const togglePassword = document.getElementById("togglePassword");
const loginMessage = document.getElementById("loginMessage");

const savedRollNo = localStorage.getItem("studentPortalRollNo");
if (savedRollNo) {
    rollnoInput.value = savedRollNo;
    rememberMeInput.checked = true;
}

togglePassword.addEventListener("click", () => {
    passwordInput.type = passwordInput.type === "password" ? "text" : "password";
});

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const rollno = rollnoInput.value.trim();
    const password = passwordInput.value;

    if (!rollno || !password) {
        loginMessage.textContent = "Please enter your roll number and password.";
        loginMessage.style.color = "red";
        return;
    }

    if (rememberMeInput.checked) {
        localStorage.setItem("studentPortalRollNo", rollno);
    } else {
        localStorage.removeItem("studentPortalRollNo");
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                rollno: rollno,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            loginMessage.textContent = data.message || "Login successful.";
            loginMessage.style.color = "green";
            passwordInput.value = "";
        } else {
            loginMessage.textContent = data.detail || "Invalid roll number or password.";
            loginMessage.style.color = "red";
        }
    } catch (error) {
        console.error("Login error:", error);
        loginMessage.textContent = "Unable to connect to the server.";
        loginMessage.style.color = "red";
    }
});
