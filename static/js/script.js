/**
 * Script JavaScript principale per l'applicazione Interrogazioni Programmate
 * Gestisce le interazioni client-side e le chiamate AJAX
 */

/**
 * Mostra un alert dinamico nella pagina
 * 
 * @param {string} message - Messaggio da visualizzare
 * @param {string} type - Tipo di alert (success, danger, warning, info)
 * @param {number} duration - Durata in millisecondi (default: 4000)
 */
function showAlert(message, type = 'info', duration = 4000) {
    const alertContainer = $('#alert-container');
    
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="bi bi-${getAlertIcon(type)}"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.append(alertHtml);
    
    // Auto-dismiss dopo la durata specificata
    setTimeout(() => {
        alertContainer.find('.alert').first().fadeOut(400, function() {
            $(this).remove();
        });
    }, duration);
}

/**
 * Restituisce l'icona appropriata per il tipo di alert
 * 
 * @param {string} type - Tipo di alert
 * @returns {string} Nome dell'icona Bootstrap
 */
function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle-fill',
        'danger': 'exclamation-triangle-fill',
        'warning': 'exclamation-circle-fill',
        'info': 'info-circle-fill'
    };
    return icons[type] || 'info-circle-fill';
}

/**
 * Formatta una data in formato leggibile
 * 
 * @param {string} dateString - Stringa data ISO
 * @returns {string} Data formattata
 */
function formatDate(dateString) {
    if (!dateString) return '-';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('it-IT', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Valida un numero di registro
 * 
 * @param {number} registro - Numero di registro
 * @returns {boolean} True se valido
 */
function validateRegistro(registro) {
    return Number.isInteger(registro) && registro > 0;
}

/**
 * Valida un nome o cognome
 * 
 * @param {string} name - Nome da validare
 * @returns {boolean} True se valido
 */
function validateName(name) {
    return typeof name === 'string' && name.trim().length > 0;
}

/**
 * Conferma azione con modal Bootstrap personalizzato
 * 
 * @param {string} message - Messaggio di conferma
 * @param {Function} onConfirm - Callback se confermato
 */
function confirmAction(message, onConfirm) {
    if (confirm(message)) {
        onConfirm();
    }
}

/**
 * Gestisce errori AJAX generici
 * 
 * @param {object} xhr - Oggetto XMLHttpRequest
 * @param {string} status - Status della richiesta
 * @param {string} error - Messaggio di errore
 */
function handleAjaxError(xhr, status, error) {
    console.error('AJAX Error:', status, error);
    
    let errorMessage = 'Si è verificato un errore nella comunicazione con il server';
    
    if (xhr.responseJSON && xhr.responseJSON.error) {
        errorMessage = xhr.responseJSON.error;
    } else if (xhr.status === 404) {
        errorMessage = 'Risorsa non trovata';
    } else if (xhr.status === 500) {
        errorMessage = 'Errore interno del server';
    }
    
    showAlert(errorMessage, 'danger');
}

/**
 * Imposta handler globali per AJAX
 */
$(document).ready(function() {
    // Setup AJAX error handler globale
    $(document).ajaxError(function(event, xhr, settings, error) {
        if (xhr.status !== 200 && !settings.suppressErrors) {
            handleAjaxError(xhr, xhr.statusText, error);
        }
    });
    
    // Setup CSRF token per tutte le richieste AJAX (se necessario)
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            // Se hai bisogno di CSRF protection, aggiungi qui il token
        }
    });
    
    // Attiva i tooltip Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Attiva i popover Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

/**
 * Utility per salvare dati in sessionStorage con encoding JSON
 * 
 * @param {string} key - Chiave
 * @param {*} value - Valore da salvare
 */
function saveToSession(key, value) {
    try {
        sessionStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
        console.error('Error saving to sessionStorage:', e);
    }
}

/**
 * Utility per recuperare dati da sessionStorage con parsing JSON
 * 
 * @param {string} key - Chiave
 * @returns {*} Valore recuperato o null
 */
function getFromSession(key) {
    try {
        const item = sessionStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    } catch (e) {
        console.error('Error reading from sessionStorage:', e);
        return null;
    }
}

/**
 * Utility per rimuovere dati da sessionStorage
 * 
 * @param {string} key - Chiave da rimuovere
 */
function removeFromSession(key) {
    try {
        sessionStorage.removeItem(key);
    } catch (e) {
        console.error('Error removing from sessionStorage:', e);
    }
}

/**
 * Debounce function per limitare chiamate frequenti
 * 
 * @param {Function} func - Funzione da debounce
 * @param {number} wait - Millisecondi di attesa
 * @returns {Function} Funzione con debounce
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function per limitare esecuzioni
 * 
 * @param {Function} func - Funzione da throttle
 * @param {number} limit - Millisecondi limite
 * @returns {Function} Funzione con throttle
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Copia testo negli appunti
 * 
 * @param {string} text - Testo da copiare
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('Copiato negli appunti!', 'success', 2000);
        }).catch(err => {
            console.error('Error copying to clipboard:', err);
            showAlert('Errore nella copia', 'danger');
        });
    } else {
        // Fallback per browser più vecchi
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            showAlert('Copiato negli appunti!', 'success', 2000);
        } catch (err) {
            console.error('Error copying to clipboard:', err);
            showAlert('Errore nella copia', 'danger');
        }
        document.body.removeChild(textarea);
    }
}

/**
 * Genera un ID univoco
 * 
 * @returns {string} ID univoco
 */
function generateUniqueId() {
    return '_' + Math.random().toString(36).substr(2, 9);
}

/**
 * Sanitizza input HTML per prevenire XSS
 * 
 * @param {string} str - Stringa da sanitizzare
 * @returns {string} Stringa sanitizzata
 */
function sanitizeHTML(str) {
    const temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML;
}

/**
 * Controlla se l'applicazione è online
 * 
 * @returns {boolean} True se online
 */
function isOnline() {
    return navigator.onLine;
}

// Event listener per status online/offline
window.addEventListener('online', () => {
    showAlert('Connessione ristabilita', 'success', 3000);
});

window.addEventListener('offline', () => {
    showAlert('Connessione persa - Alcune funzionalità potrebbero non essere disponibili', 'warning', 5000);
});

/**
 * Esporta funzioni per uso globale
 */
window.showAlert = showAlert;
window.formatDate = formatDate;
window.validateRegistro = validateRegistro;
window.validateName = validateName;
window.confirmAction = confirmAction;
window.saveToSession = saveToSession;
window.getFromSession = getFromSession;
window.removeFromSession = removeFromSession;
window.copyToClipboard = copyToClipboard;
window.sanitizeHTML = sanitizeHTML;
