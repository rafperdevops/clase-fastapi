const API_URL = 'http://localhost:8000';
let currentEmail = '';

document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    setupForms();
});

function checkAuth() {
    const token = localStorage.getItem('authToken');
    if (token) {
        window.location.href = 'index.html';
    }
}

function setupForms() {
    const emailForm = document.getElementById('email-form');
    const otpForm = document.getElementById('otp-form');
    const resetBtn = document.getElementById('reset-btn');

    emailForm.addEventListener('submit', requestOTP);
    otpForm.addEventListener('submit', verifyOTP);
    resetBtn.addEventListener('click', resetToEmail);
}

function requestOTP(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    currentEmail = email;

    fetch(`${API_URL}/auth/request-otp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
    })
    .then(response => response.json())
    .then(data => {
        showMessage('email-message', 'Código enviado a tu correo', 'success');
        document.getElementById('step-email').style.display = 'none';
        document.getElementById('step-otp').style.display = 'block';
    })
    .catch(error => {
        showMessage('email-message', 'Error: ' + error.message, 'error');
    });
}

function verifyOTP(e) {
    e.preventDefault();
    const otp = document.getElementById('otp').value;

    fetch(`${API_URL}/auth/verify-otp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: currentEmail, otp })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Código inválido'); });
        }
        return response.json();
    })
    .then(data => {
        localStorage.setItem('authToken', data.token);
        localStorage.setItem('userEmail', data.email);
        window.location.href = 'index.html';
    })
    .catch(error => {
        showMessage('otp-message', 'Error: ' + error.message, 'error');
    });
}

function resetToEmail() {
    document.getElementById('step-otp').style.display = 'none';
    document.getElementById('step-email').style.display = 'block';
    document.getElementById('email-message').style.display = 'none';
    document.getElementById('otp-message').style.display = 'none';
}

function showMessage(elementId, text, type) {
    const el = document.getElementById(elementId);
    el.textContent = text;
    el.className = `message ${type}`;
    el.style.display = 'block';
    
    setTimeout(() => {
        el.style.display = 'none';
    }, 5000);
}