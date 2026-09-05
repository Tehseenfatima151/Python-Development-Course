/**
 * orders.js — Order history page logic
 */
(function () {
  if (!document.getElementById('orders-container')) return;
  if (!Auth.isLoggedIn()) { window.location.href = '/login.html'; return; }

  const container = document.getElementById('orders-container');

  function statusBadge(status) {
    const map = {
      paid:      'badge-success',
      pending:   'badge-warning',
      failed:    'badge-danger',
      cancelled: 'badge-secondary',
    };
    return `<span class="badge ${map[status] || 'badge-secondary'}">${status.toUpperCase()}</span>`;
  }

  async function loadOrders() {
    try {
      const data = await API.get('/api/orders');
      const orders = data.data.orders;

      if (!orders.length) {
        container.innerHTML = `
          <div class="cart-empty">
            <div class="cart-empty-icon">📦</div>
            <h3>No orders yet</h3>
            <p>Once you complete a purchase your orders will appear here.</p>
            <a href="/index.html" class="btn btn-primary mt-2">Start Shopping</a>
          </div>`;
        return;
      }

      container.innerHTML = orders.map(o => `
        <div class="card order-card">
          <div class="card-body">
            <div class="order-header">
              <div>
                <div class="order-id">Order <strong>#${o.id}</strong></div>
                <div class="order-meta">${new Date(o.created_at).toLocaleDateString('en-US', { year:'numeric', month:'long', day:'numeric' })}</div>
              </div>
              <div style="display:flex;align-items:center;gap:1rem;">
                ${statusBadge(o.status)}
                <span class="order-total">$${o.total_amount.toFixed(2)}</span>
                <button class="btn btn-ghost btn-sm" onclick="viewOrder(${o.id})">View Details</button>
              </div>
            </div>
          </div>
        </div>`).join('');
    } catch (err) {
      container.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
    }
  }

  window.viewOrder = async (orderId) => {
    const modal = document.getElementById('order-modal');
    const modalBody = document.getElementById('modal-body');
    const modalTitle = document.getElementById('modal-title');
    modalTitle.textContent = `Order #${orderId}`;
    modalBody.innerHTML = '<div class="loading-overlay" style="padding:2rem;"><div class="spinner spinner-dark"></div></div>';
    modal.classList.add('open');

    try {
      const data = await API.get(`/api/orders/${orderId}`);
      const o = data.data.order;

      const itemsHtml = o.items.map(item => `
        <tr>
          <td>${item.product_name}</td>
          <td style="text-align:center;">${item.quantity}</td>
          <td style="text-align:right;">$${item.price.toFixed(2)}</td>
          <td style="text-align:right;font-weight:700;">$${item.subtotal.toFixed(2)}</td>
        </tr>`).join('');

      modalBody.innerHTML = `
        <div style="display:flex;gap:.75rem;align-items:center;margin-bottom:1rem;flex-wrap:wrap;">
          ${statusBadge(o.status)}
          <span style="color:var(--gray-500);font-size:.88rem;">${new Date(o.created_at).toLocaleString()}</span>
        </div>
        <div class="table-wrap" style="margin-bottom:1rem;">
          <table>
            <thead><tr>
              <th>Product</th><th style="text-align:center;">Qty</th>
              <th style="text-align:right;">Price</th><th style="text-align:right;">Subtotal</th>
            </tr></thead>
            <tbody>${itemsHtml}</tbody>
          </table>
        </div>
        <div style="text-align:right;">
          <span style="font-size:1.2rem;font-weight:800;color:var(--primary);">
            Total: $${o.total_amount.toFixed(2)}
          </span>
        </div>
        ${o.stripe_session_id ? `<p style="font-size:.78rem;color:var(--gray-400);margin-top:.75rem;">Stripe Session: ${o.stripe_session_id}</p>` : ''}`;
    } catch (err) {
      modalBody.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
    }
  };

  window.closeModal = () => {
    document.getElementById('order-modal').classList.remove('open');
  };

  // Close modal on backdrop click
  document.getElementById('order-modal').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) closeModal();
  });

  loadOrders();
})();
