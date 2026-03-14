// utils.js — Shared helper functions for CoreInventory
// Version: March 2026 • Compatible with all pages

// ────────────────────────────────────────────────
// 1. Formatting Helpers
// ────────────────────────────────────────────────

/**
 * Format number as Indian Rupee currency (₹)
 * @param {number} amount 
 * @returns {string} e.g. "₹ 1,23,456.00"
 */
function formatINR(amount) {
  if (isNaN(amount) || amount == null) return '₹ 0.00';
  return '₹ ' + Number(amount).toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}

/**
 * Format date to readable Indian style
 * @param {string|Date} dateInput 
 * @param {boolean} includeTime 
 * @returns {string} e.g. "14 Mar 2026" or "14 Mar 2026, 09:34 AM"
 */
function formatDate(dateInput, includeTime = false) {
  if (!dateInput) return '—';
  const date = new Date(dateInput);
  if (isNaN(date)) return 'Invalid date';

  const options = {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  };

  if (includeTime) {
    options.hour = '2-digit';
    options.minute = '2-digit';
    options.hour12 = true;
  }

  return date.toLocaleDateString('en-IN', options)
    .replace(/,/g, ''); // remove comma after year if present
}

/**
 * Format datetime (short version)
 * @param {string|Date} dt 
 * @returns {string} e.g. "14/03/26 09:34"
 */
function formatDateTimeShort(dt) {
  if (!dt) return '—';
  const d = new Date(dt);
  if (isNaN(d)) return '—';
  return d.toLocaleString('en-IN', {
    day: '2-digit',
    month: '2-digit',
    year: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  }).replace(/,/, '');
}

// ────────────────────────────────────────────────
// 2. Toast / Notification Helpers
// ────────────────────────────────────────────────

/**
 * Show a temporary toast message at top-right
 * @param {string} message 
 * @param {string} type - 'success' | 'error' | 'warning' | 'info'
 * @param {number} durationMs 
 */
function showToast(message, type = 'info', durationMs = 4000) {
  const colors = {
    success: 'var(--success)',
    error:   'var(--danger)',
    warning: 'var(--warning)',
    info:    'var(--primary)'
  };

  const bg = colors[type] || 'var(--primary)';

  const toast = document.createElement('div');
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 14px 24px;
    background: ${bg};
    color: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    z-index: 9999;
    font-weight: 500;
    font-size: 0.98rem;
    opacity: 0;
    transform: translateY(-20px);
    transition: all 0.4s ease;
  `;

  document.body.appendChild(toast);

  // Fade in
  setTimeout(() => {
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';
  }, 100);

  // Fade out & remove
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-20px)';
    setTimeout(() => toast.remove(), 400);
  }, durationMs);
}

// ────────────────────────────────────────────────
// 3. Form Validation Helpers
// ────────────────────────────────────────────────

/**
 * Simple required field checker
 * @param {string[]} fieldIds 
 * @returns {boolean}
 */
function validateRequiredFields(fieldIds) {
  let valid = true;
  fieldIds.forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    if (!el.value.trim()) {
      el.style.borderColor = 'var(--danger)';
      valid = false;
    } else {
      el.style.borderColor = 'var(--border)';
    }
  });
  return valid;
}

/**
 * Check if two password fields match & meet min length
 * @param {string} pwdId 
 * @param {string} confirmId 
 * @param {number} minLength 
 * @returns {boolean}
 */
function validatePasswordMatch(pwdId, confirmId, minLength = 8) {
  const pwd = document.getElementById(pwdId)?.value || '';
  const conf = document.getElementById(confirmId)?.value || '';

  if (pwd.length < minLength) return false;
  if (pwd !== conf) return false;
  return true;
}

// ────────────────────────────────────────────────
// 4. DOM & Event Helpers
// ────────────────────────────────────────────────

/**
 * Debounce a function (useful for search inputs)
 * @param {Function} fn 
 * @param {number} delay 
 * @returns {Function}
 */
function debounce(fn, delay = 300) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

/**
 * Get query param from URL
 * @param {string} name 
 * @returns {string|null}
 */
function getQueryParam(name) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(name);
}

// ────────────────────────────────────────────────
// 5. Theme & Sidebar Persistence (used on almost every page)
// ────────────────────────────────────────────────

function initThemeAndSidebar() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
  }

  const savedCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
  if (savedCollapsed) {
    document.getElementById('sidebar')?.classList.add('collapsed');
  }
}

// Auto-init when script is loaded
initThemeAndSidebar();

// ────────────────────────────────────────────────
// Export (if using modules in future — optional)
// ────────────────────────────────────────────────

window.CoreUtils = {
  formatINR,
  formatDate,
  formatDateTimeShort,
  showToast,
  validateRequiredFields,
  validatePasswordMatch,
  debounce,
  getQueryParam
};

console.log('CoreInventory Utils loaded • ready for use');