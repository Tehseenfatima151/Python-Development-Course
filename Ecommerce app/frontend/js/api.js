/**
 * api.js — Centralized HTTP client
 * All API calls go through this module. It attaches the JWT token,
 * handles non-2xx responses, and returns parsed JSON data.
 */
const API = (() => {
  const BASE = '';   // Same origin — Flask serves both API and frontend

  function getToken() {
    return localStorage.getItem('access_token');
  }

  function buildHeaders(extra = {}) {
    const headers = { 'Content-Type': 'application/json', ...extra };
    const token = getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;
    return headers;
  }

  async function request(method, path, body = null) {
    const opts = {
      method,
      headers: buildHeaders(),
    };
    if (body !== null) opts.body = JSON.stringify(body);

    let res;
    try {
      res = await fetch(BASE + path, opts);
    } catch (networkErr) {
      throw { message: 'Network error — is the server running?', status: 0 };
    }

    let json;
    try {
      json = await res.json();
    } catch {
      throw { message: `Server returned non-JSON response (${res.status})`, status: res.status };
    }

    if (!res.ok) {
      // If JWT expired, clear auth and redirect to login
      if (res.status === 401) {
        const errCode = json.error;
        if (errCode === 'TOKEN_EXPIRED' || errCode === 'TOKEN_INVALID' || errCode === 'TOKEN_MISSING') {
          Auth.logout();
          window.location.href = '/login.html';
        }
      }
      const err = new Error(json.message || `Request failed (${res.status})`);
      err.status = res.status;
      err.errors = json.errors;
      err.error = json.error;
      throw err;
    }

    return json;
  }

  return {
    get:    (path)           => request('GET',    path),
    post:   (path, body)     => request('POST',   path, body),
    put:    (path, body)     => request('PUT',    path, body),
    patch:  (path, body)     => request('PATCH',  path, body),
    delete: (path)           => request('DELETE', path),
  };
})();
