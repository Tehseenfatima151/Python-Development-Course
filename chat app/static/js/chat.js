/**
 * LiveChat — Real-Time Collaboration & Chat Platform
 * Vanilla JavaScript Client
 * 100% XSS Safe DOM Operations & Real-Time Socket.IO Coordination
 */

(function () {
    "use strict";

    // Application Configuration
    const CONFIG = window.LIVECHAT_CONFIG || {
        maxMessageLen: 1000,
        maxUsernameLen: 30,
        maxRoomLen: 50,
        allowedReactions: ["👍", "❤️", "😂", "🔥", "👏"],
    };

    // Client State
    const state = {
        socket: null,
        currentUser: "",
        currentRoom: "",
        currentRoomDescription: "",
        userColor: "#4f46e5",
        userStatus: "online", // 'online' | 'away'
        isConnected: false,
        allRooms: [],
        onlineUsers: [],
        activeTypers: new Set(),
        replyingTo: null, // { id, username, snippet, color }
        typingTimer: null,
        lastTypingEmitTime: 0,
        isUserScrolledUp: false,
        unreadCount: 0,
        searchDebounceTimer: null,
    };

    // DOM Elements Cache
    const DOM = {
        toastContainer: document.getElementById("toast-container"),

        // Join Screen
        joinScreen: document.getElementById("join-screen"),
        joinForm: document.getElementById("join-form"),
        usernameInput: document.getElementById("username-input"),
        roomInput: document.getElementById("room-input"),
        joinBtn: document.getElementById("join-btn"),
        joinErrorBox: document.getElementById("join-error-box"),
        joinErrorText: document.getElementById("join-error-text"),
        usernameError: document.getElementById("username-error"),
        roomError: document.getElementById("room-error"),
        presetPills: document.querySelectorAll(".room-pill"),

        // Chat Screen & Main Header
        chatScreen: document.getElementById("chat-screen"),
        currentRoomTitle: document.getElementById("current-room-title"),
        roomMembersCount: document.getElementById("room-members-count"),
        connectionBadge: document.getElementById("connection-badge"),
        connectionStatusText: document.getElementById("connection-status-text"),
        leaveRoomBtn: document.getElementById("leave-room-btn"),
        roomInfoBtn: document.getElementById("room-info-btn"),
        openMsgSearchBtn: document.getElementById("open-msg-search-btn"),

        // Sidebar
        usersSidebar: document.getElementById("online-users-sidebar"),
        sidebarToggleBtn: document.getElementById("sidebar-toggle-btn"),
        sidebarCloseBtn: document.getElementById("sidebar-close-btn"),
        sidebarBackdrop: document.getElementById("sidebar-backdrop"),
        channelSearchInput: document.getElementById("channel-search-input"),
        defaultRoomsList: document.getElementById("default-rooms-list"),
        customRoomsList: document.getElementById("custom-rooms-list"),
        onlineUsersList: document.getElementById("online-users-list"),
        onlineCountBadge: document.getElementById("online-count-badge"),
        openCreateRoomModalBtn: document.getElementById("open-create-room-modal-btn"),
        currentUserAvatar: document.getElementById("current-user-avatar"),
        currentUserName: document.getElementById("current-user-name"),
        userStatusPill: document.getElementById("user-status-pill"),
        userStatusText: document.getElementById("user-status-text"),

        // Messages Viewport
        messagesContainer: document.getElementById("messages-container"),
        messagesFeed: document.getElementById("messages-feed"),
        messagesLoading: document.getElementById("messages-loading"),
        emptyChatState: document.getElementById("empty-chat-state"),
        emptyRoomName: document.getElementById("empty-room-name"),
        scrollBottomBtn: document.getElementById("scroll-bottom-btn"),
        unreadCounter: document.getElementById("unread-counter"),

        // Typing & Replying
        typingIndicatorBar: document.getElementById("typing-indicator-bar"),
        typingText: document.getElementById("typing-text"),
        replyingBanner: document.getElementById("replying-banner"),
        replyingToUser: document.getElementById("replying-to-user"),
        replyingSnippet: document.getElementById("replying-snippet"),
        cancelReplyBtn: document.getElementById("cancel-reply-btn"),

        // Composer
        messageForm: document.getElementById("message-form"),
        messageInput: document.getElementById("message-input"),
        sendMsgBtn: document.getElementById("send-msg-btn"),
        charCounter: document.getElementById("char-counter"),
        quickEmojiBtns: document.querySelectorAll(".quick-emoji-btn"),

        // Modals
        createRoomModal: document.getElementById("create-room-modal"),
        createRoomForm: document.getElementById("create-room-form"),
        newRoomName: document.getElementById("new-room-name"),
        newRoomDesc: document.getElementById("new-room-desc"),
        createRoomErrorBox: document.getElementById("create-room-error-box"),
        createRoomErrorText: document.getElementById("create-room-error-text"),
        closeCreateRoomModalBtn: document.getElementById("close-create-room-modal-btn"),
        cancelCreateRoomBtn: document.getElementById("cancel-create-room-btn"),

        roomInfoModal: document.getElementById("room-info-modal"),
        closeRoomInfoModalBtn: document.getElementById("close-room-info-modal-btn"),
        infoRoomName: document.getElementById("info-room-name"),
        infoRoomMembersCount: document.getElementById("info-room-members-count"),
        infoRoomPinsCount: document.getElementById("info-room-pins-count"),
        infoRoomCreator: document.getElementById("info-room-creator"),
        infoRoomDescription: document.getElementById("info-room-description"),
        pinnedMessagesList: document.getElementById("pinned-messages-list"),

        msgSearchModal: document.getElementById("msg-search-modal"),
        closeMsgSearchModalBtn: document.getElementById("close-msg-search-modal-btn"),
        searchCurrentRoomName: document.getElementById("search-current-room-name"),
        inRoomSearchInput: document.getElementById("in-room-search-input"),
        searchResultsContainer: document.getElementById("search-results-container"),
    };

    /* ==========================================================================
       Utility Functions & Logger
       ========================================================================== */

    function logger(...args) {
        if (window.__LC_DEBUG) {
            console.log("[LiveChat]", ...args);
        }
    }

    function showToast(message, type = "info", duration = 4000) {
        if (!DOM.toastContainer) return;

        const toast = document.createElement("div");
        toast.className = `toast toast-${type}`;

        const icon = document.createElement("i");
        if (type === "error") {
            icon.className = "fa-solid fa-circle-exclamation";
        } else if (type === "success") {
            icon.className = "fa-solid fa-circle-check";
        } else if (type === "warning") {
            icon.className = "fa-solid fa-triangle-exclamation";
        } else {
            icon.className = "fa-solid fa-circle-info";
        }

        const textSpan = document.createElement("span");
        textSpan.textContent = message;

        toast.appendChild(icon);
        toast.appendChild(textSpan);
        DOM.toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateX(50px)";
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    function formatTime(isoString) {
        if (!isoString) return "";
        try {
            const date = new Date(isoString);
            return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        } catch (e) {
            return "";
        }
    }

    function updateConnectionStatus(status) {
        if (!DOM.connectionBadge || !DOM.connectionStatusText) return;

        DOM.connectionBadge.className = "connection-status-pill";

        if (status === "connected") {
            state.isConnected = true;
            DOM.connectionBadge.classList.add("status-connected");
            DOM.connectionStatusText.textContent = "Connected";
            updateSendButtonState();
        } else if (status === "connecting") {
            state.isConnected = false;
            DOM.connectionBadge.classList.add("status-connecting");
            DOM.connectionStatusText.textContent = "Connecting...";
            DOM.sendMsgBtn.disabled = true;
        } else {
            state.isConnected = false;
            DOM.connectionBadge.classList.add("status-disconnected");
            DOM.connectionStatusText.textContent = "Disconnected";
            DOM.sendMsgBtn.disabled = true;
        }
    }

    /* ==========================================================================
       Socket.IO Connection & Event Handlers
       ========================================================================== */

    function initSocket() {
        if (state.socket) return state.socket;

        updateConnectionStatus("connecting");

        const socket = io({
            reconnection: true,
            reconnectionAttempts: 20,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            timeout: 10000,
        });

        socket.on("connect", () => {
            logger("Socket connected:", socket.id);
            updateConnectionStatus("connected");
        });

        socket.on("disconnect", (reason) => {
            logger("Socket disconnected:", reason);
            updateConnectionStatus("disconnected");
            showToast("Connection lost. Attempting to reconnect...", "warning");
        });

        socket.on("connect_error", (err) => {
            logger("Socket connection error:", err);
            updateConnectionStatus("connecting");
        });

        // Room joined acknowledgment
        socket.on("room_joined", (data) => {
            logger("Room joined confirmation:", data);
            state.currentUser = data.username;
            state.currentRoom = data.room;
            state.currentRoomDescription = data.room_description || "";
            state.userColor = data.username_color || "#4f46e5";

            // Transition UI to chat screen
            DOM.joinScreen.classList.add("hidden");
            DOM.chatScreen.classList.remove("hidden");

            // Update main chat header
            DOM.currentRoomTitle.textContent = data.room;
            DOM.emptyRoomName.textContent = data.room;

            // Update user footer profile in sidebar
            DOM.currentUserName.textContent = state.currentUser;
            DOM.currentUserAvatar.textContent = (state.currentUser.charAt(0) || "?").toUpperCase();
            DOM.currentUserAvatar.style.backgroundColor = state.userColor;

            // Reset replying state
            cancelReply();

            // Refresh available rooms in sidebar
            fetchRoomsList();

            // Focus message input
            setTimeout(() => DOM.messageInput.focus(), 100);
        });

        // Historical messages batch
        socket.on("message_history", (data) => {
            DOM.messagesLoading.classList.add("hidden");
            DOM.messagesFeed.replaceChildren();

            const messages = data.messages || [];
            if (messages.length === 0) {
                DOM.emptyChatState.classList.remove("hidden");
            } else {
                DOM.emptyChatState.classList.add("hidden");
                messages.forEach((msg) => renderChatMessage(msg, msg.username === state.currentUser));
            }
            scrollToBottom(true);
        });

        // New real-time message received
        socket.on("new_message", (msg) => {
            DOM.emptyChatState.classList.add("hidden");
            const isMine = msg.username === state.currentUser;
            renderChatMessage(msg, isMine);

            if (isMine || !state.isUserScrolledUp) {
                scrollToBottom(false);
            } else {
                state.unreadCount++;
                updateScrollBottomButton();
            }
        });

        // System notification: user joined
        socket.on("user_joined", (data) => {
            renderSystemMessage(`${data.username} joined the channel`, data.timestamp);
            if (data.username !== state.currentUser && !state.isUserScrolledUp) {
                scrollToBottom(false);
            }
        });

        // System notification: user left
        socket.on("user_left", (data) => {
            renderSystemMessage(`${data.username} left the channel`, data.timestamp);
            state.activeTypers.delete(data.username);
            updateTypingDisplay();
        });

        // Online room users list updated
        socket.on("room_users_updated", (data) => {
            state.onlineUsers = data.users || [];
            renderOnlineUsers(state.onlineUsers);
            const count = data.count !== undefined ? data.count : state.onlineUsers.length;
            DOM.roomMembersCount.textContent = `${count} online`;
            DOM.onlineCountBadge.textContent = count;
        });

        // User status (online / away) updated
        socket.on("user_status_updated", (data) => {
            if (data.users) {
                state.onlineUsers = data.users;
                renderOnlineUsers(state.onlineUsers);
            }
        });

        // Typing updates from peers
        socket.on("typing_update", (data) => {
            if (data.username === state.currentUser) return;

            if (data.is_typing) {
                state.activeTypers.add(data.username);
            } else {
                state.activeTypers.delete(data.username);
            }
            updateTypingDisplay();
        });

        // Real-Time Reaction Updated
        socket.on("reaction_updated", (data) => {
            updateMessageReactionsInDOM(data.message_id, data.reactions);
        });

        // Real-Time Message Pinned / Unpinned
        socket.on("message_pinned", (data) => {
            updateMessagePinInDOM(data.message_id, true);
            showToast(`Message pinned by ${data.pinned_by}`, "info");
        });

        socket.on("message_unpinned", (data) => {
            updateMessagePinInDOM(data.message_id, false);
        });

        // Real-Time Dynamic Room Created (Broadcast to all clients)
        socket.on("room_created", (roomData) => {
            if (!state.allRooms.some((r) => r.name === roomData.name)) {
                state.allRooms.push(roomData);
                renderChannelsList(state.allRooms);
            }
        });

        // Room left acknowledgment
        socket.on("room_left", () => {
            resetChatState();
        });

        // Error notification from server
        socket.on("error", (err) => {
            const msg = err.message || "An unexpected error occurred.";
            showToast(msg, "error");
            if (err.field === "username") {
                showJoinError(msg, DOM.usernameInput, DOM.usernameError);
            } else if (err.field === "room") {
                showJoinError(msg, DOM.roomInput, DOM.roomError);
            }
        });

        state.socket = socket;
        return socket;
    }

    /* ==========================================================================
       Message Rendering (100% Safe DOM Manipulation)
       ========================================================================== */

    function renderChatMessage(msg, isMine) {
        const wrapper = document.createElement("div");
        wrapper.className = `message-wrapper ${isMine ? "message-mine" : "message-peer"}`;
        wrapper.id = `msg-${msg.id}`;
        wrapper.setAttribute("data-msg-id", msg.id || "");

        // Header: Author Name, Timestamp, Pinned Pill
        const header = document.createElement("div");
        header.className = "message-header";

        const authorSpan = document.createElement("span");
        authorSpan.className = "message-username";
        authorSpan.textContent = isMine ? "You" : msg.username;
        if (!isMine && msg.username_color) {
            authorSpan.style.color = msg.username_color;
        }

        const timeSpan = document.createElement("span");
        timeSpan.className = "message-time";
        timeSpan.textContent = formatTime(msg.timestamp);

        header.appendChild(authorSpan);
        header.appendChild(timeSpan);

        if (msg.is_pinned) {
            const pinPill = document.createElement("span");
            pinPill.className = "pin-pill";
            pinPill.innerHTML = '<i class="fa-solid fa-thumbtack"></i> Pinned';
            header.appendChild(pinPill);
        }

        wrapper.appendChild(header);

        // Nested Reply Quote Card (if reply)
        if (msg.reply_to) {
            const quoteCard = document.createElement("div");
            quoteCard.className = "reply-quote-card";
            quoteCard.title = "Click to jump to parent message";

            const quoteIcon = document.createElement("i");
            quoteIcon.className = "fa-solid fa-reply";

            const quoteAuthor = document.createElement("span");
            quoteAuthor.className = "reply-quote-author";
            quoteAuthor.textContent = `@${msg.reply_to.username}:`;

            const quoteSnippet = document.createElement("span");
            quoteSnippet.className = "reply-quote-snippet";
            quoteSnippet.textContent = msg.reply_to.message || msg.reply_to.content || "";

            quoteCard.appendChild(quoteIcon);
            quoteCard.appendChild(quoteAuthor);
            quoteCard.appendChild(quoteSnippet);

            quoteCard.addEventListener("click", () => {
                jumpToMessageInFeed(msg.reply_to.id);
            });

            wrapper.appendChild(quoteCard);
        }

        // Message Bubble Text
        const bubble = document.createElement("div");
        bubble.className = "message-bubble";
        bubble.textContent = msg.message || msg.content || "";
        wrapper.appendChild(bubble);

        // Reactions Row
        const reactionsRow = document.createElement("div");
        reactionsRow.className = "reactions-row";
        reactionsRow.id = `reactions-${msg.id}`;
        renderReactionPills(reactionsRow, msg.id, msg.reactions || []);
        wrapper.appendChild(reactionsRow);

        // Floating Action Toolbar on Hover
        const toolbar = createMessageActionToolbar(msg);
        wrapper.appendChild(toolbar);

        DOM.messagesFeed.appendChild(wrapper);
    }

    function createMessageActionToolbar(msg) {
        const toolbar = document.createElement("div");
        toolbar.className = "message-actions-toolbar";

        // Quick Emoji Shortcut Buttons
        CONFIG.allowedReactions.forEach((emoji) => {
            const emojiBtn = document.createElement("button");
            emojiBtn.type = "button";
            emojiBtn.className = "action-tool-btn emoji-shortcut-btn";
            emojiBtn.textContent = emoji;
            emojiBtn.title = `React ${emoji}`;
            emojiBtn.addEventListener("click", () => {
                toggleMessageReaction(msg.id, emoji);
            });
            toolbar.appendChild(emojiBtn);
        });

        // Reply Button
        const replyBtn = document.createElement("button");
        replyBtn.type = "button";
        replyBtn.className = "action-tool-btn";
        replyBtn.title = "Reply to message";
        replyBtn.innerHTML = '<i class="fa-solid fa-reply"></i>';
        replyBtn.addEventListener("click", () => {
            initiateReply(msg);
        });

        // Pin Button
        const pinBtn = document.createElement("button");
        pinBtn.type = "button";
        pinBtn.className = `action-tool-btn ${msg.is_pinned ? "btn-pin-active" : ""}`;
        pinBtn.title = msg.is_pinned ? "Unpin message" : "Pin message";
        pinBtn.innerHTML = '<i class="fa-solid fa-thumbtack"></i>';
        pinBtn.addEventListener("click", () => {
            togglePinMessage(msg.id, !msg.is_pinned);
        });

        // Copy Button
        const copyBtn = document.createElement("button");
        copyBtn.type = "button";
        copyBtn.className = "action-tool-btn";
        copyBtn.title = "Copy text";
        copyBtn.innerHTML = '<i class="fa-regular fa-copy"></i>';
        copyBtn.addEventListener("click", () => {
            copyMessageText(msg.content || msg.message || "");
        });

        toolbar.appendChild(replyBtn);
        toolbar.appendChild(pinBtn);
        toolbar.appendChild(copyBtn);

        return toolbar;
    }

    function renderReactionPills(container, messageId, reactions) {
        container.replaceChildren();
        if (!reactions || reactions.length === 0) return;

        reactions.forEach((rx) => {
            const hasMyReaction = rx.users && rx.users.includes(state.currentUser);
            const pill = document.createElement("button");
            pill.type = "button";
            pill.className = `reaction-pill ${hasMyReaction ? "reacted-by-me" : ""}`;
            pill.title = rx.users ? rx.users.join(", ") : "";

            const emojiSpan = document.createElement("span");
            emojiSpan.textContent = rx.reaction;

            const countSpan = document.createElement("span");
            countSpan.className = "reaction-count";
            countSpan.textContent = rx.count;

            pill.appendChild(emojiSpan);
            pill.appendChild(countSpan);

            pill.addEventListener("click", () => {
                toggleMessageReaction(messageId, rx.reaction);
            });

            container.appendChild(pill);
        });
    }

    function updateMessageReactionsInDOM(messageId, reactions) {
        const container = document.getElementById(`reactions-${messageId}`);
        if (container) {
            renderReactionPills(container, messageId, reactions);
        }
    }

    function updateMessagePinInDOM(messageId, isPinned) {
        const msgEl = document.getElementById(`msg-${messageId}`);
        if (!msgEl) return;

        const header = msgEl.querySelector(".message-header");
        const existingPin = header ? header.querySelector(".pin-pill") : null;

        if (isPinned && !existingPin && header) {
            const pinPill = document.createElement("span");
            pinPill.className = "pin-pill";
            pinPill.innerHTML = '<i class="fa-solid fa-thumbtack"></i> Pinned';
            header.appendChild(pinPill);
        } else if (!isPinned && existingPin) {
            existingPin.remove();
        }

        const pinBtn = msgEl.querySelector('.action-tool-btn[title*="pin" i], .action-tool-btn[title*="Pin" i]');
        if (pinBtn) {
            if (isPinned) {
                pinBtn.classList.add("btn-pin-active");
                pinBtn.title = "Unpin message";
            } else {
                pinBtn.classList.remove("btn-pin-active");
                pinBtn.title = "Pin message";
            }
        }
    }

    function renderSystemMessage(text, timestamp) {
        const container = document.createElement("div");
        container.className = "message-system";

        const pill = document.createElement("div");
        pill.className = "system-pill";

        const icon = document.createElement("i");
        icon.className = "fa-solid fa-circle-info system-icon";

        const textNode = document.createElement("span");
        textNode.textContent = text;

        pill.appendChild(icon);
        pill.appendChild(textNode);

        if (timestamp) {
            const timeNode = document.createElement("span");
            timeNode.className = "message-time";
            timeNode.textContent = ` • ${formatTime(timestamp)}`;
            pill.appendChild(timeNode);
        }

        container.appendChild(pill);
        DOM.messagesFeed.appendChild(container);
    }

    /* ==========================================================================
       Sidebar Channels & Members
       ========================================================================== */

    async function fetchRoomsList() {
        try {
            const res = await fetch("/api/rooms");
            if (res.ok) {
                const data = await res.json();
                state.allRooms = data.rooms || [];
                renderChannelsList(state.allRooms);
            }
        } catch (e) {
            logger("Failed to fetch rooms list:", e);
        }
    }

    function renderChannelsList(rooms) {
        DOM.defaultRoomsList.replaceChildren();
        DOM.customRoomsList.replaceChildren();

        const query = (DOM.channelSearchInput.value || "").trim().toLowerCase();
        const filtered = rooms.filter((r) => r.name.toLowerCase().includes(query));

        const defaultRooms = filtered.filter((r) => r.is_default);
        const customRooms = filtered.filter((r) => !r.is_default);

        defaultRooms.forEach((room) => {
            DOM.defaultRoomsList.appendChild(createChannelListItem(room));
        });

        customRooms.forEach((room) => {
            DOM.customRoomsList.appendChild(createChannelListItem(room));
        });
    }

    function createChannelListItem(room) {
        const li = document.createElement("li");
        const isCurrent = room.name === state.currentRoom;

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = `room-nav-btn ${isCurrent ? "active" : ""}`;
        btn.setAttribute("data-room", room.name);

        const labelGroup = document.createElement("div");
        labelGroup.className = "room-nav-label";

        const hash = document.createElement("span");
        hash.textContent = "#";

        const nameSpan = document.createElement("span");
        nameSpan.textContent = room.name;

        labelGroup.appendChild(hash);
        labelGroup.appendChild(nameSpan);
        btn.appendChild(labelGroup);

        if (room.online_count !== undefined && room.online_count > 0) {
            const countSpan = document.createElement("span");
            countSpan.className = "room-online-count";
            countSpan.textContent = room.online_count;
            btn.appendChild(countSpan);
        }

        btn.addEventListener("click", () => {
            if (room.name !== state.currentRoom) {
                switchChannel(room.name);
            }
        });

        li.appendChild(btn);
        return li;
    }

    function renderOnlineUsers(users) {
        DOM.onlineUsersList.replaceChildren();

        if (users.length === 0) {
            const emptyItem = document.createElement("li");
            emptyItem.className = "user-item";
            emptyItem.style.color = "var(--text-muted)";
            emptyItem.style.fontSize = "0.82rem";
            emptyItem.textContent = "No members in room";
            DOM.onlineUsersList.appendChild(emptyItem);
            return;
        }

        users.forEach((user) => {
            const isMe = user.username === state.currentUser;
            const li = document.createElement("li");
            li.className = `user-item ${isMe ? "is-current-user" : ""}`;

            const avatar = document.createElement("div");
            avatar.className = "user-avatar-circle";
            avatar.style.backgroundColor = user.color || "#4f46e5";
            avatar.textContent = (user.username || "?").charAt(0).toUpperCase();

            const dot = document.createElement("span");
            dot.className = `user-status-dot ${user.status === "away" ? "status-away" : ""}`;
            avatar.appendChild(dot);

            const nameWrapper = document.createElement("div");
            nameWrapper.className = "user-name-wrapper";

            const nameSpan = document.createElement("span");
            nameSpan.className = "user-name-text";
            nameSpan.textContent = user.username;
            nameWrapper.appendChild(nameSpan);

            if (isMe) {
                const youTag = document.createElement("span");
                youTag.className = "user-you-tag";
                youTag.textContent = "you";
                nameWrapper.appendChild(youTag);
            }

            li.appendChild(avatar);
            li.appendChild(nameWrapper);
            DOM.onlineUsersList.appendChild(li);
        });
    }

    /* ==========================================================================
       Interactive Actions: Reactions, Replies, Pins, Copy, Switching
       ========================================================================== */

    function switchChannel(newRoomName) {
        if (!state.socket || !state.isConnected) {
            showToast("Cannot switch channel: Disconnected from server.", "error");
            return;
        }

        DOM.messagesLoading.classList.remove("hidden");
        DOM.emptyChatState.classList.add("hidden");
        DOM.messagesFeed.replaceChildren();

        state.socket.emit("join_room", {
            username: state.currentUser,
            room: newRoomName,
        });

        if (DOM.usersSidebar) DOM.usersSidebar.classList.remove("open");
        if (DOM.sidebarBackdrop) DOM.sidebarBackdrop.classList.add("hidden");
    }

    function toggleMessageReaction(messageId, reaction) {
        if (!state.socket || !state.isConnected || !state.currentRoom) return;

        state.socket.emit("toggle_reaction", {
            message_id: messageId,
            reaction: reaction,
            room: state.currentRoom,
        });
    }

    function togglePinMessage(messageId, shouldPin) {
        if (!state.socket || !state.isConnected || !state.currentRoom) return;

        const eventName = shouldPin ? "pin_message" : "unpin_message";
        state.socket.emit(eventName, {
            message_id: messageId,
            room: state.currentRoom,
        });
    }

    function initiateReply(msg) {
        state.replyingTo = {
            id: msg.id,
            username: msg.username,
            snippet: msg.content || msg.message || "",
            color: msg.username_color || "#4f46e5",
        };

        DOM.replyingToUser.textContent = msg.username;
        DOM.replyingSnippet.textContent = state.replyingTo.snippet;
        DOM.replyingBanner.classList.remove("hidden");

        DOM.messageInput.focus();
    }

    function cancelReply() {
        state.replyingTo = null;
        DOM.replyingBanner.classList.add("hidden");
    }

    async function copyMessageText(text) {
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                await navigator.clipboard.writeText(text);
            } else {
                const tempTextarea = document.createElement("textarea");
                tempTextarea.value = text;
                document.body.appendChild(tempTextarea);
                tempTextarea.select();
                document.execCommand("copy");
                document.body.removeChild(tempTextarea);
            }
            showToast("Message copied to clipboard.", "success", 2500);
        } catch (e) {
            showToast("Failed to copy message to clipboard.", "error");
        }
    }

    function jumpToMessageInFeed(messageId) {
        const msgEl = document.getElementById(`msg-${messageId}`);
        if (msgEl) {
            msgEl.scrollIntoView({ behavior: "smooth", block: "center" });
            msgEl.classList.remove("message-highlighted");
            void msgEl.offsetWidth;
            msgEl.classList.add("message-highlighted");
        } else {
            showToast("Message is from older history.", "info");
        }
    }

    function toggleUserPresence() {
        const newStatus = state.userStatus === "online" ? "away" : "online";
        state.userStatus = newStatus;

        DOM.userStatusPill.className = `user-status-toggle status-${newStatus}`;
        DOM.userStatusText.textContent = newStatus === "online" ? "Online" : "Away";

        if (state.socket && state.isConnected && state.currentRoom) {
            state.socket.emit("user_status", { status: newStatus });
        }
        showToast(`Your status is now ${newStatus.toUpperCase()}`, "info", 2000);
    }

    /* ==========================================================================
       Modals: Create Room, Room Info, Message Search
       ========================================================================== */

    function openCreateRoomModal() {
        DOM.newRoomName.value = "";
        DOM.newRoomDesc.value = "";
        DOM.createRoomErrorBox.classList.add("hidden");
        DOM.createRoomModal.classList.remove("hidden");
        DOM.newRoomName.focus();
    }

    function closeCreateRoomModal() {
        DOM.createRoomModal.classList.add("hidden");
    }

    async function handleCreateRoomSubmit(e) {
        if (e) e.preventDefault();

        const name = (DOM.newRoomName.value || "").trim().toLowerCase();
        const description = (DOM.newRoomDesc.value || "").trim();

        if (!name || name.length < 2) {
            showCreateRoomError("Channel name must be at least 2 characters.");
            return;
        }

        try {
            const res = await fetch("/api/rooms", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name: name,
                    description: description,
                    created_by: state.currentUser || "anonymous",
                }),
            });

            const data = await res.json();
            if (!res.ok) {
                showCreateRoomError(data.error || "Failed to create channel.");
                return;
            }

            closeCreateRoomModal();
            showToast(`Channel #${name} created successfully!`, "success");

            await fetchRoomsList();
            switchChannel(name);

        } catch (err) {
            showCreateRoomError("Server communication error.");
        }
    }

    function showCreateRoomError(msg) {
        DOM.createRoomErrorText.textContent = msg;
        DOM.createRoomErrorBox.classList.remove("hidden");
    }

    async function openRoomInfoModal() {
        DOM.infoRoomName.textContent = `#${state.currentRoom}`;
        DOM.infoRoomDescription.textContent = state.currentRoomDescription || "No channel description provided.";
        DOM.infoRoomMembersCount.textContent = state.onlineUsers.length;
        DOM.infoRoomCreator.textContent = "team";
        DOM.pinnedMessagesList.replaceChildren();

        DOM.roomInfoModal.classList.remove("hidden");

        try {
            const infoRes = await fetch(`/api/rooms/${encodeURIComponent(state.currentRoom)}/info`);
            if (infoRes.ok) {
                const data = await infoRes.json();
                const r = data.room;
                DOM.infoRoomDescription.textContent = r.description || "No channel description provided.";
                DOM.infoRoomCreator.textContent = r.created_by || "system";
                DOM.infoRoomPinsCount.textContent = r.pinned_count || 0;
            }

            const pinRes = await fetch(`/api/rooms/${encodeURIComponent(state.currentRoom)}/pinned`);
            if (pinRes.ok) {
                const pinData = await pinRes.json();
                renderPinnedMessagesList(pinData.pinned_messages || []);
            }
        } catch (e) {
            logger("Failed to load room details:", e);
        }
    }

    function closeRoomInfoModal() {
        DOM.roomInfoModal.classList.add("hidden");
    }

    function renderPinnedMessagesList(pinnedMessages) {
        DOM.pinnedMessagesList.replaceChildren();

        if (pinnedMessages.length === 0) {
            const empty = document.createElement("div");
            empty.style.padding = "16px";
            empty.style.textAlign = "center";
            empty.style.color = "var(--text-muted)";
            empty.textContent = "No pinned messages in this channel yet.";
            DOM.pinnedMessagesList.appendChild(empty);
            return;
        }

        pinnedMessages.forEach((msg) => {
            const card = document.createElement("div");
            card.className = "pinned-card";

            const header = document.createElement("div");
            header.className = "card-top-row";

            const author = document.createElement("span");
            author.className = "card-author";
            author.textContent = msg.username;

            const time = document.createElement("span");
            time.className = "message-time";
            time.textContent = formatTime(msg.pinned_at || msg.timestamp);

            header.appendChild(author);
            header.appendChild(time);

            const text = document.createElement("div");
            text.className = "card-text";
            text.textContent = msg.content || msg.message || "";

            card.appendChild(header);
            card.appendChild(text);

            card.addEventListener("click", () => {
                closeRoomInfoModal();
                jumpToMessageInFeed(msg.id);
            });

            DOM.pinnedMessagesList.appendChild(card);
        });
    }

    function openMsgSearchModal() {
        DOM.searchCurrentRoomName.textContent = state.currentRoom;
        DOM.inRoomSearchInput.value = "";
        DOM.searchResultsContainer.replaceChildren();

        const emptyNotice = document.createElement("div");
        emptyNotice.style.padding = "20px";
        emptyNotice.style.textAlign = "center";
        emptyNotice.style.color = "var(--text-muted)";
        emptyNotice.textContent = "Enter a search term to find messages in this channel.";
        DOM.searchResultsContainer.appendChild(emptyNotice);

        DOM.msgSearchModal.classList.remove("hidden");
        DOM.inRoomSearchInput.focus();
    }

    function closeMsgSearchModal() {
        DOM.msgSearchModal.classList.add("hidden");
    }

    async function handleInRoomSearchInput() {
        const query = (DOM.inRoomSearchInput.value || "").trim();
        if (state.searchDebounceTimer) clearTimeout(state.searchDebounceTimer);

        if (!query) {
            DOM.searchResultsContainer.replaceChildren();
            return;
        }

        state.searchDebounceTimer = setTimeout(async () => {
            try {
                const res = await fetch(`/api/rooms/${encodeURIComponent(state.currentRoom)}/search?q=${encodeURIComponent(query)}`);
                if (res.ok) {
                    const data = await res.json();
                    renderSearchResults(data.results || [], query);
                }
            } catch (e) {
                logger("Search request failed:", e);
            }
        }, 250);
    }

    function renderSearchResults(results, query) {
        DOM.searchResultsContainer.replaceChildren();

        if (results.length === 0) {
            const empty = document.createElement("div");
            empty.style.padding = "20px";
            empty.style.textAlign = "center";
            empty.style.color = "var(--text-muted)";
            empty.textContent = `No messages matching "${query}" in #${state.currentRoom}.`;
            DOM.searchResultsContainer.appendChild(empty);
            return;
        }

        results.forEach((msg) => {
            const card = document.createElement("div");
            card.className = "search-result-card";

            const header = document.createElement("div");
            header.className = "card-top-row";

            const author = document.createElement("span");
            author.className = "card-author";
            author.textContent = msg.username;
            if (msg.username_color) author.style.color = msg.username_color;

            const time = document.createElement("span");
            time.className = "message-time";
            time.textContent = formatTime(msg.timestamp);

            header.appendChild(author);
            header.appendChild(time);

            const content = document.createElement("div");
            content.className = "card-text";
            content.textContent = msg.content || msg.message || "";

            card.appendChild(header);
            card.appendChild(content);

            card.addEventListener("click", () => {
                closeMsgSearchModal();
                jumpToMessageInFeed(msg.id);
            });

            DOM.searchResultsContainer.appendChild(card);
        });
    }

    /* ==========================================================================
       Scroll Management
       ========================================================================== */

    function scrollToBottom(instant = false) {
        if (!DOM.messagesContainer) return;
        DOM.messagesContainer.scrollTo({
            top: DOM.messagesContainer.scrollHeight,
            behavior: instant ? "instant" : "smooth",
        });
        state.unreadCount = 0;
        updateScrollBottomButton();
    }

    function handleScroll() {
        const el = DOM.messagesContainer;
        const threshold = 80;
        const isUp = el.scrollHeight - el.scrollTop - el.clientHeight > threshold;
        state.isUserScrolledUp = isUp;

        if (!isUp) {
            state.unreadCount = 0;
        }
        updateScrollBottomButton();
    }

    function updateScrollBottomButton() {
        if (state.isUserScrolledUp) {
            DOM.scrollBottomBtn.classList.remove("hidden");
            if (state.unreadCount > 0) {
                DOM.unreadCounter.classList.remove("hidden");
                DOM.unreadCounter.textContent = state.unreadCount > 99 ? "99+" : state.unreadCount;
            } else {
                DOM.unreadCounter.classList.add("hidden");
            }
        } else {
            DOM.scrollBottomBtn.classList.add("hidden");
            DOM.unreadCounter.classList.add("hidden");
        }
    }

    /* ==========================================================================
       Form & Input Validation & Handlers
       ========================================================================== */

    function clearJoinErrors() {
        DOM.joinErrorBox.classList.add("hidden");
        DOM.joinErrorText.textContent = "";
        DOM.usernameInput.classList.remove("is-invalid");
        DOM.roomInput.classList.remove("is-invalid");
        DOM.usernameError.textContent = "";
        DOM.roomError.textContent = "";
    }

    function showJoinError(message, inputElement, errorElement) {
        if (inputElement) inputElement.classList.add("is-invalid");
        if (errorElement) errorElement.textContent = message;
        DOM.joinErrorText.textContent = message;
        DOM.joinErrorBox.classList.remove("hidden");
    }

    function updateSendButtonState() {
        const text = (DOM.messageInput.value || "").trim();
        const isValid = text.length > 0 && text.length <= CONFIG.maxMessageLen && state.isConnected;
        DOM.sendMsgBtn.disabled = !isValid;

        const currentLen = (DOM.messageInput.value || "").length;
        DOM.charCounter.textContent = `${currentLen} / ${CONFIG.maxMessageLen}`;
        if (currentLen > CONFIG.maxMessageLen) {
            DOM.charCounter.style.color = "var(--danger)";
        } else {
            DOM.charCounter.style.color = "var(--text-muted)";
        }
    }

    function handleJoinSubmit(e) {
        if (e) e.preventDefault();
        clearJoinErrors();

        const username = (DOM.usernameInput.value || "").trim();
        const room = (DOM.roomInput.value || "").trim().toLowerCase();

        if (!username) {
            showJoinError("Username is required.", DOM.usernameInput, DOM.usernameError);
            DOM.usernameInput.focus();
            return;
        }
        if (username.length < 2) {
            showJoinError("Username must be at least 2 characters.", DOM.usernameInput, DOM.usernameError);
            DOM.usernameInput.focus();
            return;
        }
        if (!room) {
            showJoinError("Room name is required.", DOM.roomInput, DOM.roomError);
            DOM.roomInput.focus();
            return;
        }
        if (room.length < 2) {
            showJoinError("Room name must be at least 2 characters.", DOM.roomInput, DOM.roomError);
            DOM.roomInput.focus();
            return;
        }

        DOM.messagesLoading.classList.remove("hidden");
        DOM.emptyChatState.classList.add("hidden");

        const socket = initSocket();
        socket.emit("join_room", { username, room });
    }

    function handleSendMessage(e) {
        if (e) e.preventDefault();
        if (!state.socket || !state.isConnected) {
            showToast("Cannot send message: Disconnected from server.", "error");
            return;
        }

        const rawMessage = DOM.messageInput.value;
        const text = rawMessage.trim();

        if (!text) return;

        if (text.length > CONFIG.maxMessageLen) {
            showToast(`Message exceeds maximum limit of ${CONFIG.maxMessageLen} characters.`, "error");
            return;
        }

        const payload = {
            message: text,
            room: state.currentRoom,
            reply_to_id: state.replyingTo ? state.replyingTo.id : null,
        };

        state.socket.emit("send_message", payload);

        DOM.messageInput.value = "";
        DOM.messageInput.style.height = "auto";
        updateSendButtonState();
        stopTypingImmediately();
        cancelReply();
        DOM.messageInput.focus();
    }

    function handleLeaveRoom() {
        if (state.socket) {
            state.socket.emit("leave_room", { room: state.currentRoom });
        }
        resetChatState();
    }

    function resetChatState() {
        state.currentUser = "";
        state.currentRoom = "";
        state.onlineUsers = [];
        state.activeTypers.clear();
        state.unreadCount = 0;
        state.isUserScrolledUp = false;
        state.replyingTo = null;

        DOM.messagesFeed.replaceChildren();
        DOM.onlineUsersList.replaceChildren();
        DOM.typingIndicatorBar.classList.add("hidden");
        DOM.replyingBanner.classList.add("hidden");
        DOM.chatScreen.classList.add("hidden");
        DOM.joinScreen.classList.remove("hidden");
        clearJoinErrors();
    }

    /* ==========================================================================
       Typing Indicator Throttling & Debounce
       ========================================================================== */

    function handleTypingInput() {
        updateSendButtonState();

        DOM.messageInput.style.height = "auto";
        DOM.messageInput.style.height = `${Math.min(DOM.messageInput.scrollHeight, 120)}px`;

        if (!state.socket || !state.isConnected || !state.currentRoom || !state.currentUser) return;

        const now = Date.now();
        if (now - state.lastTypingEmitTime > 1000) {
            state.socket.emit("typing_start", {
                username: state.currentUser,
                room: state.currentRoom,
            });
            state.lastTypingEmitTime = now;
        }

        if (state.typingTimer) clearTimeout(state.typingTimer);
        state.typingTimer = setTimeout(() => {
            stopTypingImmediately();
        }, 1500);
    }

    function stopTypingImmediately() {
        if (state.typingTimer) {
            clearTimeout(state.typingTimer);
            state.typingTimer = null;
        }
        if (state.socket && state.isConnected && state.currentRoom && state.currentUser) {
            state.socket.emit("typing_stop", {
                username: state.currentUser,
                room: state.currentRoom,
            });
            state.lastTypingEmitTime = 0;
        }
    }

    function updateTypingDisplay() {
        const typers = Array.from(state.activeTypers);

        if (typers.length === 0) {
            DOM.typingIndicatorBar.classList.add("hidden");
            return;
        }

        DOM.typingIndicatorBar.classList.remove("hidden");

        if (typers.length === 1) {
            DOM.typingText.textContent = `${typers[0]} is typing...`;
        } else if (typers.length === 2) {
            DOM.typingText.textContent = `${typers[0]} and ${typers[1]} are typing...`;
        } else {
            DOM.typingText.textContent = `${typers[0]} and ${typers.length - 1} others are typing...`;
        }
    }

    /* ==========================================================================
       Event Listeners Initialization
       ========================================================================== */

    function initEvents() {
        DOM.joinForm.addEventListener("submit", handleJoinSubmit);

        DOM.presetPills.forEach((pill) => {
            pill.addEventListener("click", () => {
                DOM.presetPills.forEach((p) => p.classList.remove("active"));
                pill.classList.add("active");
                DOM.roomInput.value = pill.getAttribute("data-room");
                DOM.roomInput.focus();
            });
        });

        DOM.messageInput.addEventListener("input", handleTypingInput);
        DOM.messageInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
            }
        });

        DOM.messageForm.addEventListener("submit", handleSendMessage);
        DOM.cancelReplyBtn.addEventListener("click", cancelReply);

        DOM.quickEmojiBtns.forEach((btn) => {
            btn.addEventListener("click", () => {
                const emoji = btn.getAttribute("data-emoji");
                DOM.messageInput.value += emoji;
                updateSendButtonState();
                DOM.messageInput.focus();
            });
        });

        DOM.leaveRoomBtn.addEventListener("click", () => {
            if (confirm("Are you sure you want to leave this room?")) {
                handleLeaveRoom();
            }
        });

        DOM.messagesContainer.addEventListener("scroll", handleScroll);
        DOM.scrollBottomBtn.addEventListener("click", () => scrollToBottom(false));

        DOM.channelSearchInput.addEventListener("input", () => {
            renderChannelsList(state.allRooms);
        });

        DOM.userStatusPill.addEventListener("click", toggleUserPresence);

        DOM.openCreateRoomModalBtn.addEventListener("click", openCreateRoomModal);
        DOM.closeCreateRoomModalBtn.addEventListener("click", closeCreateRoomModal);
        DOM.cancelCreateRoomBtn.addEventListener("click", closeCreateRoomModal);
        DOM.createRoomForm.addEventListener("submit", handleCreateRoomSubmit);

        DOM.roomInfoBtn.addEventListener("click", openRoomInfoModal);
        DOM.closeRoomInfoModalBtn.addEventListener("click", closeRoomInfoModal);

        DOM.openMsgSearchBtn.addEventListener("click", openMsgSearchModal);
        DOM.closeMsgSearchModalBtn.addEventListener("click", closeMsgSearchModal);
        DOM.inRoomSearchInput.addEventListener("input", handleInRoomSearchInput);

        if (DOM.sidebarToggleBtn) {
            DOM.sidebarToggleBtn.addEventListener("click", () => {
                DOM.usersSidebar.classList.add("open");
                DOM.sidebarBackdrop.classList.remove("hidden");
            });
        }
        if (DOM.sidebarCloseBtn) {
            DOM.sidebarCloseBtn.addEventListener("click", () => {
                DOM.usersSidebar.classList.remove("open");
                DOM.sidebarBackdrop.classList.add("hidden");
            });
        }
        if (DOM.sidebarBackdrop) {
            DOM.sidebarBackdrop.addEventListener("click", () => {
                DOM.usersSidebar.classList.remove("open");
                DOM.sidebarBackdrop.classList.add("hidden");
            });
        }

        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") {
                closeCreateRoomModal();
                closeRoomInfoModal();
                closeMsgSearchModal();
                cancelReply();
            }
        });

        initSocket();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initEvents);
    } else {
        initEvents();
    }
})();
