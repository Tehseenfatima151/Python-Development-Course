# ShopFlask — E-Commerce Backend with Stripe Payments

A **production-style, full-stack e-commerce application** built with Flask, SQLAlchemy, JWT authentication, Stripe Checkout, Celery background jobs, and Redis. The primary focus is backend architecture: clean service layers, secure payment handling, idempotent webhook processing, atomic inventory management, and a comprehensive automated test suite.

---

## Features

- **JWT Authentication** — register, login, role-based access (customer / admin)
- **Product Catalogue** — public listing with search, category filter, sorting, pagination
- **Shopping Cart** — per-user cart, server-side price validation, stock enforcement
- **Order Management** — server-side order creation, price snapshots, order history
- **Stripe Checkout** — redirects to Stripe-hosted payment page (TEST mode)
- **Stripe Webhooks** — signature-verified, idempotent webhook processing
- **Inventory Management** — atomic stock decrements only after confirmed payment
- **Celery + Redis** — HTML confirmation emails sent asynchronously
- **Admin Dashboard** — product CRUD, stock management, order overview, revenue stats
- **Frontend** — responsive vanilla JS + CSS3 SPA-style frontend (10 pages)
- **35+ Automated Tests** — pytest suite covering auth, products, cart, orders, payments, webhooks, inventory, idempotency
- **Docker Compose** — one-command local stack (Flask + PostgreSQL + Redis + Celery Worker)

---

## Architecture

```
Browser / Frontend (HTML + Vanilla JS)
           │
           ▼
  Flask REST API  (/api/*)
           │
    ┌──────┴──────┐
    │             │
SQLAlchemy     Stripe SDK
    │
 SQLite (dev) / PostgreSQL (prod)

Stripe Webhook ──► Verify Signature
                       │
                  Find Order
                       │
               Mark Order PAID
                       │
            Decrease Inventory (atomic)
                       │
               Clear User Cart
                       │
            Celery Task ──► Redis Queue ──► Worker ──► SMTP Email
```

---

## Tech Stack

| Layer         | Technology                                    |
|---------------|-----------------------------------------------|
| Language      | Python 3.11+                                  |
| Web Framework | Flask 3.x                                     |
| ORM           | SQLAlchemy 2.x via Flask-SQLAlchemy           |
| Migrations    | Flask-Migrate (Alembic)                       |
| Auth          | Flask-JWT-Extended                            |
| Payments      | Stripe Python SDK (Checkout + Webhooks)       |
| Queue / Tasks | Celery 5.x + Redis                            |
| Email         | Python smtplib (SMTP with STARTTLS)           |
| Database      | SQLite (dev/test) · PostgreSQL (production)   |
| Frontend      | HTML5 · CSS3 · Vanilla JavaScript             |
| Tests         | pytest + pytest-flask                         |
| Container     | Docker + Docker Compose                       |

---

## Quick Start (Local — SQLite, no Docker)

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd "Ecommerce app"
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
copy .env.example .env      # Windows
cp .env.example .env        # macOS/Linux
```

Edit `.env` and set at minimum:

```
SECRET_KEY=any-long-random-string
JWT_SECRET_KEY=another-long-random-string
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

For local dev the `DATABASE_URL` can stay as the SQLite default (no config needed).

### 4. Initialise the database

```bash
flask db init        # only needed once
flask db migrate -m "initial"
flask db upgrade
```

### 5. Run Flask

```bash
python run.py
```

The API and frontend are served on **http://localhost:5000**.

### 6. Run Redis (required for Celery)

```bash
# Docker (easiest):
docker run -d -p 6379:6379 redis:7-alpine

# Or install Redis locally and run:
redis-server
```

### 7. Run the Celery worker

```bash
celery -A celery_worker.celery worker --loglevel=info
```

---

## Docker Compose (PostgreSQL + Redis + Flask + Worker)

