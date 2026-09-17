// BloodLink - Interactive Scripts

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Hamburger Menu Toggle
  const hamburgerBtn = document.getElementById('hamburger-btn');
  const mobileNav = document.getElementById('mobile-nav');

  if (hamburgerBtn && mobileNav) {
    hamburgerBtn.addEventListener('click', () => {
      mobileNav.classList.toggle('open');
      const isOpen = mobileNav.classList.contains('open');
      hamburgerBtn.setAttribute('aria-expanded', isOpen);
    });

    // Close on click outside
    document.addEventListener('click', (e) => {
      if (!mobileNav.contains(e.target) && !hamburgerBtn.contains(e.target)) {
        mobileNav.classList.remove('open');
        hamburgerBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // 2. Toast Alert Auto-Dismissal and manual close
  const alertCloseButtons = document.querySelectorAll('.alert-close');
  alertCloseButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const alert = btn.closest('.alert');
      if (alert) {
        alert.style.opacity = '0';
        alert.style.transform = 'translateX(100%)';
        setTimeout(() => alert.remove(), 300);
      }
    });
  });

  // Auto-dismiss alerts after 5 seconds
  const autoAlerts = document.querySelectorAll('.alert');
  autoAlerts.forEach((alert) => {
    setTimeout(() => {
      if (alert && alert.parentElement) {
        alert.style.transition = 'all 0.4s ease';
        alert.style.opacity = '0';
        alert.style.transform = 'translateX(100%)';
        setTimeout(() => alert.remove(), 400);
      }
    }, 5000);
  });

  // 3. Quick confirmation for sensitive actions
  const confirmActionForms = document.querySelectorAll('form[data-confirm]');
  confirmActionForms.forEach((form) => {
    form.addEventListener('submit', (e) => {
      const message = form.getAttribute('data-confirm') || 'Are you sure you want to proceed?';
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  });

  // 4. Password Show / Hide Toggle (Event Delegation)
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.password-toggle');
    if (!btn) return;
    e.preventDefault();
    const wrapper = btn.closest('.password-wrapper');
    if (!wrapper) return;
    const input = wrapper.querySelector('input');
    if (!input) return;
    
    const eyeShow = btn.querySelector('.eye-show');
    const eyeHide = btn.querySelector('.eye-hide');

    if (input.type === 'password') {
      input.type = 'text';
      btn.setAttribute('aria-label', 'Hide password');
      if (eyeShow) eyeShow.style.display = 'none';
      if (eyeHide) eyeHide.style.display = 'block';
    } else {
      input.type = 'password';
      btn.setAttribute('aria-label', 'Show password');
      if (eyeShow) eyeShow.style.display = 'block';
      if (eyeHide) eyeHide.style.display = 'none';
    }
  });
});

// Standalone function for inline onclick support
function togglePassword(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const eyeShow = btn.querySelector('.eye-show');
  const eyeHide = btn.querySelector('.eye-hide');

  if (input.type === 'password') {
    input.type = 'text';
    btn.setAttribute('aria-label', 'Hide password');
    if (eyeShow) eyeShow.style.display = 'none';
    if (eyeHide) eyeHide.style.display = 'block';
  } else {
    input.type = 'password';
    btn.setAttribute('aria-label', 'Show password');
    if (eyeShow) eyeShow.style.display = 'block';
    if (eyeHide) eyeHide.style.display = 'none';
  }
}
window.togglePassword = togglePassword;
