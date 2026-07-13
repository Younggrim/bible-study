/* Bible Study Site — Shared JavaScript */

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

function switchTranslation(trans) {
    document.querySelectorAll('.translation-block').forEach(b => b.classList.remove('active'));
    const block = document.querySelector(`.translation-block[data-translation="${trans}"]`);
    if (block) block.classList.add('active');
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

function toggleTransInfo() {
    document.getElementById('transPopup').classList.toggle('show');
}


/* Translation Comparison — Filter Logic */
function filterTranslations() {
    // Get all checked translations
    var checkboxes = document.querySelectorAll('.trans-filter input[type="checkbox"]');
    var selected = [];
    checkboxes.forEach(function(cb) {
        if (cb.checked) selected.push(cb.value);
    });

    // Get all translation entry cards
    var entries = document.querySelectorAll('.trans-entry');
    entries.forEach(function(entry) {
        var entryTrans = entry.getAttribute('data-translations').split(' ');

        if (selected.length === 0) {
            // Nothing selected — hide all
            entry.classList.add('hidden');
        } else if (entryTrans[0] === 'general') {
            // Entries without specific translations always show
            entry.classList.remove('hidden');
        } else {
            // Check if any of the entry's translations are in the selected list
            var hasMatch = entryTrans.some(function(t) {
                return selected.indexOf(t) !== -1;
            });
            if (hasMatch) {
                entry.classList.remove('hidden');
            } else {
                entry.classList.add('hidden');
            }
        }
    });

    // Dim/hide individual translation labels that are unchecked
    var allTrans = ['KJV', 'ESV', 'ASV', 'NET', 'WEB'];
    allTrans.forEach(function(t) {
        var cls = 'trans-' + t.toLowerCase();
        var labels = document.querySelectorAll('.trans-label.' + cls);
        var isSelected = selected.indexOf(t) !== -1;
        labels.forEach(function(label) {
            if (isSelected) {
                label.classList.remove('trans-deselected');
            } else {
                label.classList.add('trans-deselected');
            }
        });
    });
}
