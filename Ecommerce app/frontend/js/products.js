/**
 * products.js — Product listing page logic (index.html)
 * Handles search, filter, sort, pagination, and add-to-cart.
 */

(function () {
  // Only run on the index page
  if (!document.getElementById('products-container')) return;

  let currentPage = 1;
  let currentSearch = '';
  let currentCategory = '';
  let currentSort = 'created_at';
  let currentOrder = 'desc';
  let searchTimer = null;

  // ---- DOM refs ----
  const container   = document.getElementById('products-container');
  const pagination  = document.getElementById('pagination');
  const searchInput = document.getElementById('search-input');
  const catFilter   = document.getElementById('category-filter');
  const sortSelect  = document.getElementById('sort-select');
  const countEl     = document.getElementById('filter-count');

  // ---- Event listeners ----
  searchInput.addEventListener('input', () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      currentSearch = searchInput.value.trim();
      currentPage = 1;
      loadProducts();
    }, 350);
  });

  catFilter.addEventListener('change', () => {
    currentCategory = catFilter.value;
    currentPage = 1;
    loadProducts();
  });

  sortSelect.addEventListener('change', () => {
    const [col, dir] = sortSelect.value.split(':');
    currentSort = col;
    currentOrder = dir;
    currentPage = 1;
    loadProducts();
  });

  // ---- Load categories for the filter dropdown ----
  async function loadCategories() {
    try {
      const data = await API.get('/api/products?per_page=100');
      const categories = [...new Set(data.data.products.map(p => p.category).filter(Boolean))].sort();
      categories.forEach(cat => {
        const opt = document.createElement('option');
        opt.value = cat;
        opt.textContent = cat;
        catFilter.appendChild(opt);
      });
    } catch {}
  }

  // ---- Main product loader ----
  async function loadProducts() {
    container.innerHTML = '<div class="loading-overlay"><div class="spinner spinner-dark"></div><span>Loading…</span></div>';

    const params = new URLSearchParams({
      page: currentPage,
      per_page: 12,
      sort_by: currentSort,
      order: currentOrder,
    });
    if (currentSearch)   params.set('search', currentSearch);
    if (currentCategory) params.set('category', currentCategory);

    try {
      const data = await API.get(`/api/products?${params}`);
      const { products, pagination: pager } = data.data;

      if (countEl) countEl.textContent = `${pager.total} product${pager.total !== 1 ? 's' : ''}`;

      if (!products.length) {
        container.innerHTML = `
          <div class="cart-empty">
            <div class="cart-empty-icon">🔍</div>
            <h3>No products found</h3>
            <p>Try a different search term or category.</p>
          </div>`;
        pagination.innerHTML = '';
        return;
      }

      container.innerHTML = `<div class="products-grid">${products.map(renderCard).join('')}</div>`;
      renderPagination(pager);
      attachCartButtons();
    } catch (err) {
      container.innerHTML = `<div class="alert alert-danger"><span class="alert-icon">❌</span> Failed to load products: ${err.message}</div>`;
    }
  }

  function renderCard(p) {
    const stockInfo = p.stock === 0
      ? '<span class="product-stock out">✕ Out of stock</span>'
      : p.stock < 5
        ? `<span class="product-stock low">⚠ Only ${p.stock} left</span>`
        : `<span class="product-stock">✓ In stock (${p.stock})</span>`;

    const imgHtml = p.image_url
      ? `<img src="${p.image_url}" alt="${p.name}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=product-image-placeholder>🛒</div>'">`
      : '<div class="product-image-placeholder">🛒</div>';

    return `
      <div class="product-card">
        <a href="/product.html?id=${p.id}" style="text-decoration:none;color:inherit;">
          <div class="product-image-wrap">${imgHtml}</div>
          <div class="product-body">
            ${p.category ? `<span class="product-category">${p.category}</span>` : ''}
            <div class="product-name">${p.name}</div>
            <div class="product-desc">${p.description || ''}</div>
          </div>
        </a>
        <div class="product-footer">
          <div>
            <div class="product-price">$${p.price.toFixed(2)}</div>
            ${stockInfo}
          </div>
          ${p.stock > 0
            ? `<button class="btn btn-primary btn-sm add-cart-btn" data-id="${p.id}" data-name="${p.name}">+ Cart</button>`
            : '<button class="btn btn-ghost btn-sm" disabled>Sold out</button>'}
        </div>
      </div>`;
  }

  function attachCartButtons() {
    document.querySelectorAll('.add-cart-btn').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        if (!Auth.isLoggedIn()) { window.location.href = '/login.html'; return; }
        const productId = parseInt(btn.dataset.id);
        const origText = btn.textContent;
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span>';
        try {
          await Cart.addItem(productId, 1);
          Cart.refreshBadge();
          btn.innerHTML = '✓ Added';
          btn.classList.remove('btn-primary');
          btn.classList.add('btn-success');
          setTimeout(() => {
            btn.innerHTML = origText;
            btn.classList.remove('btn-success');
            btn.classList.add('btn-primary');
            btn.disabled = false;
          }, 1800);
        } catch (err) {
          btn.disabled = false;
          btn.textContent = origText;
          showFlash('error', err.message);
        }
      });
    });
  }

  function renderPagination(pager) {
    if (pager.pages <= 1) { pagination.innerHTML = ''; return; }
    let html = '';
    html += `<button class="page-btn" ${!pager.has_prev ? 'disabled' : ''} onclick="goPage(${pager.page - 1})">‹</button>`;
    for (let i = 1; i <= pager.pages; i++) {
      if (pager.pages > 7 && Math.abs(i - pager.page) > 2 && i !== 1 && i !== pager.pages) {
        if (i === 2 || i === pager.pages - 1) html += '<span style="padding:0 .3rem;color:var(--gray-400);">…</span>';
        continue;
      }
      html += `<button class="page-btn ${i === pager.page ? 'active' : ''}" onclick="goPage(${i})">${i}</button>`;
    }
    html += `<button class="page-btn" ${!pager.has_next ? 'disabled' : ''} onclick="goPage(${pager.page + 1})">›</button>`;
    pagination.innerHTML = html;
  }

  window.goPage = (page) => { currentPage = page; loadProducts(); window.scrollTo(0, 0); };

  function showFlash(type, msg) {
    const el = document.getElementById(type === 'error' ? 'flash-error' : 'flash-success');
    const text = document.getElementById(type === 'error' ? 'flash-error-text' : 'flash-success-text');
    if (!el || !text) return;
    text.textContent = msg;
    el.classList.add('show');
    setTimeout(() => el.classList.remove('show'), 4000);
  }

  // ---- Init ----
  loadCategories();
  loadProducts();
})();
