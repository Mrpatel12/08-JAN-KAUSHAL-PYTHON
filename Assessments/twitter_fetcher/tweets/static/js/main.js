document.addEventListener("DOMContentLoaded", () => {
    // Initialize Lucide Icons
    lucide.createIcons();

    // DOM Elements
    const searchForm = document.getElementById("search-form");
    const usernameInput = document.getElementById("username-input");
    const searchSubmitBtn = searchForm.querySelector(".search-submit-btn");
    const btnText = searchSubmitBtn.querySelector(".btn-text");
    const loaderSpinner = searchSubmitBtn.querySelector(".loader-spinner");

    const statusBanner = document.getElementById("status-banner");
    const dismissBannerBtn = document.getElementById("dismiss-banner");

    const profileCard = document.getElementById("profile-card");
    const profileAvatar = document.getElementById("profile-avatar");
    const profileName = document.getElementById("profile-name");
    const profileHandle = document.getElementById("profile-handle");
    const profileBio = document.getElementById("profile-bio");
    const profileVerified = document.getElementById("profile-verified");
    const badgeMode = document.getElementById("badge-mode");

    const statFollowing = document.getElementById("stat-following");
    const statFollowers = document.getElementById("stat-followers");
    const statTweets = document.getElementById("stat-tweets");

    const tweetsFeed = document.getElementById("tweets-feed");
    const skeletonLoader = document.getElementById("skeleton-loader");

    const developerForm = document.getElementById("credentials-form");
    const statusCodeSelect = document.getElementById("status-code-select");
    const latencySelect = document.getElementById("latency-select");
    const settingsCard = document.getElementById("settings-card");
    const toggleSettingsBtn = document.getElementById("toggle-settings-btn");

    const searchHistoryList = document.getElementById("search-history");
    const clearHistoryBtn = document.getElementById("clear-history");

    const toastContainer = document.getElementById("toast-container");

    // Local State
    let searchHistory = JSON.parse(localStorage.getItem("twitter_search_history") || "[]");

    // ==========================================================================
    // Initialization & Theme Handling
    // ==========================================================================
    
    // Set initial developer settings
    statusCodeSelect.value = INITIAL_STATUS;
    latencySelect.value = INITIAL_LATENCY.toString();

    // Theme selector
    const themeButtons = document.querySelectorAll(".theme-btn");
    const savedTheme = localStorage.getItem("twitter_theme") || "dim";
    setTheme(savedTheme);

    themeButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const theme = btn.getAttribute("data-theme");
            setTheme(theme);
        });
    });

    function setTheme(theme) {
        document.body.classList.remove("dim-theme", "dark-theme", "light-theme");
        document.body.classList.add(`${theme}-theme`);
        localStorage.setItem("twitter_theme", theme);

        themeButtons.forEach(b => {
            if (b.getAttribute("data-theme") === theme) {
                b.classList.add("active");
            } else {
                b.classList.remove("active");
            }
        });
    }

    // Render search history
    renderHistory();

    // Setup preset chips
    document.querySelectorAll(".preset-chip").forEach(chip => {
        chip.addEventListener("click", () => {
            const username = chip.textContent.trim();
            usernameInput.value = username;
            triggerSearch(username);
        });
    });

    // Dismiss banner
    if (dismissBannerBtn) {
        dismissBannerBtn.addEventListener("click", () => {
            statusBanner.style.display = "none";
        });
    }

    // ==========================================================================
    // Search Actions & AJAX Fetch
    // ==========================================================================
    
    searchForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const username = usernameInput.value.trim();
        if (username) {
            triggerSearch(username);
        }
    });

    function triggerSearch(username) {
        username = username.replace("@", "").trim();
        if (!username) return;

        setLoadingState(true);
        
        fetch(`/api/fetch-tweets/?username=${encodeURIComponent(username)}`)
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.error || "Failed to fetch tweets") });
                }
                return response.json();
            })
            .then(data => {
                setLoadingState(false);
                displayResults(data);
                addToHistory(data.user.username, data.user.name);
            })
            .catch(error => {
                setLoadingState(false);
                showToast(error.message, "error");
                
                // Show failed state in the feed panel
                tweetsFeed.innerHTML = `
                    <div class="empty-feed">
                        <div class="empty-icon-wrapper" style="background-color: rgba(239, 68, 68, 0.1); color: var(--color-danger-red);">
                            <i data-lucide="alert-circle" style="width: 42px; height: 42px;"></i>
                        </div>
                        <h2>Fetch Failed</h2>
                        <p>${error.message}</p>
                    </div>
                `;
                lucide.createIcons();
            });
    }

    function setLoadingState(isLoading) {
        if (isLoading) {
            btnText.style.display = "none";
            loaderSpinner.style.display = "block";
            searchSubmitBtn.disabled = true;
            usernameInput.disabled = true;

            profileCard.style.display = "none";
            tweetsFeed.style.display = "none";
            skeletonLoader.style.display = "flex";
        } else {
            btnText.style.display = "block";
            loaderSpinner.style.display = "none";
            searchSubmitBtn.disabled = false;
            usernameInput.disabled = false;

            skeletonLoader.style.display = "none";
            tweetsFeed.style.display = "flex";
        }
    }

    // ==========================================================================
    // Render Results (Profile & Tweets)
    // ==========================================================================
    
    function displayResults(data) {
        const user = data.user;
        const tweets = data.tweets;

        // Update status banner
        statusBanner.className = "status-banner banner-mock";
        statusBanner.querySelector(".banner-text").innerHTML = `
            <strong>Developer Mock Mode Active</strong> - Viewing simulated high-fidelity data for @${user.username}.
        `;
        statusBanner.style.display = "flex";
        
        badgeMode.textContent = "DEV MOCK";
        badgeMode.className = "badge badge-mock";

        // 1. Populate Profile Card
        profileAvatar.src = user.profile_image_url;
        profileName.textContent = user.name;
        profileHandle.textContent = user.username;
        profileBio.textContent = user.description || "No bio description set.";
        
        if (user.verified) {
            profileVerified.style.display = "inline-block";
        } else {
            profileVerified.style.display = "none";
        }

        statFollowing.textContent = formatNumber(user.following_count);
        statFollowers.textContent = formatNumber(user.followers_count);
        statTweets.textContent = formatNumber(user.tweet_count);

        profileCard.style.display = "flex";

        // 2. Populate Tweets List
        tweetsFeed.innerHTML = "";
        if (tweets.length === 0) {
            tweetsFeed.innerHTML = `
                <div class="empty-feed">
                    <div class="empty-icon-wrapper">
                        <i data-lucide="message-square-off" style="width: 42px; height: 42px;"></i>
                    </div>
                    <h2>No tweets found</h2>
                    <p>@{user.username} hasn't posted any tweets recently.</p>
                </div>
            `;
        } else {
            tweets.forEach((tweet, index) => {
                const formattedText = parseTweetText(tweet.text);
                const relativeTime = getRelativeTime(tweet.created_at);
                const isLiked = localStorage.getItem(`liked_${tweet.id}`) === "true";

                const tweetCardHtml = `
                    <article class="tweet-card" style="animation-delay: ${index * 0.08}s">
                        <img class="tweet-avatar" src="${user.profile_image_url}" alt="${user.name}">
                        <div class="tweet-main">
                            <div class="tweet-header">
                                <a href="#" class="tweet-author-name">${user.name}</a>
                                ${user.verified ? `<svg class="tweet-verified-badge" viewBox="0 0 24 24"><path fill="currentColor" d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.99-3.818-3.99-.48 0-.941.1-1.358.275C14.77 2.52 13.5 1.5 12 1.5s-2.77 1.02-3.412 2.285C8.17 3.6 7.71 3.5 7.23 3.5 5.122 3.5 3.41 5.28 3.41 7.5c0 .495.084.965.238 1.4-1.273.65-2.148 2.02-2.148 3.6 0 1.58.875 2.95 2.148 3.6-.154.435-.238.905-.238 1.4 0 2.21 1.71 3.99 3.818 3.99.48 0 .941-.1 1.358-.275C9.23 21.48 10.5 22.5 12 22.5s2.77-1.02 3.412-2.285c.418.175.878.275 1.358.275 2.108 0 3.818-1.78 3.818-3.99 0-.495-.084-.965-.238-1.4 1.273-.65 2.148-2.02 2.148-3.6zm-12.72 4.41l-3.32-3.32 1.41-1.42 1.91 1.9 5.3-5.3 1.41 1.42-6.71 6.72z"/></svg>` : ""}
                                <span class="tweet-handle">@${user.username}</span>
                                <span class="tweet-dot">&middot;</span>
                                <a href="#" class="tweet-time" title="${formatDateTime(tweet.created_at)}">${relativeTime}</a>
                            </div>
                            <div class="tweet-body">${formattedText}</div>
                            <div class="tweet-footer">
                                <button class="action-btn btn-reply" title="Reply">
                                    <i data-lucide="message-circle"></i>
                                    <span>${formatNumber(tweet.replies)}</span>
                                </button>
                                <button class="action-btn btn-retweet" title="Retweet">
                                    <i data-lucide="repeat"></i>
                                    <span>${formatNumber(tweet.retweets)}</span>
                                </button>
                                <button class="action-btn btn-like ${isLiked ? 'liked' : ''}" data-tweet-id="${tweet.id}" title="Like">
                                    <i data-lucide="heart"></i>
                                    <span class="like-count">${formatNumber(tweet.likes + (isLiked ? 1 : 0))}</span>
                                </button>
                                <button class="action-btn btn-views" title="Views">
                                    <i data-lucide="bar-chart-3"></i>
                                    <span>${formatNumber(tweet.views)}</span>
                                </button>
                            </div>
                        </div>
                    </article>
                `;
                tweetsFeed.insertAdjacentHTML("beforeend", tweetCardHtml);
            });

            setupLikeButtons();
        }

        lucide.createIcons();
    }

    function setupLikeButtons() {
        document.querySelectorAll(".btn-like").forEach(btn => {
            btn.addEventListener("click", () => {
                const tweetId = btn.getAttribute("data-tweet-id");
                const countSpan = btn.querySelector(".like-count");
                let isLiked = btn.classList.contains("liked");
                
                let currentCount = parseFormattedNumber(countSpan.textContent);

                if (isLiked) {
                    btn.classList.remove("liked");
                    localStorage.setItem(`liked_${tweetId}`, "false");
                    countSpan.textContent = formatNumber(Math.max(0, currentCount - 1));
                } else {
                    btn.classList.add("liked");
                    localStorage.setItem(`liked_${tweetId}`, "true");
                    countSpan.textContent = formatNumber(currentCount + 1);
                    
                    const icon = btn.querySelector("i");
                    icon.style.transform = "scale(1.4)";
                    setTimeout(() => {
                        icon.style.transform = "scale(1)";
                    }, 200);
                }
            });
        });
    }

    // ==========================================================================
    // Developer Controls Form AJAX Action
    // ==========================================================================
    
    developerForm.addEventListener("submit", (e) => {
        e.preventDefault();
        
        const latency = parseFloat(latencySelect.value);
        const status_code = statusCodeSelect.value;

        fetch("/api/update-credentials/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": DJANGO_CSRF_TOKEN
            },
            body: JSON.stringify({ latency: latency, status_code: status_code })
        })
        .then(response => {
            if (!response.ok) throw new Error("Failed to update configurations");
            return response.json();
        })
        .then(data => {
            showToast(data.message, "success");

            // If a search is currently active, prompt a refresh to apply mock conditions
            const activeUsername = profileHandle.textContent;
            if (profileCard.style.display !== "none" && activeUsername) {
                showToast(`Re-fetching @${activeUsername} with new settings...`, "info");
                triggerSearch(activeUsername);
            }
        })
        .catch(error => {
            showToast(error.message, "error");
        });
    });

    // Highlight controls panel
    toggleSettingsBtn.addEventListener("click", (e) => {
        e.preventDefault();
        settingsCard.scrollIntoView({ behavior: "smooth" });
        settingsCard.style.outline = "2px solid var(--color-twitter-blue)";
        setTimeout(() => {
            settingsCard.style.transition = "outline var(--transition-normal)";
            settingsCard.style.outline = "2px solid transparent";
        }, 1500);
    });

    // ==========================================================================
    // Search History Storage & UI Manager
    // ==========================================================================
    
    function addToHistory(username, name) {
        username = username.toLowerCase().trim();
        searchHistory = searchHistory.filter(item => item.username.toLowerCase() !== username);
        searchHistory.unshift({ username, name });
        if (searchHistory.length > 8) searchHistory.pop();
        
        localStorage.setItem("twitter_search_history", JSON.stringify(searchHistory));
        renderHistory();
    }

    function renderHistory() {
        searchHistoryList.innerHTML = "";
        
        if (searchHistory.length === 0) {
            searchHistoryList.innerHTML = `<li class="history-empty">No recent searches</li>`;
            clearHistoryBtn.style.display = "none";
            return;
        }

        clearHistoryBtn.style.display = "block";
        searchHistory.forEach(item => {
            const li = document.createElement("li");
            li.className = "history-item";
            li.innerHTML = `
                <div class="history-link" data-username="${item.username}">
                    <i data-lucide="search"></i>
                    <span>@${item.username}</span>
                </div>
                <button class="history-remove-btn" data-username="${item.username}" title="Remove from history">
                    <i data-lucide="x"></i>
                </button>
            `;
            searchHistoryList.appendChild(li);
        });

        searchHistoryList.querySelectorAll(".history-link").forEach(link => {
            link.addEventListener("click", () => {
                const username = link.getAttribute("data-username");
                usernameInput.value = username;
                triggerSearch(username);
            });
        });

        searchHistoryList.querySelectorAll(".history-remove-btn").forEach(btn => {
            btn.addEventListener("click", (e) => {
                e.stopPropagation();
                const username = btn.getAttribute("data-username");
                searchHistory = searchHistory.filter(item => item.username.toLowerCase() !== username.toLowerCase());
                localStorage.setItem("twitter_search_history", JSON.stringify(searchHistory));
                renderHistory();
            });
        });

        lucide.createIcons();
    }

    clearHistoryBtn.addEventListener("click", () => {
        searchHistory = [];
        localStorage.removeItem("twitter_search_history");
        renderHistory();
        showToast("Search history cleared", "info");
    });

    // ==========================================================================
    // String Formatters & Parser Helpers
    // ==========================================================================
    
    function parseTweetText(text) {
        if (!text) return "";
        let sanitized = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");

        // Link URLs
        sanitized = sanitized.replace(
            /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig,
            '<a href="$1" target="_blank" rel="noopener">$1</a>'
        );

        // Link Handles
        sanitized = sanitized.replace(
            /(^|\s)@(\w+)/g,
            '$1<a href="#" class="tweet-mention" onclick="event.preventDefault(); document.getElementById(\'username-input\').value=\'$2\'; document.getElementById(\'search-form\').dispatchEvent(new Event(\'submit\'));">@$2</a>'
        );

        // Link Hashtags
        sanitized = sanitized.replace(
            /(^|\s)#(\w+)/g,
            '$1<span class="tweet-hashtag">#$2</span>'
        );

        return sanitized;
    }

    function getRelativeTime(isoString) {
        const date = new Date(isoString);
        const now = new Date();
        const diffMs = now - date;
        const diffSeconds = Math.floor(diffMs / 1000);
        const diffMinutes = Math.floor(diffSeconds / 60);
        const diffHours = Math.floor(diffMinutes / 60);
        const diffDays = Math.floor(diffHours / 24);

        if (diffSeconds < 60) return "just now";
        if (diffMinutes < 60) return `${diffMinutes}m`;
        if (diffHours < 24) return `${diffHours}h`;
        if (diffDays < 7) return `${diffDays}d`;
        
        return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
    }

    function formatDateTime(isoString) {
        const date = new Date(isoString);
        return date.toLocaleString("en-US", {
            hour: "numeric",
            minute: "2-digit",
            hour12: true,
            day: "numeric",
            month: "short",
            year: "numeric"
        });
    }

    function formatNumber(num) {
        if (!num) return "0";
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1).replace(/\.0$/, "") + "M";
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1).replace(/\.0$/, "") + "K";
        }
        return num.toLocaleString();
    }

    function parseFormattedNumber(str) {
        str = str.trim().toUpperCase();
        if (str.endsWith("M")) {
            return parseFloat(str.slice(0, -1)) * 1000000;
        }
        if (str.endsWith("K")) {
            return parseFloat(str.slice(0, -1)) * 1000;
        }
        return parseInt(str.replace(/,/g, ""), 10) || 0;
    }

    // ==========================================================================
    // Dynamic Toast Notification System
    // ==========================================================================
    
    function showToast(message, type = "info") {
        const toast = document.createElement("div");
        toast.className = `toast toast-${type}`;
        
        let iconName = "info";
        if (type === "success") iconName = "check-circle";
        if (type === "error") iconName = "alert-triangle";
        if (type === "warning") iconName = "alert-circle";

        toast.innerHTML = `
            <i class="toast-icon" data-lucide="${iconName}"></i>
            <span>${message}</span>
        `;
        
        toastContainer.appendChild(toast);
        lucide.createIcons();

        setTimeout(() => {
            toast.style.transform = "translateX(120%)";
            toast.style.opacity = "0";
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3500);
    }
});
