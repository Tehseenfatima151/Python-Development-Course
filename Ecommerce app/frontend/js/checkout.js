/**
 * checkout.js — Checkout page logic
 * Loads the cart summary and initiates Stripe Checkout.
 */
(function () {
  if (!document.getElementById('checkout-container')) return;
  if (!Auth.isLoggedIn()) { window.location.href = '/login.html'; return; }

  const container = document.getElementById('checkout-container');
  const errorDiv  = document.getElementById('checkout-error');
  const errorText = document.getElementById('checkout-error-text');

  function showError(msg) {
    errorText.textContent = msg;
    errorDiv.classList.add('show');
    window.scrollTo(0, 0);
  }

  async function loadCheckout() {
    try {
      const data = await API.get('/api/cart');
      const cart = data.data.cart;

      if (!cart.items || cart.items.length === 0) {
        container.innerHTML = `
          <div class="cart-empty">
            <div class="cart-empty-icon">🛒</div>
            <h3>Your cart is empty</h3>
            <p>Add some products before checking out.</p>
            <a href="/index.html" class="btn btn-primary mt-2">Browse Products</a>
          </div>`;
        return;
      }

      const itemsHtml = cart.items.map(item => `
        <div class="order-summary-item">
          <span>${item.product_name} <span style="color:var(--gray-400);font-size:.85rem;">× ${item.quantity}</span></span>
          <span><strong>$${item.subtotal.toFixed(2)}</strong></span>
        </div>`).join('');

      container.innerHTML = `
        <div class="checkout-grid">
          <!-- Left: order summary -->
          <div class="card">
            <div class="card-header">
              <h2 style="font-size:1.1rem;">Order Summary</h2>
            </div>
            <div class="card-body">
              ${itemsHtml}
              <div class="summary-total">
                <span>Total</span>
                <span style="color:var(--primary);">$${cart.total.toFixed(2)}</span>
              </div>
            </div>
          </div>

          <!-- Right: pay panel -->
          <div>
            <div class="card">
              <div class="card-body">
                <h2 style="font-size:1.1rem;margin-bottom:1rem;">Secure Payment</h2>
                <p style="font-size:.9rem;color:var(--gray-600);margin-bottom:1.25rem;">
                  You will be redirected to Stripe's secure checkout page.
                  No card details are handled by this server.
                </p>
                <div style="background:var(--gray-50);border:1px solid var(--gray-200);border-radius:var(--radius-sm);padding:1rem;margin-bottom:1.25rem;font-size:.88rem;color:var(--gray-600);">
                  <strong style="display:block;margin-bottom:.4rem;">🔒 Test Mode Active</strong>
                  Use card <code style="background:var(--primary-light);padding:.1rem .3rem;border-radius:3px;">4242 4242 4242 4242</code>
                  with any future expiry and any 3-digit CVC.
                </div>
                <button class="btn btn-primary btn-lg btn-full" id="pay-btn">
                  💳 Pay $${cart.total.toFixed(2)} with Stripe
                </button>
                <div class="stripe-badge">
                  🔒 Secured by <strong>Stripe</strong>
                </div>
              </div>
            </div>
          </div>
        </div>`;

      document.getElementById('pay-btn').addEventListener('click', startCheckout);
    } catch (err) {
      container.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
    }
  }

  async function startCheckout() {
    const btn = document.getElementById('pay-btn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Preparing checkout…';

    try {
      const data = await API.post('/api/payments/create-checkout-session', {});
      // Redirect to Stripe Checkout
      window.location.href = data.data.checkout_url;
    } catch (err) {
      showError(err.message || 'Failed to start checkout. Please try again.');
      btn.disabled = false;
      btn.textContent = `💳 Pay with Stripe`;
    }
  }

  loadCheckout();
})();
