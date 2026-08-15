const API_BASE = ''; // Same domain

// State
let token = localStorage.getItem('access_token');
let user = null;

// DOM Elements
const authSection = document.getElementById('auth-section');
const dashboardSection = document.getElementById('dashboard-section');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const tabLogin = document.getElementById('tab-login');
const tabSignup = document.getElementById('tab-signup');
const apiList = document.getElementById('api-list');
const userDisplay = document.getElementById('user-display');
const toastEl = document.getElementById('toast');

// Utility: Show Toast
function showToast(message, type = 'success') {
    toastEl.textContent = message;
    toastEl.className = `toast show ${type}`;
    setTimeout(() => {
        toastEl.className = 'toast hidden';
    }, 3000);
}

// Check initial auth state
function checkAuth() {
    if (token) {
        // Assume valid for now, load dashboard
        authSection.classList.add('hidden');
        dashboardSection.classList.remove('hidden');
        loadAPIs();
        // In real app, fetch user profile to populate userDisplay
        userDisplay.textContent = 'Dashboard';
    } else {
        authSection.classList.remove('hidden');
        dashboardSection.classList.add('hidden');
    }
}

// Switch between Login and Signup tabs
function switchAuthTab(tab) {
    if (tab === 'login') {
        loginForm.classList.remove('hidden');
        signupForm.classList.add('hidden');
        tabLogin.classList.add('active');
        tabSignup.classList.remove('active');
    } else {
        signupForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
        tabSignup.classList.add('active');
        tabLogin.classList.remove('active');
    }
}

// API Calls
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    const formData = new URLSearchParams();
    formData.append('username', email); // OAuth2 requires 'username'
    formData.append('password', password);

    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });

        if (!res.ok) throw new Error((await res.json()).detail || 'Login failed');
        
        const data = await res.json();
        token = data.access_token;
        localStorage.setItem('access_token', token);
        showToast('Login successful!');
        checkAuth();
    } catch (err) {
        showToast(err.message, 'error');
    }
}

async function handleSignup(e) {
    e.preventDefault();
    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;

    try {
        const res = await fetch(`${API_BASE}/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });

        if (!res.ok) throw new Error((await res.json()).detail || 'Signup failed');
        
        showToast('Account created! Please login.');
        switchAuthTab('login');
    } catch (err) {
        showToast(err.message, 'error');
    }
}

function handleLogout() {
    token = null;
    localStorage.removeItem('access_token');
    checkAuth();
}

// Dashboard Functions
async function loadAPIs() {
    try {
        const res = await fetch(`${API_BASE}/apis/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) {
            if (res.status === 401) {
                handleLogout();
                return;
            }
            throw new Error('Failed to load APIs');
        }

        const apis = await res.json();
        renderAPIs(apis);
    } catch (err) {
        showToast(err.message, 'error');
    }
}

function renderAPIs(apis) {
    apiList.innerHTML = '';
    
    if (apis.length === 0) {
        apiList.innerHTML = `<p class="subtitle" style="grid-column: 1/-1; text-align: center; padding: 2rem;">You haven't created any APIs yet.</p>`;
        return;
    }

    apis.forEach(api => {
        const date = new Date(api.created_at).toLocaleDateString();
        const card = document.createElement('div');
        card.className = 'api-card fade-in';
        card.innerHTML = `
            <div class="api-card-header">
                <h3>${api.name}</h3>
                <span class="api-date">${date}</span>
            </div>
            <div class="keys-section">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4>API Keys</h4>
                    <button onclick="generateKey(${api.id})" class="btn-small">Generate Key</button>
                </div>
                <div id="keys-container-${api.id}">
                    <!-- Keys will appear here after generation (The backend doesn't seem to list keys, only create them, so we just show newly generated ones here) -->
                </div>
            </div>
        `;
        apiList.appendChild(card);
    });
}

function openModal(id) {
    document.getElementById(id).classList.remove('hidden');
}

function closeModal(id) {
    document.getElementById(id).classList.add('hidden');
}

async function handleCreateAPI(e) {
    e.preventDefault();
    const name = document.getElementById('new-api-name').value;

    try {
        const res = await fetch(`${API_BASE}/apis/`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ name })
        });

        if (!res.ok) throw new Error('Failed to create API');
        
        showToast('API Created successfully!');
        closeModal('create-api-modal');
        document.getElementById('new-api-name').value = '';
        loadAPIs();
    } catch (err) {
        showToast(err.message, 'error');
    }
}

async function generateKey(apiId) {
    try {
        const res = await fetch(`${API_BASE}/apis/${apiId}/keys/`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) throw new Error('Failed to generate key');
        
        const data = await res.json();
        
        const container = document.getElementById(`keys-container-${apiId}`);
        const keyItem = document.createElement('div');
        keyItem.className = 'key-item fade-in';
        keyItem.innerHTML = `
            <code>${data.raw_key}</code>
            <button class="btn-small" onclick="navigator.clipboard.writeText('${data.raw_key}'); showToast('Copied to clipboard!')">Copy</button>
        `;
        container.prepend(keyItem);
        showToast('New key generated!');
    } catch (err) {
        showToast(err.message, 'error');
    }
}

// Init
checkAuth();
