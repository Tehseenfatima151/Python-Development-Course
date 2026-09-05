/**
 * cart.js — Cart operations and badge management
 * Exposes the Cart object globally so other modules can use it.
 */
const Cart = (() => {

  async function addItem(productId, quantity = 1) {
    return await API.post('/api/cart/items', { product_id: productId, quantity });
  }

  async function updateItem(productId, quantity) {
    return await API.put(`/api/cart/items/${productId}`, { quantity });
  }

  async function removeItem(productId) {
    return await API.delete(`/api/cart/items/${productId}`);
  }

  async function clearCart() {
    return await API.delete('/api/cart');
  }

  async function getCart() {
    return await API.get('/api/cart');
  }

  /** Update the cart badge in the navbar. */
  async function refreshBadge() {
    const badge = document.getElementById('cart-count');
    if (!badge) return;
    if (!Auth.isLoggedIn()) { badge.classList.add('hidden'); return; }
    try {
      const data = await getCart();
      const count = data.data.cart.item_count || 0;
      if (count > 0) {
        badge.textContent = count > 99 ? '99+' : count;
        badge.classList.remove('hidden');
      } else {
        badge.classList.add('hidden');
      }
    } catch {
      badge.classList.add('hidden');
    }
  }

  // Refresh badge on every page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', refreshBadge);
  } else {
    refreshBadge();
  }

  return { addItem, updateItem, removeItem, clearCart, getCart, refreshBadge };
})();
