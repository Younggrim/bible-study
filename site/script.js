/* Bible Study Site — Shared JavaScript */

/* ESV API Configuration — via Cloudflare Worker proxy */
var ESV_PROXY_URL = 'https://esv-proxy.cloudflare-dust598.workers.dev';

/* Service worker registration — every page, not just index.html/devotional.html,
   so offline caching and the install prompt below both work regardless of
   which page someone lands on first (a shared chapter link, a bookmark, etc). */
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js').catch(function() {});
}

/* ===== Add-to-Home-Screen install banner — site-wide =====
   Moved here from index.html so every entry point (a shared chapter link,
   a topical study, the devotional page) offers the install nudge, not just
   the homepage. Guards against double-injection in case a page already has
   its own #install-banner markup. */
(function() {
  if (document.getElementById('install-banner')) return;
  if (window.matchMedia('(display-mode: standalone)').matches || navigator.standalone) return;
  if (localStorage.getItem('install-banner-dismissed')) return;

  function buildBanner() {
    var wrap = document.createElement('div');
    wrap.id = 'install-banner';
    wrap.style.cssText = "display:none;position:fixed;bottom:0;left:0;right:0;z-index:9999;background:linear-gradient(135deg,#3d2b1f 0%,#5a3e2b 100%);color:#fff;padding:16px 20px;box-shadow:0 -4px 20px rgba(0,0,0,0.3);font-family:'Inter',sans-serif;";
    wrap.innerHTML =
      '<div style="max-width:600px;margin:0 auto;display:flex;align-items:center;gap:14px;">'
      + '<img src="site/icon-192.png" alt="Bible Study" style="width:48px;height:48px;border-radius:10px;flex-shrink:0;">'
      + '<div style="flex:1;">'
      + '<div style="font-weight:600;font-size:0.95rem;margin-bottom:4px;">Add Bible Study to Home Screen</div>'
      + '<div id="install-instructions" style="font-size:0.8rem;color:#ddd;line-height:1.4;"></div>'
      + '</div>'
      + '<button id="install-btn" style="background:#f0c865;color:#3d2b1f;border:none;padding:10px 18px;border-radius:8px;font-weight:700;font-size:0.85rem;cursor:pointer;white-space:nowrap;">Install</button>'
      + '<button id="install-dismiss" style="background:none;border:none;color:#aaa;font-size:1.4rem;cursor:pointer;padding:4px 8px;line-height:1;" aria-label="Dismiss">&times;</button>'
      + '</div>';
    document.body.appendChild(wrap);
    return wrap;
  }

  var banner = null, installBtn, dismissBtn, instructions, deferredPrompt = null;

  function ensureBanner() {
    if (!banner) {
      banner = buildBanner();
      installBtn = document.getElementById('install-btn');
      dismissBtn = document.getElementById('install-dismiss');
      instructions = document.getElementById('install-instructions');

      installBtn.addEventListener('click', function() {
        if (deferredPrompt) {
          deferredPrompt.prompt();
          deferredPrompt.userChoice.then(function() {
            deferredPrompt = null;
            banner.style.display = 'none';
          });
        }
      });
      dismissBtn.addEventListener('click', function() {
        banner.style.display = 'none';
        localStorage.setItem('install-banner-dismissed', '1');
      });
    }
    return banner;
  }

  // Android / Chrome — catches the native install prompt
  window.addEventListener('beforeinstallprompt', function(e) {
    e.preventDefault();
    deferredPrompt = e;
    var b = ensureBanner();
    instructions.textContent = 'Get quick access like a native app — works offline too.';
    b.style.display = 'block';
  });

  // iOS Safari — no native prompt exists, so show manual instructions
  var isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  var isSafari = /Safari/.test(navigator.userAgent) && !/CriOS|FxiOS|OPiOS|EdgiOS/.test(navigator.userAgent);
  if (isIOS && isSafari && !navigator.standalone) {
    var b = ensureBanner();
    instructions.innerHTML = 'Tap <strong>Share</strong> <span style="font-size:1.1em;">&#9757;</span> then <strong>"Add to Home Screen"</strong>';
    installBtn.style.display = 'none';
    b.style.display = 'block';
  }
})();

