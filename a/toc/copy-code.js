/**
 * copy-code.js - Copy to Clipboard for Code Snippets
 * 
 * For The Building Coder Archive
 * Adds copy buttons to all <pre> code blocks
 */

(function() {
  'use strict';

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCopyButtons);
  } else {
    initCopyButtons();
  }

  function initCopyButtons() {
    // Find all <pre> elements
    const codeBlocks = document.querySelectorAll('pre');
    
    codeBlocks.forEach(function(pre) {
      // Skip if already has a copy button
      if (pre.querySelector('.tbc-copy-btn')) return;
      
      // Create wrapper div for positioning
      const wrapper = document.createElement('div');
      wrapper.className = 'tbc-code-wrapper';
      
      // Insert wrapper before pre, then move pre into wrapper
      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);
      
      // Create copy button
      const copyBtn = document.createElement('button');
      copyBtn.className = 'tbc-copy-btn';
      copyBtn.setAttribute('aria-label', 'Copy code to clipboard');
      copyBtn.setAttribute('title', 'Copy to clipboard');
      copyBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>';
      
      // Add click handler
      copyBtn.addEventListener('click', function() {
        copyToClipboard(pre, copyBtn);
      });
      
      // Insert button into wrapper
      wrapper.appendChild(copyBtn);
    });
  }

  function copyToClipboard(pre, btn) {
    // Get text content, stripping any HTML
    const text = pre.textContent || pre.innerText;
    
    // Use modern clipboard API if available
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function() {
        showCopiedFeedback(btn);
      }).catch(function(err) {
        console.error('Failed to copy:', err);
        fallbackCopy(text, btn);
      });
    } else {
      fallbackCopy(text, btn);
    }
  }

  function fallbackCopy(text, btn) {
    // Fallback for older browsers
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    textarea.style.top = '0';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    
    try {
      document.execCommand('copy');
      showCopiedFeedback(btn);
    } catch (err) {
      console.error('Fallback copy failed:', err);
    }
    
    document.body.removeChild(textarea);
  }

  function showCopiedFeedback(btn) {
    // Change icon to checkmark
    const originalHTML = btn.innerHTML;
    btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
    btn.classList.add('tbc-copy-success');
    
    // Reset after delay
    setTimeout(function() {
      btn.innerHTML = originalHTML;
      btn.classList.remove('tbc-copy-success');
    }, 2000);
  }
})();
