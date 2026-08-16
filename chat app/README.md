# LiveChat — Real-Time Collaboration & Chat Platform

A production-grade, portfolio-ready **Real-Time Collaboration & Team Chat Platform** built with **Flask-SocketIO, Vanilla JavaScript, SQLite, and Redis**.

LiveChat delivers instantaneous bidirectional messaging, dynamic channel creation, threaded replies, interactive emoji reactions, message pinning, in-room search, real-time typing indicators, user presence tracking, and persistent message history with zero heavy frontend framework dependencies.

---

## 🌟 Key Features

### 🚀 Dynamic Channel & Workspace System
* **Pre-Seeded Default Channels**: `#general`, `#developers`, `#design`, `#random`.
* **Dynamic Custom Channel Creation**: Users can create custom channels (e.g. `#ai-lab`, `#python`, `#frontend`) with names, descriptions, and real-time validation.
* **Instant Multi-Client Synchronization**: Newly created channels appear instantly in the sidebars of all connected users without refreshing.
* **Seamless In-App Room Switching**: Leave and join channels instantly with live message history loading and member list updates.

### 💬 Advanced Real-Time Messaging & Collaboration
* **Threaded Replies**: Interactive hover reply action with active reply preview bar above the composer and nested quote cards in the message feed.
* **Emoji Reactions**: Real-time message reactions (`👍`, `❤️`, `😂`, `🔥`, `👏`) with instant count badges and interactive user toggling.
* **Message Pinning**: Pin and unpin important messages with dedicated visual badges and a consolidated Pinned Messages view in the Channel Details modal.
* **In-Room Message Search**: Parameterized, room-isolated search allowing users to find keywords with instant scroll-to-message jump and highlight animations.
* **One-Click Message Copy**: Copy message text directly to clipboard with animated toast notification feedback.

### 👥 Presence & User Identity
* **Deterministic Color Avatars**: Usernames are deterministically mapped to distinct, accessible palette colors with initials.
* **Live Online / Away Status**: Real-time presence status with clickable toggle and live badge updates across all room members.
* **Real-Time Typing Indicators**: Debounced and throttled broadcasts (*"Fatima is typing..."* / *"Ali and Fatima are typing..."*).
* **Unread Message Counter & Smart Scroll**: Floating *"↓ X new messages"* button when scrolled away from bottom.

### 🛡️ Architecture & Production Reliability
* **Safe SQLite Persistence & Automatic Migration**: Fully backward-compatible schema migration preserving all existing messages and channels.
* **Redis Pub/Sub & Multi-Worker Coordination**: Optional Redis message queue for horizontal scaling with automatic fallback to standalone in-memory mode.
* **100% XSS-Safe DOM Manipulation**: Client-side rendering strictly using `textContent` and `createElement`.
* **Comprehensive Automated Test Suite**: 20 automated pytest unit and integration tests covering Socket.IO events, REST APIs, and room isolation.
* **Obsidian SaaS UI / UX**: Modern dark theme with responsive mobile navigation drawer, micro-animations, and glassmorphic dialogs.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3.x, Flask 3.0+ |
| **WebSocket Engine** | Flask-SocketIO, Python-EngineIO, Simple-WebSocket |
| **Database & ORM** | SQLite, Flask-SQLAlchemy, SQLAlchemy 2.0+ |
| **Message Broker / Cache** | Redis 7+ / 8+ (redis-py) |
| **Configuration** | Python-dotenv |
| **Frontend** | HTML5, Vanilla CSS3 (Custom Design System), Vanilla JavaScript (ES6+) |
| **Icons & Typography** | Font Awesome 6, Plus Jakarta Sans, JetBrains Mono |
| **Testing Framework** | Pytest |

---

## 🏗️ Architecture

```
                                  ┌────────────────────────┐
                                  │      Web Browser       │
                                  │   (Vanilla JS Client)  │
                                  └───────────┬────────────┘
                                              │ WebSocket / REST API
                                              ▼
                                  ┌────────────────────────┐
                                  │   Flask-SocketIO App   │
                                  │       (app.py)         │
                                  └───┬────────────────┬───┘
                                      │                │
            Persistent Storage        │                │ Real-Time Message Queue / PubSub
                                      ▼                ▼
                           ┌─────────────────┐  ┌─────────────────┐
                           │ SQLite Database │  │  Redis Server   │
                           │   (chat.db)     │  │ (REDIS_URL)     │
                           │                 │  │                 │
                           │ • messages      │  │ • sessions      │
                           │ • rooms         │  │ • room members  │
                           │ • reactions     │  │ • queue events  │
                           └─────────────────┘  └─────────────────┘
```

---

## 📁 Project Structure