function switchTab(tabId) {
    document.querySelectorAll('.study-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    const tab = document.querySelector(`.study-tab[data-tab="${tabId}"]`);
    if (tab) tab.classList.add('active');
    const content = document.getElementById('tab-' + tabId);
    if (content) content.classList.add('active');
}

function toggleSidebar() {
    document.querySelector('.left-sidebar').classList.toggle('open');
    document.querySelector('.sidebar-overlay').classList.toggle('show');
}

/* Translation colors — match homepage Translation Guide */
var TRANSLATION_COLORS = {
    'ESV': '#8b3a2a',
    'KJV': '#4a5a8a',
    'ASV': '#7a5c2e',
    'NET': '#5c3d6e',
    'WEB': '#2c6b4f'
};

function switchTranslation(trans) {
    document.querySelectorAll('.translation-block').forEach(b => b.classList.remove('active'));
    const block = document.querySelector(`.translation-block[data-translation="${trans}"]`);
    if (block) block.classList.add('active');

    // Apply translation color to the active block
    var container = document.querySelector('.scripture-container');
    if (container) {
        container.style.color = TRANSLATION_COLORS[trans] || '#3d2b1f';
    }

    // Save preference to localStorage
    try { localStorage.setItem('preferredTranslation', trans); } catch(e) {}

    // Load ESV from API if needed
    if (trans === 'ESV') {
        loadESVText();
    }
}

/* Fetch ESV text via Cloudflare Worker proxy and inject into the ESV translation block */
function loadESVText() {
    var esvBlock = document.querySelector('.translation-block[data-translation="ESV"]');
    if (!esvBlock) return;

    // Already loaded
    if (esvBlock.dataset.loaded === 'true') return;

    var passage = esvBlock.dataset.passage;
    if (!passage) return;

    fetch(ESV_PROXY_URL + '/?q=' + encodeURIComponent(passage))
    .then(function(response) {
        if (!response.ok) throw new Error('ESV proxy error: ' + response.status);
        return response.json();
    })
    .then(function(data) {
        if (data.passages && data.passages.length > 0) {
            esvBlock.innerHTML = data.passages[0];
            esvBlock.dataset.loaded = 'true';
        } else {
            esvBlock.innerHTML = '<p class="verse" style="color:var(--text-muted);font-style:italic;">ESV text could not be loaded for this passage.</p>';
        }
    })
    .catch(function(err) {
        console.error('ESV fetch failed:', err);
        esvBlock.innerHTML = '<p class="verse" style="color:var(--text-muted);font-style:italic;">Unable to load ESV text. Please try again later.</p>';
    });
}

// Navigation: book/chapter selector
function navigateTo(book, chapter) {
    const slug = book.toLowerCase().replace(/\s+/g, '');
    window.location.href = `${slug}${chapter}.html`;
}

// Initialize tab clicks
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.study-tab').forEach(tab => {
        tab.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });

    // Prevent touch-drag on the tab bar (mobile fix)
    var tabBar = document.querySelector('.study-tabs');
    if (tabBar) {
        tabBar.addEventListener('touchmove', function(e) {
            e.preventDefault();
        }, { passive: false });
    }

    // Book select navigation
    const bookSelect = document.querySelector('.nav-book-select');
    const chapterSelect = document.querySelector('.nav-chapter-select');
    if (bookSelect && chapterSelect) {
        const navBtn = document.querySelector('.nav-go-btn');
        if (navBtn) {
            navBtn.addEventListener('click', function() {
                navigateTo(bookSelect.value, chapterSelect.value);
            });
        }
    }

    // Restore saved translation preference or default to ESV
    var savedTrans = null;
    try { savedTrans = localStorage.getItem('preferredTranslation'); } catch(e) {}
    if (savedTrans && TRANSLATION_COLORS[savedTrans]) {
        switchTranslation(savedTrans);
        // Update the dropdown to match
        var transSelect = document.querySelector('.nav-translation');
        if (transSelect) transSelect.value = savedTrans;
    } else {
        // Auto-load ESV text on page load (ESV is default translation)
        loadESVText();
        // Set default translation color (ESV)
        var container = document.querySelector('.scripture-container');
        if (container) {
            container.style.color = TRANSLATION_COLORS['ESV'];
        }
    }
});

function updateChapters() {
    var bookSelect = document.getElementById('bookSelect');
    var chapterSelect = document.getElementById('chapterSelect');
    var chapters = bookSelect.options[bookSelect.selectedIndex].dataset.chapters;
    chapterSelect.innerHTML = '';
    for (var i = 1; i <= parseInt(chapters); i++) {
        var opt = document.createElement('option');
        opt.value = i;
        opt.textContent = 'Ch ' + i;
        chapterSelect.appendChild(opt);
    }
}

function goToChapter() {
    var book = document.getElementById('bookSelect').value;
    var chapter = document.getElementById('chapterSelect').value;
    window.location.href = book + chapter + '.html';
}

/* ===== Extra videos overlay (New River channel only) =====
   Looks for newriver-videos.json, a file that exists ONLY in the New River
   deployment (keyed by page filename, e.g. "1kings1.html"). It never exists
   on the main site, so this fetch 404s there and the block below is a silent
   no-op — that's what keeps New River's channel videos from ever appearing
   on bible.macdwellings.com without needing a separate copy of this file. */
(function() {
    var tabVideos = document.getElementById('tab-videos');
    if (!tabVideos) return;
    var page = window.location.pathname.split('/').pop() || 'index.html';

    function escapeHtml(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    fetch('newriver-videos.json', { cache: 'no-store' })
        .then(function(r) { return r.ok ? r.json() : null; })
        .then(function(data) {
            var entries = data && data[page];
            if (!entries || !entries.length) return;
            entries.forEach(function(v) {
                var card = document.createElement('div');
                card.className = 'yt-facade';
                card.style.cssText = "position:relative;cursor:pointer;border-radius:10px;overflow:hidden;border:1px solid var(--border-light);aspect-ratio:16/9;background:#000 url('https://img.youtube.com/vi/" + v.id + "/hqdefault.jpg') center/cover;";
                card.setAttribute('onclick', "loadYT(this,'" + v.id + "')");
                card.innerHTML = '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.3);"><div style="width:60px;height:42px;background:#c0392b;border-radius:10px;display:flex;align-items:center;justify-content:center;"><div style="width:0;height:0;border-left:18px solid #fff;border-top:10px solid transparent;border-bottom:10px solid transparent;margin-left:4px;"></div></div></div><p style="position:absolute;bottom:0;left:0;right:0;padding:8px 12px;margin:0;background:rgba(0,0,0,0.7);color:#fff;font-size:0.78rem;font-weight:600;">'
                    + escapeHtml(v.title) + '<br><span class="yt-src" style="font-size:0.64rem;font-weight:400;opacity:0.75;">' + escapeHtml(v.source || 'New River Church') + '</span></p>';
                tabVideos.appendChild(card);
            });
            var h3 = tabVideos.querySelector('h3');
            if (h3) {
                var count = tabVideos.querySelectorAll('.yt-facade').length;
                h3.innerHTML = 'Videos (' + count + ') <span style="font-size:0.75rem;color:#8a7e74;font-weight:400;"> — tap thumbnails to play</span>';
            }
        })
        .catch(function() { /* no overlay file on this deployment — expected */ });
})();