```bash
# Copy and edit your .env first
cp .env.example .env

# Build and start all services
docker compose up --build

# Run migrations inside the web container
docker compose exec web flask db upgrade
```

Services started:
- `web` → Flask API + Frontend on port 5000
- `db` → PostgreSQL 16
- `redis` → Redis 7
- `worker` → Celery worker

---

## Running Tests

```bash
# All tests (uses in-memory SQLite — no external services needed)
pytest

# Verbose output
pytest -v

# Specific file
pytest tests/test_webhooks.py -v

# With coverage (requires pytest-cov)
pip install pytest-cov
pytest --cov=app --cov-report=term-missing
```

**No real Stripe keys or Redis needed for tests.** Stripe API calls are mocked; Celery runs in eager/synchronous mode.

---

## Stripe Testing

### Test mode setup

1. Get your test keys from [https://dashboard.stripe.com/test/apikeys](https://dashboard.stripe.com/test/apikeys)
2. Set `STRIPE_SECRET_KEY=sk_test_...` and `STRIPE_PUBLISHABLE_KEY=pk_test_...` in `.env`

### Test card numbers

| Scenario         | Card number          | Expiry    | CVC  |
|------------------|----------------------|-----------|------|
| Payment succeeds | `4242 4242 4242 4242`| Any future| Any  |
| Payment declined | `4000 0000 0000 0002`| Any future| Any  |
| Auth required    | `4000 0025 0000 3155`| Any future| Any  |

### Webhook local forwarding

Install the [Stripe CLI](https://stripe.com/docs/stripe-cli) and run:

```bash
stripe listen --forward-to localhost:5000/api/payments/webhook
```

This prints a `whsec_...` secret — paste it into `.env` as `STRIPE_WEBHOOK_SECRET`.

To simulate a payment:

```bash
stripe trigger checkout.session.completed
```

---

## API Documentation

### Authentication

| Method | Endpoint           | Auth     | Description                    |
|--------|--------------------|----------|--------------------------------|
| POST   | `/api/auth/register` | None   | Register new customer account  |
| POST   | `/api/auth/login`    | None   | Login, returns JWT token       |
| GET    | `/api/auth/me`       | JWT    | Get current user profile       |
| POST   | `/api/auth/logout`   | JWT    | Logout (client discards token) |

### Products

| Method | Endpoint                | Auth       | Description                        |
|--------|-------------------------|------------|------------------------------------|
| GET    | `/api/products`         | None       | List products (search/filter/page) |
| GET    | `/api/products/<id>`    | None       | Get product by ID                  |
| POST   | `/api/products`         | Admin JWT  | Create product                     |
| PUT    | `/api/products/<id>`    | Admin JWT  | Update product                     |
| DELETE | `/api/products/<id>`    | Admin JWT  | Delete product                     |

Query params: `search`, `category`, `sort_by`, `order`, `page`, `per_page`

### Cart

| Method | Endpoint                        | Auth | Description              |
|--------|---------------------------------|------|--------------------------|
| GET    | `/api/cart`                     | JWT  | Get current cart         |
| POST   | `/api/cart/items`               | JWT  | Add item to cart         |
| PUT    | `/api/cart/items/<product_id>`  | JWT  | Update item quantity     |
| DELETE | `/api/cart/items/<product_id>`  | JWT  | Remove item from cart    |
| DELETE | `/api/cart`                     | JWT  | Clear entire cart        |

### Orders

| Method | Endpoint              | Auth | Description              |
|--------|-----------------------|------|--------------------------|
| POST   | `/api/orders`         | JWT  | Create order from cart   |
| GET    | `/api/orders`         | JWT  | List user's orders       |
| GET    | `/api/orders/<id>`    | JWT  | Get order details        |

### Payments

| Method | Endpoint                                  | Auth | Description                        |
|--------|-------------------------------------------|------|------------------------------------|
| POST   | `/api/payments/create-checkout-session`   | JWT  | Create Stripe Checkout Session     |
| POST   | `/api/payments/webhook`                   | None | Stripe webhook receiver            |

### Admin

| Method | Endpoint                             | Auth       | Description              |
|--------|--------------------------------------|------------|--------------------------|
| GET    | `/api/admin/orders`                  | Admin JWT  | List all orders          |
| GET    | `/api/admin/orders/<id>`             | Admin JWT  | Get order detail         |
| PATCH  | `/api/admin/products/<id>/stock`     | Admin JWT  | Update product stock     |
| GET    | `/api/admin/users`                   | Admin JWT  | List all users           |
| GET    | `/api/admin/stats`                   | Admin JWT  | Dashboard stats          |

### Health

| Method | Endpoint       | Auth | Description  |
|--------|----------------|------|--------------|
| GET    | `/api/health`  | None | Health check |

---

## Response Format

All responses follow a consistent envelope:

```json
// Success
{
  "success": true,
  "message": "Product created successfully",
  "data": { ... }
}

// Error
{
  "success": false,
  "message": "Insufficient stock",
  "error": "INSUFFICIENT_STOCK"
}

// Validation error
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "price": "Price must be greater than zero",
    "name": "Product name is required"
  }
}
```

---

## Project Structure

```
Ecommerce app/
│
├── app/
│   ├── __init__.py          # App factory, blueprint registration, JWT/error handlers
│   ├── config.py            # Dev / Test / Production config classes
│   ├── extensions.py        # Extension instances (db, migrate, jwt, cors, celery)
│   │
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── user.py          # User (password hashing, roles)
│   │   ├── product.py       # Product (price in cents, stock helpers)
│   │   ├── cart.py          # Cart + CartItem (unique constraint, subtotal)
│   │   ├── order.py         # Order + OrderItem (price snapshots, status)
│   │   └── payment.py       # Payment (Stripe fields)
│   │
│   ├── routes/              # Flask blueprints (thin — delegate to services)
│   │   ├── auth.py          # /api/auth/*
│   │   ├── products.py      # /api/products/*
│   │   ├── cart.py          # /api/cart/*
│   │   ├── orders.py        # /api/orders/*
│   │   ├── payments.py      # /api/payments/* (checkout + webhook)
│   │   └── admin.py         # /api/admin/*
│   │
│   ├── services/            # Business logic layer
│   │   ├── order_service.py     # Cart → Order creation
│   │   ├── stripe_service.py    # Stripe API calls
│   │   └── inventory_service.py # Atomic stock decrements
│   │
│   ├── tasks/
│   │   └── email_tasks.py   # Celery task: send_order_confirmation_email
│   │
│   └── utils/
│       ├── validators.py    # Input validation helpers
│       └── decorators.py    # @admin_required, get_current_user
│
├── frontend/                # Vanilla JS + CSS frontend
│   ├── index.html           # Product listing
│   ├── login.html
│   ├── register.html
│   ├── product.html         # Product detail
│   ├── cart.html
│   ├── checkout.html
│   ├── orders.html
│   ├── order-success.html
│   ├── order-cancel.html
│   ├── admin.html
│   ├── css/style.css
│   └── js/
│       ├── api.js           # Fetch wrapper, JWT attachment
│       ├── auth.js          # Token storage, navbar rendering
│       ├── products.js      # Product grid + search
│       ├── cart.js          # Cart operations + badge
│       ├── checkout.js      # Order summary + Stripe redirect
│       └── orders.js        # Order history + detail modal
│
├── tests/
│   ├── conftest.py          # Fixtures (app, db, client, users, products, orders)
│   ├── test_auth.py         # 13 auth tests
│   ├── test_products.py     # 11 product tests
│   ├── test_cart.py         # 12 cart tests
│   ├── test_orders.py       # 9 order tests
│   ├── test_payments.py     # 5 payment tests
│   ├── test_webhooks.py     # 11 webhook + idempotency tests
│   └── test_inventory.py    # 8 inventory tests
│
├── migrations/
├── run.py                   # Flask entry point
├── celery_worker.py         # Celery entry point
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
└── docker-compose.yml
```

---

## Security Practices

| Practice | Implementation |
|----------|---------------|
| Password hashing | Werkzeug `generate_password_hash` (PBKDF2-SHA256) |
| JWT authentication | Flask-JWT-Extended with expiry and error handlers |
| Role-based access | `@admin_required` decorator |
| Webhook signature | `stripe.Webhook.construct_event` with `STRIPE_WEBHOOK_SECRET` |
| Server-side prices | Cart totals and order totals always calculated from DB |
| Server-side stock | Stock validated at cart add AND at order creation AND at payment confirmation |
| No secrets in frontend | Stripe secret key never sent to browser |
| No password in responses | `password_hash` excluded from all serialization |
| SQL injection | SQLAlchemy ORM — no raw SQL |
| Input validation | Validators on every write endpoint |
| CORS | Configurable via `CORS_ORIGINS` env var |
| Database transactions | Order + payment + inventory updates in a single transaction |
| Idempotent webhooks | Already-paid orders are skipped on duplicate webhook delivery |

---

## Inventory Consistency Strategy

Stock is managed conservatively:

1. **At cart add** — quantity is checked against current stock; adding more than available is rejected immediately with `409 INSUFFICIENT_STOCK`.
2. **At order creation** — stock is re-verified for every cart item. The order is created only if all items are available.
3. **At payment confirmation** — inside the webhook handler, stock is decremented using `SELECT FOR UPDATE` (PostgreSQL row-level lock) inside a database transaction. If any product has insufficient stock at this point the entire transaction is rolled back, the error is logged, and the order remains in a non-paid state for manual review.
4. **Stock is never pre-reserved** — no stock is held during the checkout session window. In the rare case a product sells out between order creation and payment confirmation, the webhook handler catches and logs it.

This trades perfect reservation for simplicity; a Redis-based reservation layer could be added as a future improvement.

---

## Creating an Admin User

There is no public admin registration endpoint (by design). To create an admin:

```bash
flask shell
```

```python
from app.extensions import db
from app.models.user import User

admin = User(name="Admin", email="admin@yourstore.com", role="admin")
admin.set_password("your-strong-password")
db.session.add(admin)
db.session.commit()
print("Admin created:", admin.id)
```

---

## End-to-End Payment Flow

```
1.  User registers / logs in  →  receives JWT
2.  User browses products     →  adds items to cart
3.  POST /api/payments/create-checkout-session
        └─ server creates pending Order from cart
        └─ server creates Stripe Checkout Session
        └─ returns { checkout_url }
4.  Browser redirects to Stripe-hosted checkout page
5.  User enters test card  4242 4242 4242 4242
6.  Stripe processes payment
7.  Stripe sends POST /api/payments/webhook (checkout.session.completed)
        └─ signature verified
        └─ order found via metadata.order_id
        └─ idempotency check: order not already paid
        └─ inventory decremented (atomic, SELECT FOR UPDATE)
        └─ order.status → "paid"
        └─ payment record created
        └─ cart cleared
        └─ send_order_confirmation_email.delay(order_id)  ← Celery task
8.  Redis delivers task to Celery worker
9.  Worker sends HTML email via SMTP
10. Browser lands on /order-success.html
11. User views paid order in /orders.html
```

---

## Future Improvements

- **Product reviews and ratings**
- **Discount codes / coupons**
- **Order cancellation and Stripe refunds**
- **Inventory reservation with TTL (Redis)**
- **Admin analytics charts (Chart.js)**
- **CI/CD pipeline (GitHub Actions)**
- **Rate limiting (Flask-Limiter)**
- **Token blacklisting on logout (Redis)**
- **S3 product image uploads**
- **Shipping address collection**
- **Multi-currency support**
