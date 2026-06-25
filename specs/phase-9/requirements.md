# Phase 9 Requirements — UI Polish & Accessibility

## Scope

Polish the Tower of Hanoi application's visual interface and responsiveness, adding smooth transitions and keyboard/screen-reader accessibility enhancements.

1. **Visual Animations**:
   - Integrate **FLIP (First, Last, Invert, Play)** visual transition mechanics for manual, keyboard, and simulated disk moves. Bounding rectangles before and after states must be calculated to animate a 350ms slide transition.

2. **Mobile Responsiveness**:
   - Rod dimensions must dynamically adjust (`h-44 sm:h-64`) using Tailwind break points.
   - Disks should stack cleanly and scale down contextually to avoid clipping on smaller viewports.

3. **Keyboard Accessibility**:
   - Numeric triggers `1`/`2`/`3` must immediately select Peg 0, 1, or 2 to select or move a disk.
   - Column columns must support focus-visible highlights (`outline: 3px solid rgba(139, 92, 246, 0.8)`).
   - Traversal via arrow keys (Right/Down to shift right, Left/Up to shift left) and selection via Enter/Space must be supported.

4. **Announcer Announcements**:
   - Maintain a visually hidden screen reader block with `aria-live="polite"` to broadcast interactive announcements, such as `"Selected disk of size 2 on Peg A"` or `"Moved disk 1 from Peg A to Peg C."`

## Design Decisions

- **FLIP-based Transitions**: Animate layout changes using standard CSS transforms rather than layout calculations, ensuring high framerate animations on all devices.
- **Tailwind CDN Config**: Extend Tailwind themes with custom utility overrides to support focus highlights.
- **Pure JavaScript Announcements**: Maintain announcements entirely inside the game client loop, eliminating extra library dependencies.
