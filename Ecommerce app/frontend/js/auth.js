/**
 * auth.js — Authentication state management
 * Handles token/user storage and shared navbar rendering.
 */
const Auth = (() => {
  const TOKEN_KEY = 'access_token';
  const USER_KEY  = 'current_user';

  function saveToken(token, user) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  function getToken()  { return localStorage.getItem(TOKEN_KEY); }
  function getUser()   {
    try { return JSON.parse(localStorage.getItem(USER_KEY)); }
    catch { return null; }
  }
  function isLoggedIn() { return !!getToken(); }

  function logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  /** Render the shared navbar elements based on current auth state. */
  function renderNav() {
    const user = getUser();
    const loggedIn = isLoggedIn() && user;

    const btnLogin      = document.getElementById('btn-login');
    const btnRegNav     = document.getElementById('btn-register-nav');
    const btnLogout     = document.getElementById('btn-logout');
    const navUsername   = document.getElementById('nav-username');
    const navOrders     = document.getElementById('nav-orders');
    const navAdmin      = document.getElementById('nav-admin');
    const cartCount     = document.getElementById('cart-count');

    if (loggedIn) {
      if (btnLogin)    { btnLogin.classList.add('hidden'); }
      if (btnRegNav)   { btnRegNav.classList.add('hidden'); }
      if (btnLogout)   { btnLogout.classList.remove('hidden'); }
      if (navUsername) { navUsername.textContent = user.name; }
      if (navOrders)   { navOrders.classList.remove('hidden'); }
      if (navAdmin && user.role === 'admin') { navAdmin.classList.remove('hidden'); }
    } else {
      if (btnLogin)    { btnLogin.classList.remove('hidden'); }
      if (btnRegNav)   { btnRegNav.classList.remove('hidden'); }
      if (btnLogout)   { btnLogout.classList.add('hidden'); }
      if (navUsername) { navUsername.textContent = ''; }
      if (navOrders)   { navOrders.classList.add('hidden'); }
      if (navAdmin)    { navAdmin.classList.add('hidden'); }
    }

    // Logout handler
    if (btnLogout) {
      btnLogout.onclick = async () => {
        try { await API.post('/api/auth/logout', {}); } catch {}
        logout();
        window.location.href = '/login.html';
      };
    }
  }

  // Auto-render on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderNav);
  } else {
    renderNav();
  }

  return { saveToken, getToken, getUser, isLoggedIn, logout, renderNav };
})();
