(function () {
  "use strict";

  var THEME_KEY = "reading-room-theme";
  var LAST_READ_KEY = "reading-room-last-read";
  var SCROLL_PREFIX = "reading-room-scroll:";

  function safeGet(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function safeSet(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* ignore */ }
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
  }

  function initTheme() {
    var saved = safeGet(THEME_KEY);
    if (saved) applyTheme(saved);

    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var current = document.documentElement.getAttribute("data-theme") || "light";
      var next = current === "dark" ? "light" : "dark";
      applyTheme(next);
      safeSet(THEME_KEY, next);
    });
  }

  function initContinueReading() {
    var banner = document.getElementById("continue-reading");
    var link = document.getElementById("continue-reading-link");
    if (!banner || !link) return;

    var raw = safeGet(LAST_READ_KEY);
    if (!raw) return;

    var data;
    try { data = JSON.parse(raw); } catch (e) { return; }
    if (!data || !data.url || data.url === window.location.pathname) return;

    link.href = data.url;
    link.textContent = data.title || "your last story";
    banner.hidden = false;
  }

  function initChapterTracking() {
    var article = document.querySelector(".chapter");
    if (!article) return;

    var url = window.location.pathname;
    var storyTitle = document.querySelector(".chapter-story-title");
    var title = storyTitle ? storyTitle.textContent.trim() : document.title;

    safeSet(LAST_READ_KEY, JSON.stringify({ url: url, title: title }));

    var scrollKey = SCROLL_PREFIX + url;
    var savedScroll = safeGet(scrollKey);
    if (savedScroll) {
      requestAnimationFrame(function () {
        window.scrollTo(0, parseInt(savedScroll, 10) || 0);
      });
    }

    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        safeSet(scrollKey, String(window.scrollY));
        ticking = false;
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTheme();
    initContinueReading();
    initChapterTracking();
  });
})();
