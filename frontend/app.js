// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State Management
let authToken = localStorage.getItem('authToken');
let currentUser = localStorage.getItem('currentUser');

// DOM Elements
const loginScreen = document.getElementById('loginScreen');
const dashboardScreen = document.getElementById('dashboardScreen');
const loginForm = document.getElementById('loginForm');
const loginBtn = document.getElementById('loginBtn');
const loginError = document.getElementById('loginError');
const logoutBtn = document.getElementById('logoutBtn');
const currentUserElement = document.getElementById('currentUser');
const startProtocolBtn = document.getElementById('startProtocolBtn');
const resetBtn = document.getElementById('resetBtn');
const sensorNameInput = document.getElementById('sensorName');
const alarmStatus = document.getElementById('alarmStatus');
const sprinklerStatus = document.getElementById('sprinklerStatus');
const alarmIndicator = document.getElementById('alarmIndicator');
const sprinklerIndicator = document.getElementById('sprinklerIndicator');
const logContainer = document.getElementById('logContainer');
const toast = document.getElementById('toast');

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    if (authToken && currentUser) {
        showDashboard();
        fetchSystemStatus();
        startStatusPolling();
    } else {
        showLogin();
    }
});

// Screen Management
function showLogin() {
    loginScreen.classList.add('active');
    dashboardScreen.classList.remove('active');
}

function showDashboard() {
    loginScreen.classList.remove('active');
    dashboardScreen.classList.add('active');
    currentUserElement.textContent = `👤 ${currentUser}`;
}

// Login Handler
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    setLoading(loginBtn, true);
    hideError();

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            authToken = data.access_token;
            currentUser = data.kullanici;

            localStorage.setItem('authToken', authToken);
            localStorage.setItem('currentUser', currentUser);

            showToast('Giriş başarılı! Hoş geldiniz.', 'success');
            showDashboard();
            fetchSystemStatus();
            startStatusPolling();
        } else {
            showError(data.mesaj || 'Giriş başarısız');
        }
    } catch (error) {
        console.error('Login error:', error);
        showError('Sunucuya bağlanılamadı. Lütfen backend servisinin çalıştığından emin olun.');
    } finally {
        setLoading(loginBtn, false);
    }
});

// Logout Handler
logoutBtn.addEventListener('click', () => {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');

    showToast('Çıkış yapıldı', 'success');
    showLogin();
    stopStatusPolling();
});

// Start Fire Protocol
startProtocolBtn.addEventListener('click', async () => {
    const sensorName = sensorNameInput.value.trim() || 'Bilinmeyen_Sensör';

    setLoading(startProtocolBtn, true);

    try {
        const response = await fetch(`${API_BASE_URL}/yangin_uyarisi`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ kaynak: sensorName })
        });

        const data = await response.json();

        if (response.ok) {
            showToast('🔥 Yangın protokolü başlatıldı!', 'warning');
            addLog(`Yangın protokolü başlatıldı - Kaynak: ${sensorName}`, 'warning');
            addLog(`İşlemi yapan: ${data.islem_yapan_kullanici}`, 'info');

            if (data.protokol_akisi) {
                if (data.protokol_akisi.alarm) {
                    addLog(`Alarm: ${data.protokol_akisi.alarm.mesaj}`, 'success');
                }
                if (data.protokol_akisi.sprinkler_geri_bildirim) {
                    addLog(`Sprinkler: ${data.protokol_akisi.sprinkler_geri_bildirim.mesaj}`, 'success');
                }
            }

            // Refresh status
            setTimeout(() => fetchSystemStatus(), 500);
        } else {
            if (response.status === 401) {
                showToast('Oturum süresi doldu. Lütfen tekrar giriş yapın.', 'error');
                logoutBtn.click();
            } else {
                showToast(data.mesaj || 'İşlem başarısız', 'error');
                addLog(`Hata: ${data.mesaj}`, 'error');
            }
        }
    } catch (error) {
        console.error('Protocol start error:', error);
        showToast('Sunucuya bağlanılamadı', 'error');
        addLog('Sunucu bağlantı hatası', 'error');
    } finally {
        setLoading(startProtocolBtn, false);
    }
});

// Reset System
resetBtn.addEventListener('click', async () => {
    setLoading(resetBtn, true);

    try {
        const response = await fetch(`${API_BASE_URL}/sifirla`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (response.ok) {
            showToast('✅ Sistem sıfırlandı', 'success');
            addLog('Sistem sıfırlandı - Tüm bileşenler hazır durumda', 'success');

            // Refresh status
            setTimeout(() => fetchSystemStatus(), 500);
        } else {
            showToast(data.mesaj || 'Sıfırlama başarısız', 'error');
            addLog(`Hata: ${data.mesaj}`, 'error');
        }
    } catch (error) {
        console.error('Reset error:', error);
        showToast('Sunucuya bağlanılamadı', 'error');
        addLog('Sunucu bağlantı hatası', 'error');
    } finally {
        setLoading(resetBtn, false);
    }
});

// Fetch System Status
async function fetchSystemStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/durum`);
        const data = await response.json();

        if (response.ok) {
            updateStatusUI(data);
        }
    } catch (error) {
        console.error('Status fetch error:', error);
    }
}

// Update Status UI
function updateStatusUI(data) {
    if (data.AlarmSistemi) {
        const status = data.AlarmSistemi.durum;
        alarmStatus.textContent = status === 'Hazır' ? '✅ Hazır' : '🚨 Çalışıyor';
        alarmIndicator.className = 'status-indicator ' + (status === 'Hazır' ? 'ready' : 'active');
    }

    if (data.SprinklerSistemi) {
        const status = data.SprinklerSistemi.durum;
        sprinklerStatus.textContent = status === 'Hazır' ? '✅ Hazır' : '💧 Aktif';
        sprinklerIndicator.className = 'status-indicator ' + (status === 'Hazır' ? 'ready' : 'active');
    }
}

// Status Polling
let statusPollingInterval;

function startStatusPolling() {
    statusPollingInterval = setInterval(() => {
        fetchSystemStatus();
    }, 5000); // Poll every 5 seconds
}

function stopStatusPolling() {
    if (statusPollingInterval) {
        clearInterval(statusPollingInterval);
    }
}

// Activity Log
function addLog(message, type = 'info') {
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${type}`;

    const time = new Date().toLocaleTimeString('tr-TR');

    logEntry.innerHTML = `
        <span class="log-time">${time}</span>
        <span class="log-message">${message}</span>
    `;

    logContainer.insertBefore(logEntry, logContainer.firstChild);

    // Keep only last 50 entries
    while (logContainer.children.length > 50) {
        logContainer.removeChild(logContainer.lastChild);
    }
}

// Toast Notification
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// UI Helpers
function setLoading(button, loading) {
    const btnText = button.querySelector('.btn-text');
    const btnLoader = button.querySelector('.btn-loader');

    if (loading) {
        button.disabled = true;
        if (btnText) btnText.style.display = 'none';
        if (btnLoader) btnLoader.style.display = 'inline';
    } else {
        button.disabled = false;
        if (btnText) btnText.style.display = 'inline';
        if (btnLoader) btnLoader.style.display = 'none';
    }
}

function showError(message) {
    loginError.textContent = message;
    loginError.style.display = 'block';
}

function hideError() {
    loginError.style.display = 'none';
}

// Initial log entry
addLog('Sistem başlatıldı ve hazır durumda', 'info');
