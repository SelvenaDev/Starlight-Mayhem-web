(() => {
  'use strict';

  const keyMap = {
    ArrowLeft: { key: 'ArrowLeft', code: 'ArrowLeft', keyCode: 37 },
    ArrowUp: { key: 'ArrowUp', code: 'ArrowUp', keyCode: 38 },
    ArrowRight: { key: 'ArrowRight', code: 'ArrowRight', keyCode: 39 },
    ArrowDown: { key: 'ArrowDown', code: 'ArrowDown', keyCode: 40 },
    Enter: { key: 'Enter', code: 'Enter', keyCode: 13 },
    Escape: { key: 'Escape', code: 'Escape', keyCode: 27 },
  };
  const heldKeys = new Set();

  function dispatchKeyboardEvent(type, definition) {
    const event = new KeyboardEvent(type, {
      key: definition.key,
      code: definition.code,
      keyCode: definition.keyCode,
      which: definition.keyCode,
      bubbles: true,
      cancelable: true,
    });

    // Some mobile browsers ignore legacy keyCode constructor options; OpenFL reads keyCode.
    if (event.keyCode !== definition.keyCode) {
      try {
        Object.defineProperty(event, 'keyCode', { get: () => definition.keyCode });
        Object.defineProperty(event, 'which', { get: () => definition.keyCode });
      } catch (_) {
        // The standard key/code values remain available if a browser locks these properties.
      }
    }
    // Start at document so the keyboard event bubbles to both document and window
    // listeners used by OpenFL across desktop and mobile browsers.
    document.dispatchEvent(event);
  }

  function press(key) {
    const definition = keyMap[key];
    if (!definition || heldKeys.has(key)) return;
    heldKeys.add(key);
    dispatchKeyboardEvent('keydown', definition);
  }

  function release(key) {
    const definition = keyMap[key];
    if (!definition || !heldKeys.delete(key)) return;
    dispatchKeyboardEvent('keyup', definition);
  }

  function finishPress(button, key, event) {
    if (event) event.preventDefault();
    button.classList.remove('is-pressed');
    release(key);
  }

  document.querySelectorAll('#mobile-controls [data-key]').forEach((button) => {
    const key = button.dataset.key;

    if ('PointerEvent' in window) {
      button.addEventListener('pointerdown', (event) => {
        event.preventDefault();
        try {
          button.setPointerCapture(event.pointerId);
        } catch (_) {
          // Pointer capture is optional on older mobile browsers.
        }
        button.classList.add('is-pressed');
        press(key);
      });
      button.addEventListener('pointerup', (event) => finishPress(button, key, event));
      button.addEventListener('pointercancel', (event) => finishPress(button, key, event));
      button.addEventListener('lostpointercapture', (event) => finishPress(button, key, event));
    } else {
      button.addEventListener('touchstart', (event) => {
        event.preventDefault();
        button.classList.add('is-pressed');
        press(key);
      }, { passive: false });
      button.addEventListener('touchend', (event) => finishPress(button, key, event), { passive: false });
      button.addEventListener('touchcancel', (event) => finishPress(button, key, event), { passive: false });
    }

    button.addEventListener('contextmenu', (event) => event.preventDefault());
  });

  function releaseAll() {
    [...heldKeys].forEach(release);
    document.querySelectorAll('#mobile-controls button.is-pressed').forEach((button) => {
      button.classList.remove('is-pressed');
    });
  }
  window.addEventListener('blur', releaseAll);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) releaseAll();
  });
})();
