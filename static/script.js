let currentTab = 'basic';

function switchTab(tab) {
    currentTab = tab;
    
    // Tab butonlarını güncelle
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Panelleri göster/gizle
    document.getElementById('basic-calc').style.display = tab === 'basic' ? 'block' : 'none';
    document.getElementById('advanced-calc').style.display = tab === 'advanced' ? 'block' : 'none';
    
    clearDisplay();
}

async function calculate(operation) {
    const num1 = parseFloat(document.getElementById('num1').value);
    const num2 = parseFloat(document.getElementById('num2').value);
    
    if (isNaN(num1) || isNaN(num2)) {
        showError('Lütfen geçerli sayılar girin!');
        return;
    }
    
    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                num1: num1,
                num2: num2,
                operation: operation
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResult(data.expression, data.result);
            loadHistory();
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Sunucu hatası: ' + error.message);
    }
}

async function advancedCalc(operation) {
    const num = parseFloat(document.getElementById('advNum').value);
    
    if (isNaN(num)) {
        showError('Lütfen geçerli bir sayı girin!');
        return;
    }
    
    try {
        const response = await fetch('/api/advanced', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                num: num,
                operation: operation
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResult(data.expression, data.result);
            loadHistory();
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Sunucu hatası: ' + error.message);
    }
}

function displayResult(expression, result) {
    document.getElementById('expression').textContent = expression + ' =';
    document.getElementById('display').value = result.toFixed(6).replace(/\.?0+$/, '');
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const calculator = document.querySelector('.calculator');
    calculator.insertBefore(errorDiv, calculator.firstChild);
    
    setTimeout(() => errorDiv.remove(), 3000);
}

function clearDisplay() {
    document.getElementById('display').value = '0';
    document.getElementById('expression').textContent = '';
    
    if (currentTab === 'basic') {
        document.getElementById('num1').value = '';
        document.getElementById('num2').value = '';
    } else {
        document.getElementById('advNum').value = '';
    }
}

async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        if (data.success) {
            const historyList = document.getElementById('history-list');
            historyList.innerHTML = '';
            
            if (data.history.length === 0) {
                historyList.innerHTML = '<p style="text-align: center; color: #999;">Henüz hesaplama yok</p>';
                return;
            }
            
            data.history.forEach(item => {
                const historyItem = document.createElement('div');
                historyItem.className = 'history-item';
                historyItem.innerHTML = `
                    <span class="history-expression">${item.expression}</span>
                    <span class="history-result">= ${item.result.toFixed(6).replace(/\.?0+$/, '')}</span>
                `;
                historyList.appendChild(historyItem);
            });
        }
    } catch (error) {
        console.error('Geçmiş yüklenemedi:', error);
    }
}

async function clearHistory() {
    try {
        const response = await fetch('/api/history/clear', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            loadHistory();
        }
    } catch (error) {
        showError('Geçmiş temizlenemedi: ' + error.message);
    }
}

// Sayfa yüklendiğinde geçmişi yükle
document.addEventListener('DOMContentLoaded', loadHistory);

// Klavye kısayolları
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        if (currentTab === 'basic') {
            const lastFocused = document.activeElement;
            if (lastFocused.id === 'num1' || lastFocused.id === 'num2') {
                calculate('add');
            }
        }
    } else if (e.key === 'Escape') {
        clearDisplay();
    }
});