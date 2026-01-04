/**
 * toc-sidebar.js - Wiki-Style TOC Sidebar
 * 
 * For The Building Coder Archive
 * Author: GitHub Copilot
 * Date: January 2, 2026
 * 
 * Features:
 * - Dynamic sidebar generation from JSON data
 * - Topic-based navigation with collapsible groups
 * - Real-time search with highlighting
 * - Drag-to-resize functionality
 * - Current page detection and highlighting
 * - Mobile hamburger menu
 * - State persistence in localStorage
 */

(function() {
  'use strict';

  // ================================
  // Configuration
  // ================================
  const CONFIG = {
    tocDataUrl: 'toc/toc-data.json',
    defaultWidth: 280,
    minWidth: 180,
    maxWidth: 500,
    searchDebounce: 150,
    storageKeys: {
      width: 'tbc-sidebar-width',
      expanded: 'tbc-expanded-topics',
      scroll: 'tbc-sidebar-scroll'
    }
  };

  // ================================
  // State
  // ================================
  const state = {
    tocData: null,
    currentPage: null,
    expandedTopics: new Set(),
    isResizing: false,
    isMobileOpen: false,
    searchQuery: ''
  };

  // ================================
  // Utility Functions
  // ================================
  function debounce(func, wait) {
    let timeout;
    return function(...args) {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function getCurrentPageFile() {
    const path = window.location.pathname;
    const file = path.split('/').pop();
    return file || 'index.html';
  }

  // ================================
  // Data Loading
  // ================================
  async function loadTocData() {
    // Try to load from cache first
    const cached = localStorage.getItem('tbc-toc-data');
    const cacheTime = localStorage.getItem('tbc-toc-cache-time');
    const ONE_HOUR = 60 * 60 * 1000;
    
    if (cached && cacheTime && (Date.now() - parseInt(cacheTime)) < ONE_HOUR) {
      try {
        return JSON.parse(cached);
      } catch (e) {
        console.warn('Failed to parse cached TOC data');
      }
    }
    
    // Determine the base path for the JSON file
    const currentPath = window.location.pathname;
    let basePath = '';
    
    // If we're in the a/ directory viewing a post
    if (currentPath.includes('/a/') && !currentPath.endsWith('/a/') && !currentPath.endsWith('/a/index.html')) {
      basePath = '';  // toc/ is in same directory
    } else if (currentPath.endsWith('/a/') || currentPath.endsWith('/a/index.html')) {
      basePath = '';  // we're in a/
    } else {
      basePath = 'a/';  // we're at root
    }
    
    const url = basePath + CONFIG.tocDataUrl;
    
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      
      // Cache the data
      try {
        localStorage.setItem('tbc-toc-data', JSON.stringify(data));
        localStorage.setItem('tbc-toc-cache-time', Date.now().toString());
      } catch (e) {
        console.warn('Failed to cache TOC data');
      }
      
      return data;
    } catch (error) {
      console.error('Failed to load TOC data:', error);
      throw error;
    }
  }

  // ================================
  // State Persistence
  // ================================
  function loadPersistedState() {
    // Load expanded topics
    try {
      const expanded = localStorage.getItem(CONFIG.storageKeys.expanded);
      if (expanded) {
        state.expandedTopics = new Set(JSON.parse(expanded));
      }
    } catch (e) {
      console.warn('Failed to load expanded topics');
    }
    
    // Load sidebar width
    const savedWidth = localStorage.getItem(CONFIG.storageKeys.width);
    if (savedWidth) {
      return parseInt(savedWidth) || CONFIG.defaultWidth;
    }
    return CONFIG.defaultWidth;
  }

  function saveExpandedTopics() {
    try {
      localStorage.setItem(
        CONFIG.storageKeys.expanded, 
        JSON.stringify([...state.expandedTopics])
      );
    } catch (e) {
      console.warn('Failed to save expanded topics');
    }
  }

  function saveSidebarWidth(width) {
    try {
      localStorage.setItem(CONFIG.storageKeys.width, width.toString());
    } catch (e) {
      console.warn('Failed to save sidebar width');
    }
  }

  function saveScrollPosition() {
    const container = document.getElementById('tbc-topics-container');
    if (container) {
      try {
        localStorage.setItem(CONFIG.storageKeys.scroll, container.scrollTop.toString());
      } catch (e) {}
    }
  }

  function restoreScrollPosition() {
    const container = document.getElementById('tbc-topics-container');
    const saved = localStorage.getItem(CONFIG.storageKeys.scroll);
    if (container && saved) {
      container.scrollTop = parseInt(saved) || 0;
    }
  }

  // ================================
  // Sidebar HTML Generation
  // ================================
  function generateSidebarHTML() {
    return `
      <div id="tbc-resize-handle" title="Drag to resize"></div>
      <button id="tbc-sidebar-close" aria-label="Close sidebar">×</button>
      
      <div id="tbc-sidebar-header">
        <a href="index.html" title="The Building Coder Archive">
          <span class="tbc-logo">🏗️</span>
          <span>The Building Coder</span>
        </a>
      </div>
      
      <div id="tbc-search-container">
        <div class="tbc-search-wrapper">
          <span class="tbc-search-icon">🔍</span>
          <input type="text" 
                 id="tbc-search-input" 
                 placeholder="Search posts..." 
                 autocomplete="off"
                 aria-label="Search posts">
          <button id="tbc-search-clear" class="hidden" aria-label="Clear search">×</button>
        </div>
        <div id="tbc-search-results"></div>
      </div>
      
      <nav id="tbc-nav-links" aria-label="Main navigation">
        <!-- Populated dynamically -->
      </nav>
      
      <div id="tbc-topics-container" aria-label="Topics navigation">
        <div class="tbc-loading-spinner"></div>
      </div>
      
      <div class="tbc-shortcut-hint">
        Press <kbd>/</kbd> to search
      </div>
    `;
  }

  function generateNavLinksHTML(navigation) {
    if (!navigation || !navigation.length) return '';
    
    return navigation.map(link => {
      const isActive = state.currentPage === 'index.html' && 
                       window.location.hash === link.href.replace('index.html', '');
      return `<a href="${escapeHtml(link.href)}"${isActive ? ' class="active"' : ''}>${escapeHtml(link.label)}</a>`;
    }).join('');
  }

  function generateTopicsHTML(topics) {
    if (!topics || !topics.length) {
      return '<div class="tbc-error">No topics found</div>';
    }
    
    return topics.map(topic => generateTopicHTML(topic)).join('');
  }

  function generateArchiveHTML(archive) {
    if (!archive || !archive.length) {
      return '';
    }
    
    // Filter out invalid years (like typos e.g., 1020 instead of 2020)
    const validArchive = archive.filter(year => {
      const yearNum = parseInt(year.title);
      return yearNum >= 2000 && yearNum <= 2100;
    });
    
    if (!validArchive.length) return '';
    
    const archiveTopics = validArchive.map(year => {
      const isExpanded = state.expandedTopics.has(year.id);
      const expandedClass = isExpanded ? ' expanded' : '';
      
      const postsHTML = year.posts.map(post => {
        const isCurrent = isCurrentPost(post.file);
        const currentClass = isCurrent ? ' current' : '';
        return `<a href="${escapeHtml(post.file)}" class="tbc-post-link${currentClass}" title="${escapeHtml(post.title)}">${escapeHtml(post.title)}</a>`;
      }).join('');
      
      return `
        <div class="tbc-topic tbc-archive-year${expandedClass}" data-topic-id="${escapeHtml(year.id)}">
          <div class="tbc-topic-header" tabindex="0" role="button" aria-expanded="${isExpanded}">
            <span class="tbc-topic-toggle">▶</span>
            <span class="tbc-topic-title">
              <span class="tbc-topic-id">📅</span>
              ${escapeHtml(year.title)}
            </span>
            <span class="tbc-topic-count">(${year.posts.length})</span>
          </div>
          <div class="tbc-topic-posts">
            ${postsHTML}
          </div>
        </div>
      `;
    }).join('');
    
    return `
      <div class="tbc-archive-section">
        <div class="tbc-section-header">
          <span class="tbc-section-icon">📚</span>
          <span class="tbc-section-title">Chronological Archive</span>
          <span class="tbc-section-count">(${validArchive.reduce((sum, y) => sum + y.posts.length, 0)} posts)</span>
          <button class="tbc-toggle-all" title="Toggle all years">±</button>
        </div>
        ${archiveTopics}
      </div>
    `;
  }

  function generateTopicHTML(topic, isSubTopic = false) {
    const isExpanded = state.expandedTopics.has(topic.id);
    const postCount = topic.posts ? topic.posts.length : 0;
    const hasSubTopics = topic.subTopics && topic.subTopics.length > 0;
    const totalCount = postCount + (hasSubTopics ? topic.subTopics.reduce((sum, st) => sum + (st.posts?.length || 0), 0) : 0);
    
    const topicClass = isSubTopic ? 'tbc-topic tbc-subtopic' : 'tbc-topic';
    const expandedClass = isExpanded ? ' expanded' : '';
    
    let postsHTML = '';
    if (topic.posts && topic.posts.length) {
      postsHTML = topic.posts.map(post => {
        const isCurrent = isCurrentPost(post.file);
        const currentClass = isCurrent ? ' current' : '';
        return `<a href="${escapeHtml(post.file)}" class="tbc-post-link${currentClass}" title="${escapeHtml(post.title)}">${escapeHtml(post.title)}</a>`;
      }).join('');
    }
    
    let subTopicsHTML = '';
    if (hasSubTopics) {
      subTopicsHTML = topic.subTopics.map(st => generateTopicHTML(st, true)).join('');
    }
    
    return `
      <div class="${topicClass}${expandedClass}" data-topic-id="${escapeHtml(topic.id)}">
        <div class="tbc-topic-header" tabindex="0" role="button" aria-expanded="${isExpanded}">
          <span class="tbc-topic-toggle">▶</span>
          <span class="tbc-topic-title">
            <span class="tbc-topic-id">${escapeHtml(topic.id)}</span>
            ${escapeHtml(topic.title)}
          </span>
          <span class="tbc-topic-count">(${totalCount})</span>
        </div>
        <div class="tbc-topic-posts">
          ${postsHTML}
          ${subTopicsHTML}
        </div>
      </div>
    `;
  }

  function isCurrentPost(postFile) {
    if (!postFile || !state.currentPage) return false;
    
    // Handle URLs with anchors
    const postFileBase = postFile.split('#')[0];
    const currentBase = state.currentPage.split('#')[0];
    
    return postFileBase === currentBase || 
           postFileBase === state.currentPage ||
           postFile === state.currentPage;
  }

  // ================================
  // Sidebar Initialization
  // ================================
  async function initSidebar() {
    // Check if sidebar already exists
    if (document.getElementById('tbc-sidebar')) {
      return;
    }
    
    // Detect current page
    state.currentPage = getCurrentPageFile();
    
    // Load persisted state
    const savedWidth = loadPersistedState();
    
    // Create sidebar container
    const sidebar = document.createElement('div');
    sidebar.id = 'tbc-sidebar';
    sidebar.className = 'loading';
    sidebar.innerHTML = generateSidebarHTML();
    
    // Create mobile toggle button
    const mobileToggle = document.createElement('button');
    mobileToggle.id = 'tbc-mobile-toggle';
    mobileToggle.innerHTML = '☰';
    mobileToggle.setAttribute('aria-label', 'Open navigation');
    
    // Create overlay for mobile
    const overlay = document.createElement('div');
    overlay.id = 'tbc-overlay';
    
    // Wrap existing content
    const body = document.body;
    const existingContent = Array.from(body.childNodes);
    
    const contentWrapper = document.createElement('div');
    contentWrapper.id = 'tbc-content';
    
    existingContent.forEach(node => {
      if (node.id !== 'tbc-sidebar' && 
          node.id !== 'tbc-mobile-toggle' && 
          node.id !== 'tbc-overlay') {
        contentWrapper.appendChild(node);
      }
    });
    
    // Add elements to body
    body.innerHTML = '';
    body.appendChild(sidebar);
    body.appendChild(overlay);
    body.appendChild(mobileToggle);
    body.appendChild(contentWrapper);
    body.classList.add('tbc-has-sidebar');
    
    // Set initial width
    sidebar.style.width = savedWidth + 'px';
    contentWrapper.style.marginLeft = savedWidth + 'px';
    
    // Load TOC data
    try {
      state.tocData = await loadTocData();
      renderSidebar();
      sidebar.classList.remove('loading');
    } catch (error) {
      renderError(error);
      sidebar.classList.remove('loading');
    }
    
    // Initialize interactions
    initResizeHandle();
    initSearch();
    initTopicToggles();
    initMobileMenu();
    initKeyboardShortcuts();
    
    // Expand topic containing current page
    expandCurrentTopic();
    
    // Restore scroll position
    setTimeout(restoreScrollPosition, 100);
    
    // Save scroll position on scroll
    const topicsContainer = document.getElementById('tbc-topics-container');
    if (topicsContainer) {
      topicsContainer.addEventListener('scroll', debounce(saveScrollPosition, 500));
    }
  }

  function renderSidebar() {
    if (!state.tocData) return;
    
    // Render navigation links
    const navLinksContainer = document.getElementById('tbc-nav-links');
    if (navLinksContainer) {
      navLinksContainer.innerHTML = generateNavLinksHTML(state.tocData.navigation);
    }
    
    // Render topics and archive
    const topicsContainer = document.getElementById('tbc-topics-container');
    if (topicsContainer) {
      let html = '';
      
      // Section header for topics
      html += `
        <div class="tbc-topics-section">
          <div class="tbc-section-header">
            <span class="tbc-section-icon">📑</span>
            <span class="tbc-section-title">Topic Groups</span>
            <span class="tbc-section-count">(${state.tocData.totalPostLinks || 0} posts)</span>
            <button class="tbc-toggle-all" title="Toggle all topics">±</button>
          </div>
          ${generateTopicsHTML(state.tocData.topics)}
        </div>
      `;
      
      // Archive section
      if (state.tocData.archive && state.tocData.archive.length) {
        html += generateArchiveHTML(state.tocData.archive);
      }
      
      topicsContainer.innerHTML = html;
    }
    
    // Re-init topic toggles after rendering
    initTopicToggles();
  }

  function renderError(error) {
    const topicsContainer = document.getElementById('tbc-topics-container');
    if (topicsContainer) {
      topicsContainer.innerHTML = `
        <div class="tbc-error">
          <div class="tbc-error-icon">⚠️</div>
          <div class="tbc-error-message">Failed to load table of contents</div>
          <button class="tbc-retry-btn" onclick="location.reload()">Retry</button>
        </div>
      `;
    }
  }

  // ================================
  // Resize Handle
  // ================================
  function initResizeHandle() {
    const handle = document.getElementById('tbc-resize-handle');
    const sidebar = document.getElementById('tbc-sidebar');
    const content = document.getElementById('tbc-content');
    
    if (!handle || !sidebar || !content) return;
    
    let startX, startWidth;
    
    function onMouseDown(e) {
      state.isResizing = true;
      startX = e.clientX;
      startWidth = sidebar.offsetWidth;
      
      handle.classList.add('dragging');
      document.body.classList.add('tbc-resizing');
      
      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
      
      e.preventDefault();
    }
    
    function onMouseMove(e) {
      if (!state.isResizing) return;
      
      const diff = e.clientX - startX;
      let newWidth = startWidth + diff;
      
      // Enforce constraints
      newWidth = Math.max(CONFIG.minWidth, Math.min(CONFIG.maxWidth, newWidth));
      
      sidebar.style.width = newWidth + 'px';
      content.style.marginLeft = newWidth + 'px';
      
      // Update CSS variable
      document.documentElement.style.setProperty('--tbc-sidebar-width', newWidth + 'px');
    }
    
    function onMouseUp() {
      if (!state.isResizing) return;
      
      state.isResizing = false;
      handle.classList.remove('dragging');
      document.body.classList.remove('tbc-resizing');
      
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
      
      // Save width
      saveSidebarWidth(sidebar.offsetWidth);
    }
    
    handle.addEventListener('mousedown', onMouseDown);
    
    // Double-click to reset
    handle.addEventListener('dblclick', () => {
      sidebar.style.width = CONFIG.defaultWidth + 'px';
      content.style.marginLeft = CONFIG.defaultWidth + 'px';
      document.documentElement.style.setProperty('--tbc-sidebar-width', CONFIG.defaultWidth + 'px');
      saveSidebarWidth(CONFIG.defaultWidth);
    });
    
    // Touch support
    handle.addEventListener('touchstart', (e) => {
      state.isResizing = true;
      startX = e.touches[0].clientX;
      startWidth = sidebar.offsetWidth;
      handle.classList.add('dragging');
      e.preventDefault();
    });
    
    document.addEventListener('touchmove', (e) => {
      if (!state.isResizing) return;
      
      const touch = e.touches[0];
      const diff = touch.clientX - startX;
      let newWidth = startWidth + diff;
      newWidth = Math.max(CONFIG.minWidth, Math.min(CONFIG.maxWidth, newWidth));
      
      sidebar.style.width = newWidth + 'px';
      content.style.marginLeft = newWidth + 'px';
    });
    
    document.addEventListener('touchend', () => {
      if (state.isResizing) {
        state.isResizing = false;
        handle.classList.remove('dragging');
        saveSidebarWidth(sidebar.offsetWidth);
      }
    });
  }

  // ================================
  // Search
  // ================================
  function initSearch() {
    const input = document.getElementById('tbc-search-input');
    const clearBtn = document.getElementById('tbc-search-clear');
    
    if (!input) return;
    
    const performSearchDebounced = debounce(performSearch, CONFIG.searchDebounce);
    
    input.addEventListener('input', () => {
      state.searchQuery = input.value;
      clearBtn.classList.toggle('hidden', !input.value);
      performSearchDebounced(input.value);
    });
    
    clearBtn.addEventListener('click', () => {
      input.value = '';
      state.searchQuery = '';
      clearBtn.classList.add('hidden');
      resetSearch();
      input.focus();
    });
  }

  function performSearch(query) {
    const resultsDiv = document.getElementById('tbc-search-results');
    query = query.toLowerCase().trim();
    
    if (!query) {
      resetSearch();
      return;
    }
    
    const topics = document.querySelectorAll('.tbc-topic');
    const posts = document.querySelectorAll('.tbc-post-link');
    let matchCount = 0;
    
    // Search posts
    posts.forEach(post => {
      const title = post.textContent.toLowerCase();
      const matches = title.includes(query);
      
      post.classList.toggle('tbc-search-no-match', !matches);
      
      if (matches) {
        matchCount++;
        highlightText(post, query);
        
        // Expand parent topic
        const topic = post.closest('.tbc-topic');
        if (topic) {
          topic.classList.add('expanded');
          state.expandedTopics.add(topic.dataset.topicId);
        }
      } else {
        removeHighlight(post);
      }
    });
    
    // Search and show/hide topics
    topics.forEach(topic => {
      const topicTitle = topic.querySelector('.tbc-topic-title');
      const topicTitleText = topicTitle ? topicTitle.textContent.toLowerCase() : '';
      const topicMatches = topicTitleText.includes(query);
      const hasVisiblePosts = topic.querySelector('.tbc-post-link:not(.tbc-search-no-match)');
      
      if (topicMatches) {
        topic.classList.remove('tbc-search-no-match');
        topic.classList.add('expanded');
        state.expandedTopics.add(topic.dataset.topicId);
        
        // Show all posts in matching topic
        topic.querySelectorAll('.tbc-post-link').forEach(p => {
          p.classList.remove('tbc-search-no-match');
          matchCount++;
        });
        
        if (topicTitle) highlightText(topicTitle, query);
      } else {
        topic.classList.toggle('tbc-search-no-match', !hasVisiblePosts);
        if (topicTitle) removeHighlight(topicTitle);
      }
    });
    
    // Update results count
    if (resultsDiv) {
      if (matchCount === 0) {
        resultsDiv.textContent = 'No posts found';
        resultsDiv.classList.add('no-results');
      } else {
        resultsDiv.textContent = `${matchCount} result${matchCount === 1 ? '' : 's'}`;
        resultsDiv.classList.remove('no-results');
      }
    }
  }

  function resetSearch() {
    const resultsDiv = document.getElementById('tbc-search-results');
    const topics = document.querySelectorAll('.tbc-topic');
    const posts = document.querySelectorAll('.tbc-post-link');
    
    posts.forEach(post => {
      post.classList.remove('tbc-search-no-match');
      removeHighlight(post);
    });
    
    topics.forEach(topic => {
      topic.classList.remove('tbc-search-no-match');
      const topicTitle = topic.querySelector('.tbc-topic-title');
      if (topicTitle) removeHighlight(topicTitle);
    });
    
    if (resultsDiv) {
      resultsDiv.textContent = '';
      resultsDiv.classList.remove('no-results');
    }
  }

  function highlightText(element, query) {
    const originalText = element.getAttribute('data-original-text') || element.textContent;
    element.setAttribute('data-original-text', originalText);
    
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    element.innerHTML = escapeHtml(originalText).replace(
      regex, 
      '<span class="tbc-search-highlight">$1</span>'
    );
  }

  function removeHighlight(element) {
    const originalText = element.getAttribute('data-original-text');
    if (originalText) {
      element.textContent = originalText;
    }
  }

  // ================================
  // Topic Toggles
  // ================================
  function initTopicToggles() {
    const topicHeaders = document.querySelectorAll('.tbc-topic-header');
    
    topicHeaders.forEach(header => {
      // Remove existing listeners
      header.replaceWith(header.cloneNode(true));
    });
    
    // Re-query and add listeners
    document.querySelectorAll('.tbc-topic-header').forEach(header => {
      header.addEventListener('click', (e) => {
        const topic = header.closest('.tbc-topic');
        if (topic) {
          toggleTopic(topic);
        }
      });
      
      header.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          const topic = header.closest('.tbc-topic');
          if (topic) {
            toggleTopic(topic);
          }
        }
      });
    });
    
    // Toggle-all buttons
    document.querySelectorAll('.tbc-toggle-all').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const section = btn.closest('.tbc-topics-section, .tbc-archive-section');
        if (section) {
          toggleAllInSection(section);
        }
      });
    });
  }

  function toggleAllInSection(section) {
    const topics = section.querySelectorAll('.tbc-topic');
    const expandedCount = section.querySelectorAll('.tbc-topic.expanded').length;
    const shouldExpand = expandedCount < topics.length / 2;
    
    topics.forEach(topic => {
      const topicId = topic.dataset.topicId;
      if (shouldExpand) {
        topic.classList.add('expanded');
        if (topicId) state.expandedTopics.add(topicId);
      } else {
        topic.classList.remove('expanded');
        if (topicId) state.expandedTopics.delete(topicId);
      }
      
      const header = topic.querySelector('.tbc-topic-header');
      if (header) {
        header.setAttribute('aria-expanded', shouldExpand);
      }
    });
    
    saveExpandedTopics();
  }

  function toggleTopic(topicElement) {
    const topicId = topicElement.dataset.topicId;
    const isExpanded = topicElement.classList.toggle('expanded');
    
    const header = topicElement.querySelector('.tbc-topic-header');
    if (header) {
      header.setAttribute('aria-expanded', isExpanded);
    }
    
    if (isExpanded) {
      state.expandedTopics.add(topicId);
    } else {
      state.expandedTopics.delete(topicId);
    }
    
    saveExpandedTopics();
  }

  function expandCurrentTopic() {
    if (!state.currentPage) return;
    
    // Find the post link that matches current page
    const currentLink = document.querySelector('.tbc-post-link.current');
    if (currentLink) {
      // Expand all parent topics
      let parent = currentLink.closest('.tbc-topic');
      while (parent) {
        parent.classList.add('expanded');
        const topicId = parent.dataset.topicId;
        if (topicId) {
          state.expandedTopics.add(topicId);
        }
        parent = parent.parentElement.closest('.tbc-topic');
      }
      
      // Scroll to current link
      setTimeout(() => {
        currentLink.scrollIntoView({ block: 'center', behavior: 'smooth' });
      }, 200);
    }
  }

  // ================================
  // Mobile Menu
  // ================================
  function initMobileMenu() {
    const toggle = document.getElementById('tbc-mobile-toggle');
    const sidebar = document.getElementById('tbc-sidebar');
    const overlay = document.getElementById('tbc-overlay');
    const closeBtn = document.getElementById('tbc-sidebar-close');
    
    if (!toggle || !sidebar) return;
    
    function openSidebar() {
      state.isMobileOpen = true;
      sidebar.classList.add('open');
      if (overlay) overlay.classList.add('active');
      toggle.innerHTML = '×';
      toggle.setAttribute('aria-label', 'Close navigation');
    }
    
    function closeSidebar() {
      state.isMobileOpen = false;
      sidebar.classList.remove('open');
      if (overlay) overlay.classList.remove('active');
      toggle.innerHTML = '☰';
      toggle.setAttribute('aria-label', 'Open navigation');
    }
    
    toggle.addEventListener('click', () => {
      if (state.isMobileOpen) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });
    
    if (overlay) {
      overlay.addEventListener('click', closeSidebar);
    }
    
    if (closeBtn) {
      closeBtn.addEventListener('click', closeSidebar);
    }
    
    // Close on navigation
    sidebar.addEventListener('click', (e) => {
      if (e.target.classList.contains('tbc-post-link') || 
          e.target.closest('#tbc-nav-links a')) {
        closeSidebar();
      }
    });
  }

  // ================================
  // Keyboard Shortcuts
  // ================================
  function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      const input = document.getElementById('tbc-search-input');
      
      // Press '/' to focus search (like GitHub)
      if (e.key === '/' && document.activeElement !== input) {
        e.preventDefault();
        if (input) input.focus();
      }
      
      // Press Escape to clear and blur
      if (e.key === 'Escape') {
        if (document.activeElement === input) {
          input.value = '';
          state.searchQuery = '';
          resetSearch();
          input.blur();
          
          const clearBtn = document.getElementById('tbc-search-clear');
          if (clearBtn) clearBtn.classList.add('hidden');
        }
        
        // Close mobile menu
        if (state.isMobileOpen) {
          const sidebar = document.getElementById('tbc-sidebar');
          const overlay = document.getElementById('tbc-overlay');
          const toggle = document.getElementById('tbc-mobile-toggle');
          
          if (sidebar) sidebar.classList.remove('open');
          if (overlay) overlay.classList.remove('active');
          if (toggle) {
            toggle.innerHTML = '☰';
            toggle.setAttribute('aria-label', 'Open navigation');
          }
          state.isMobileOpen = false;
        }
      }
    });
  }

  // ================================
  // Initialize on DOM Ready
  // ================================
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSidebar);
  } else {
    initSidebar();
  }

})();
