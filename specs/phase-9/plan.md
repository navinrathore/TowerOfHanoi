# Phase 9 Plan — UI Polish & Accessibility

This document outlines the step-by-step group tasks for implementing transition animations, keyboard listeners, mobile breakpoints, and ARIA announcements.

---

## Group 1 — Styling & Layout

1. Add focus-visible highlights to peg columns in `static/css/styles.css`.
2. Add focus attributes and ARIA roles (e.g. `tabindex="0"`, `role="button"`) to peg elements in `templates/index.html`.
3. Add responsive class overrides (`h-44 sm:h-64`) on rod columns to handle mobile layouts.

## Group 2 — Accessibility Handlers

4. In `static/js/game.js`, bind keydown listeners on the document to capture numeric hotkeys (`1`/`2`/`3`).
5. Bind keydown listeners on individual columns to handle:
   - `Enter` or `Space` for selecting/moving.
   - `ArrowRight` or `ArrowDown` to shift keyboard focus to the next peg.
   - `ArrowLeft` or `ArrowUp` to shift keyboard focus to the previous peg.
6. Create an offscreen screen-reader element `#ariaAnnouncer` with `aria-live="polite"` inside `templates/index.html`.
7. Implement `announceAria(msg)` helper in `static/js/game.js` to speak game operations (disk selections, invalid moves, and completions).

## Group 3 — FLIP Transitions

8. Implement `animateMove(from, to, diskSize, updateCallback)` in `static/js/game.js`:
   - Calculate bounding rects of the source disk.
   - Run the state updates.
   - Read the target coordinates after the board re-renders.
   - Invert the translation offset and play the 350ms slide transition back to zero.
9. Wrap manual moves, solver steps, and rewind steps to run through the `animateMove` transition block.

## Group 4 — Verification

10. Run automated tests to check for script regression.
11. Perform manual user walkthrough checks using keyboard inputs and viewport inspections.