```
chat-app/
│
├── app.py                     # Flask application factory and server entry point
├── config.py                  # Environment config and Redis connection checks
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Local environment configuration
├── .gitignore                 # Git ignore patterns
├── README.md                  # Complete documentation
│
├── instance/                  # SQLite database directory (auto-created)
│   └── chat.db                # SQLite database file
│
├── models/                    # Data models and migration layer
│   ├── __init__.py            # SQLAlchemy database instance and model exports
│   ├── message.py             # Message model (replies, reactions, pins)
│   ├── room.py                # Room model for dynamic channels
│   ├── reaction.py            # MessageReaction model for emoji reactions
│   ├── migration.py           # Safe database migration and seeding utility
│   └── user.py                # Room and active user session manager
│
├── routes/                    # HTTP Blueprints & REST endpoints
│   ├── __init__.py            # Main Blueprint definition
│   └── main.py                # Index view, /health, /api/rooms, search, pins
│
├── sockets/                   # WebSocket event handlers
│   ├── __init__.py            # SocketIO instance setup & Redis queue binding
│   └── chat_events.py         # join_room, send_message, replies, reactions, pins
│
├── static/                    # Frontend static assets
│   ├── css/
│   │   └── style.css          # Modern obsidian design system stylesheet
│   └── js/
│       └── chat.js            # Vanilla JavaScript Socket.IO client
│
├── templates/                 # Jinja2 HTML templates
│   └── index.html             # Single-page collaboration interface
│
├── tests/                     # Automated test suite
│   ├── __init__.py            # Tests package
│   └── test_chat.py           # 20 unit & integration tests
│
└── utils/                     # Utility helpers
    ├── __init__.py            # Utils package
    └── helpers.py             # Validation, sanitization, color generator
```

---

## ⚡ Installation & Quick Start

### 1. Prerequisites
* Python 3.10+
* Redis (Optional for local development; required for multi-worker scaling)

### 2. Clone and Setup Environment

```bash
# Navigate to project directory
cd "c:\Users\HP\Desktop\chat app"

# Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:

```env
SECRET_KEY=livechat-super-secure-production-secret-key-2026
DATABASE_URL=sqlite:///chat.db
REDIS_URL=redis://127.0.0.1:6379/0
REQUIRE_REDIS=false
PORT=5000
FLASK_DEBUG=false
```

---

## 🔴 Redis Setup Instructions (Windows)

LiveChat works in **standalone in-memory mode** out-of-the-box when Redis is not running. To enable full Redis message queue coordination:

### Option A: Docker Desktop (Recommended)
```bash
docker run -d --name livechat-redis -p 6379:6379 redis:7-alpine
```

### Option B: Native Windows (Memurai / Redis Port)
Download and run the [Memurai Developer Edition](https://www.memurai.com/) or Redis for Windows MSI installer.

Verify Redis is reachable:
```bash
python -c "import redis; r = redis.from_url('redis://127.0.0.1:6379/0'); print(r.ping())"
# Output: True
```

---

## 🚀 Running the Application

Start the LiveChat server:

```bash
python app.py
```

Console Output:
```
============================================================
 [*] LiveChat Real-Time Collaboration Platform Starting
 [*] URL: http://127.0.0.1:5000
 [*] Database: sqlite:///.../instance/chat.db
 [*] Redis Status: Redis connected successfully
============================================================
```

Open your browser at:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

Health Check:
👉 **[http://127.0.0.1:5000/health](http://127.0.0.1:5000/health)**

---

## 🧪 Automated Testing

Run the full pytest suite:

```bash
pytest tests/test_chat.py -v
```

Test Suite Coverage (20 Tests):
* `test_color_determinism`: Deterministic avatar color generation.
* `test_sanitize_text`: XSS and control character filtering.
* `test_validations`: Username, room, message, and reaction validation rules.
* `test_message_model_persistence`: SQLite storage and serialized payload verification.
* `test_index_route`: Single-page app loading.
* `test_health_route`: Component health check endpoint.
* `test_room_messages_api`: Message history REST API.
* `test_dynamic_room_creation_and_listing`: Dynamic channel creation and listing.
* `test_duplicate_and_invalid_room_rejection`: Uniqueness and validation constraints.
* `test_socketio_join_and_history`: Room joining and history delivery.
* `test_socketio_multi_client_messaging`: Real-time bidirectional messaging.
* `test_socketio_room_isolation`: Room partition & privacy verification.
* `test_socketio_typing_indicator`: Multi-client debounced typing events.
* `test_socketio_leave_room`: Voluntary room departures.
* `test_socketio_validation_errors`: Malformed payload rejection.
* `test_message_reply_thread`: Threaded reply linking and nested preview.
* `test_message_reaction_toggle`: Interactive reaction adding and toggling.
* `test_message_pin_unpin_and_api`: Pinning, unpinning, and pinned message API.
* `test_in_room_message_search_isolation`: In-room search preventing cross-room data leaks.
* `test_user_presence_status_update`: Live Online / Away presence synchronization.

---

## 🔒 Security Best Practices

1. **XSS Protection**: All user input is rendered using `textContent` and `createElement`. Raw HTML injection (`innerHTML`) is avoided for user-generated content.
2. **SQL Injection Prevention**: All queries use SQLAlchemy ORM and parameterized queries.
3. **Room Isolation**: All message queries, reactions, pins, and searches are strictly scoped to the user's active room.
4. **Input Sanitization**: Control characters, null bytes, and excessive whitespace are stripped server-side.

---

## 📄 License
MIT License. Built for software engineering portfolio and team collaboration.
