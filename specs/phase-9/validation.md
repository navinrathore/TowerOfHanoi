# Phase 9 Validation — UI Polish & Accessibility

## Definition of Done

All checks in this document must pass before Phase 9 is considered complete.

### 1. Code Quality & Format Checks

#### Linting & Formatting
```bash
ruff check main.py tests/test_dashboard.py
ruff format --check main.py tests/test_dashboard.py
```
Must report success.

### 2. Manual Verification Checklist

#### 1. Transition Animation Checks
- Click a peg stack and click a target peg. Verify that the disk slides smoothly from the starting peg to the target peg over a 350ms period, instead of jumping instantly.
- Click "Solve & Visualize" for any solver. Verify that each step of the solver playback triggers the same smooth FLIP transitions.

#### 2. Keyboard Control Checks
- Press `Tab` to navigate to the rods. Confirm that a glowing highlight ring outlines the focused peg.
- Use `ArrowRight` / `ArrowLeft` / `ArrowUp` / `ArrowDown` to shift focus between Peg A, Peg B, and Peg C.
- Press `Space` or `Enter` on a focused peg to select its top disk, move focus to another peg, and press `Space` or `Enter` to place it.
- Alternatively, press key `1` to select Peg A, and key `3` to place the disk on Peg C. Confirm the move executes.

#### 3. Screen Reader / Accessibility Checks
- Inspect the page DOM and find `<div id="ariaAnnouncer" class="sr-only" aria-live="polite"></div>`.
- Perform game actions (selecting a disk, making a move, invalid placement) and verify that the announcer's inner text changes to reflect the status.

#### 4. Mobile Responsiveness Checks
- Inspect the webpage under a mobile emulator width (e.g., iPhone/Pixel width < 480px).
- Verify that the peg columns shrink to a shorter height (`h-44`) and the disks stack and scale correctly without overlapping or going off-screen.
