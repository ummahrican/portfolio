/**
 * HTMS Runtime - Progressive HTML Streaming
 * 
 * Handles:
 * - Replacing placeholders with streamed content
 * - Error state management
 * - Retry functionality for recoverable errors
 * - Accessibility announcements
 */

(function() {
  'use strict';

  // Track failed chunks for retry
  const failedChunks = new Map();

  // Announce content updates to screen readers
  function announceUpdate(element) {
    element.setAttribute('aria-live', 'polite');
    element.setAttribute('aria-atomic', 'true');
  }

  // Find placeholder by UUID
  function findPlaceholder(uuid) {
    return document.querySelector(`[data-htms-uuid="${uuid}"]`);
  }

  // Handle successful chunk
  function handleSuccess(target, content) {
    target.innerHTML = content;
    target.removeAttribute('data-htms-uuid');
    target.classList.remove('htms-placeholder');
    target.classList.add('htms-loaded');
    announceUpdate(target);
  }

  // Handle failed chunk
  function handleError(target, uuid, errorType, recoverable) {
    target.classList.remove('htms-placeholder');
    target.classList.add('htms-error-state');
    target.setAttribute('data-htms-failed', 'true');
    target.setAttribute('aria-live', 'assertive');
    
    if (recoverable === 'true') {
      failedChunks.set(uuid, {
        target: target,
        originalContent: target.getAttribute('data-htms-error-fallback') || target.innerHTML
      });
    }
  }

  // Retry a failed chunk
  window.htmsRetry = async function(uuid) {
    const failed = failedChunks.get(uuid);
    if (!failed) {
      console.warn('HTMS: No failed chunk found for retry:', uuid);
      return;
    }

    const target = failed.target;
    target.innerHTML = '<span class="animate-pulse">Retrying...</span>';
    target.classList.remove('htms-error-state');
    target.classList.add('htms-retrying');

    try {
      // For now, just reload the page on retry
      // In production, implement a retry endpoint
      window.location.reload();
    } catch (e) {
      // Restore error state
      target.innerHTML = failed.originalContent;
      target.classList.remove('htms-retrying');
      target.classList.add('htms-error-state');
      console.error('HTMS retry failed:', e);
    }
  };

  // Custom element for streamed chunks
  class HtmsChunk extends HTMLElement {
    connectedCallback() {
      const uuid = this.getAttribute('uuid');
      const isError = this.getAttribute('data-error') === 'true';
      const errorType = this.getAttribute('data-error-type');
      const recoverable = this.getAttribute('data-recoverable');
      
      const target = findPlaceholder(uuid);
      
      if (!target) {
        console.warn(`HTMS: No placeholder found for uuid="${uuid}"`);
        this.remove();
        return;
      }

      if (isError) {
        // Update with error content
        target.innerHTML = this.innerHTML;
        handleError(target, uuid, errorType, recoverable);
      } else {
        // Update with success content
        handleSuccess(target, this.innerHTML);
      }

      // Remove the chunk element from DOM
      this.remove();
    }
  }

  // Register custom element
  if (!customElements.get('htms-chunk')) {
    customElements.define('htms-chunk', HtmsChunk);
  }

  // Expose for debugging
  window.HTMS = {
    failedChunks,
    retry: window.htmsRetry
  };

  // Log when ready
  console.log('HTMS runtime loaded');
})();