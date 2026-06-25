class HanoiGameClient {
    constructor() {
        this.numDisks = 3;
        this.pegs = [[], [], []];
        this.moveCount = 0;
        this.startTime = null;
        this.endTime = null;
        this.timerInterval = null;
        this.selectedPeg = null; // for click-to-move
        this.movesList = []; // list of {from_peg, to_peg}
        this.isPlaying = false;

        // Element bindings
        this.diskCountSelect = document.getElementById('diskCount');
        this.startGameBtn = document.getElementById('startGameBtn');
        this.moveCounter = document.getElementById('moveCounter');
        this.optimalMoves = document.getElementById('optimalMoves');
        this.timeCounter = document.getElementById('timeCounter');
        this.gameStatusText = document.getElementById('gameStatusText');
        this.efficiencyRate = document.getElementById('efficiencyRate');
        this.validationFeedback = document.getElementById('validationFeedback');
        this.validationMsg = document.getElementById('validationMsg');
        this.winOverlay = document.getElementById('winOverlay');
        this.winMoves = document.getElementById('winMoves');
        this.winTime = document.getElementById('winTime');
        this.restartBtn = document.getElementById('restartBtn');
        this.refreshRunsBtn = document.getElementById('refreshRunsBtn');
        this.runsTableBody = document.getElementById('runsTableBody');
        this.boardContainer = document.getElementById('boardContainer');

        this.diskColors = [
            'from-rose-500 to-orange-500 text-rose-50 shadow-rose-500/20 border-rose-400/30', // Disk 8
            'from-orange-500 to-amber-500 text-orange-50 shadow-orange-500/20 border-orange-400/30', // Disk 7
            'from-amber-500 to-yellow-500 text-amber-950 shadow-amber-500/20 border-amber-400/30', // Disk 6
            'from-lime-500 to-emerald-500 text-emerald-950 shadow-emerald-500/20 border-lime-400/30', // Disk 5
            'from-emerald-500 to-teal-500 text-teal-950 shadow-emerald-500/20 border-emerald-400/30', // Disk 4
            'from-cyan-500 to-blue-500 text-cyan-50 shadow-cyan-500/20 border-cyan-400/30', // Disk 3
            'from-blue-500 to-violet-500 text-blue-50 shadow-blue-500/20 border-blue-400/30', // Disk 2
            'from-violet-500 to-fuchsia-500 text-violet-50 shadow-violet-500/20 border-violet-400/30' // Disk 1
        ];

        this.init();
    }

    init() {
        this.startGameBtn.addEventListener('click', () => this.startNewGame());
        this.restartBtn.addEventListener('click', () => this.startNewGame());
        this.refreshRunsBtn.addEventListener('click', () => this.loadRecentRuns());
        
        // Setup peg columns click and drag handlers
        document.querySelectorAll('.peg-column').forEach(column => {
            column.addEventListener('click', (e) => this.handlePegClick(column, e));
            
            // Drag and drop event listeners
            column.addEventListener('dragover', (e) => this.handleDragOver(column, e));
            column.addEventListener('dragenter', (e) => this.handleDragEnter(column, e));
            column.addEventListener('dragleave', (e) => this.handleDragLeave(column, e));
            column.addEventListener('drop', (e) => this.handleDrop(column, e));
        });

        // Initialize state on page load
        this.startNewGame();
    }

    startNewGame() {
        this.numDisks = parseInt(this.diskCountSelect.value, 10);
        this.moveCount = 0;
        this.selectedPeg = null;
        this.movesList = [];
        this.endTime = null;
        
        // Setup initial disks state on Peg 0
        this.pegs = [
            Array.from({ length: this.numDisks }, (_, i) => this.numDisks - i),
            [],
            []
        ];

        // Reset display info
        this.moveCounter.textContent = '0';
        this.optimalMoves.textContent = (Math.pow(2, this.numDisks) - 1).toString();
        this.efficiencyRate.textContent = '100%';
        this.efficiencyRate.className = 'text-2xl font-black text-indigo-400 font-mono';
        this.timeCounter.textContent = '00:00';
        this.gameStatusText.textContent = 'Playing';
        this.gameStatusText.className = 'text-indigo-400 font-semibold';
        
        // Hide overlay
        this.winOverlay.classList.add('opacity-0', 'pointer-events-none');

        // Start timer
        this.startTime = new Date();
        this.isPlaying = true;
        this.startTimer();
        
        // Render
        this.renderBoard();
    }

    startTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
        }
        this.timerInterval = setInterval(() => {
            if (!this.isPlaying) return;
            const elapsed = Math.floor((new Date() - this.startTime) / 1000);
            const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
            const seconds = (elapsed % 60).toString().padStart(2, '0');
            this.timeCounter.textContent = `${minutes}:${seconds}`;
        }, 1000);
    }

    renderBoard() {
        for (let p = 0; p < 3; p++) {
            const stackContainer = document.getElementById(`stack-${p}`);
            stackContainer.innerHTML = '';
            
            const currentStack = this.pegs[p];
            currentStack.forEach((diskSize, index) => {
                const isTopDisk = (index === currentStack.length - 1);
                const diskEl = document.createElement('div');
                
                // Base classes for the disk
                diskEl.className = 'h-7 rounded-lg flex items-center justify-center font-bold text-xs shadow-md border select-none disk-transition z-10';
                
                // Color gradient assignment (smaller disks map to colors from smallest index list)
                const colorIdx = this.diskColors.length - 1 - (this.numDisks - diskSize);
                const gradientClasses = this.diskColors[Math.max(0, Math.min(colorIdx, this.diskColors.length - 1))];
                diskEl.className += ` bg-gradient-to-r ${gradientClasses}`;
                
                // Set proportional width
                const widthPercent = (diskSize / this.numDisks) * 75 + 20; // range from 20% to 95%
                diskEl.style.width = `${widthPercent}%`;
                
                // Inner label
                diskEl.innerHTML = `<span class="opacity-80">${diskSize}</span>`;
                
                // Data attributes
                diskEl.setAttribute('data-disk-size', diskSize);
                
                // Enable Drag for top disk
                if (isTopDisk) {
                    diskEl.setAttribute('draggable', 'true');
                    diskEl.classList.add('cursor-grab', 'active:cursor-grabbing');
                    
                    // Highlight if selected for click-to-move
                    if (this.selectedPeg === p) {
                        diskEl.classList.add('selected-disk-glow');
                    }
                    
                    // Drag start/end handlers
                    diskEl.addEventListener('dragstart', (e) => this.handleDragStart(p, e));
                    diskEl.addEventListener('dragend', (e) => this.handleDragEnd(diskEl, e));
                } else {
                    diskEl.setAttribute('draggable', 'false');
                    diskEl.classList.add('opacity-90');
                }
                
                stackContainer.appendChild(diskEl);
            });
        }
    }

    // CLICK-TO-MOVE INTERACTION HANDLERS
    handlePegClick(column, e) {
        if (!this.isPlaying) return;
        const pegIndex = parseInt(column.getAttribute('data-peg-index'), 10);
        
        if (this.selectedPeg === null) {
            // Select source
            if (this.pegs[pegIndex].length > 0) {
                this.selectedPeg = pegIndex;
                this.renderBoard();
            }
        } else {
            // Source is already selected, select target
            const from = this.selectedPeg;
            const to = pegIndex;
            
            if (from === to) {
                // Cancel selection
                this.selectedPeg = null;
                this.renderBoard();
            } else {
                // Attempt move
                const success = this.attemptMove(from, to);
                this.selectedPeg = null;
                this.renderBoard();
            }
        }
    }

    // DRAG AND DROP HANDLERS
    handleDragStart(pegIndex, e) {
        if (!this.isPlaying) {
            e.preventDefault();
            return;
        }
        this.selectedPeg = null; // Reset click-to-move selection
        e.dataTransfer.setData('text/plain', pegIndex.toString());
        e.dataTransfer.effectAllowed = 'move';
        
        // Add style overlay to column
        setTimeout(() => {
            const disk = e.target;
            disk.classList.add('opacity-40');
        }, 0);
    }

    handleDragEnd(diskEl, e) {
        diskEl.classList.remove('opacity-40');
        document.querySelectorAll('.peg-column').forEach(c => {
            c.querySelector('.peg-shaft').classList.remove('from-indigo-500/30', 'to-violet-500/30');
        });
    }

    handleDragOver(column, e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    }

    handleDragEnter(column, e) {
        e.preventDefault();
        const shaft = column.querySelector('.peg-shaft');
        shaft.classList.add('from-indigo-500/30', 'to-violet-500/30');
    }

    handleDragLeave(column, e) {
        const shaft = column.querySelector('.peg-shaft');
        shaft.classList.remove('from-indigo-500/30', 'to-violet-500/30');
    }

    handleDrop(column, e) {
        e.preventDefault();
        const targetPeg = parseInt(column.getAttribute('data-peg-index'), 10);
        const sourcePeg = parseInt(e.dataTransfer.getData('text/plain'), 10);
        
        // Remove highlighting
        const shaft = column.querySelector('.peg-shaft');
        shaft.classList.remove('from-indigo-500/30', 'to-violet-500/30');

        if (!isNaN(sourcePeg) && sourcePeg !== targetPeg) {
            this.attemptMove(sourcePeg, targetPeg);
        }
        this.renderBoard();
    }

    // CORE GAME OPERATIONS
    attemptMove(from, to) {
        const sourceStack = this.pegs[from];
        const targetStack = this.pegs[to];
        
        if (sourceStack.length === 0) {
            this.showError('Source peg has no disks!');
            return false;
        }
        
        const movingDisk = sourceStack[sourceStack.length - 1];
        const targetTopDisk = targetStack[targetStack.length - 1];
        
        if (targetTopDisk && targetTopDisk < movingDisk) {
            this.showError('Cannot place larger disk on smaller disk!');
            return false;
        }
        
        // Execute move
        sourceStack.pop();
        targetStack.push(movingDisk);
        this.moveCount++;
        this.movesList.push({ from_peg: from, to_peg: to });
        
        // Update stats
        this.moveCounter.textContent = this.moveCount.toString();
        this.updateEfficiency();
        
        // Check win condition (all disks on Peg 2)
        if (this.pegs[2].length === this.numDisks) {
            this.handleWin();
        }
        
        return true;
    }

    updateEfficiency() {
        const minMoves = Math.pow(2, this.numDisks) - 1;
        if (this.moveCount <= minMoves) {
            this.efficiencyRate.textContent = '100%';
            this.efficiencyRate.className = 'text-2xl font-black text-indigo-400 font-mono';
        } else {
            const rate = Math.round((minMoves / this.moveCount) * 100);
            this.efficiencyRate.textContent = `${rate}%`;
            if (rate > 80) {
                this.efficiencyRate.className = 'text-2xl font-black text-emerald-400 font-mono';
            } else if (rate > 50) {
                this.efficiencyRate.className = 'text-2xl font-black text-amber-400 font-mono';
            } else {
                this.efficiencyRate.className = 'text-2xl font-black text-rose-400 font-mono';
            }
        }
    }

    showError(msg) {
        // Warning Toast
        this.validationMsg.textContent = msg;
        this.validationFeedback.classList.remove('opacity-0', 'pointer-events-none');
        
        // Shake Board Animation
        this.boardContainer.classList.add('shake-animation');
        
        // Reset effects
        setTimeout(() => {
            this.validationFeedback.classList.add('opacity-0', 'pointer-events-none');
            this.boardContainer.classList.remove('shake-animation');
        }, 2000);
    }

    handleWin() {
        this.isPlaying = false;
        this.endTime = new Date();
        clearInterval(this.timerInterval);
        
        const secondsElapsed = Math.floor((this.endTime - this.startTime) / 1000);
        
        this.gameStatusText.textContent = 'Winner!';
        this.gameStatusText.className = 'text-emerald-400 font-semibold';
        
        // Show Win Overlay
        this.winMoves.textContent = this.moveCount.toString();
        this.winTime.textContent = secondsElapsed.toString();
        this.winOverlay.classList.remove('opacity-0', 'pointer-events-none');
        
        // Log stats and save to DB
        this.saveRunToDB(secondsElapsed);
    }

    async saveRunToDB(secondsElapsed) {
        const payload = {
            num_disks: this.numDisks,
            solver_type: 'manual',
            start_time: this.startTime.toISOString(),
            end_time: this.endTime.toISOString(),
            total_moves: this.moveCount,
            moves: this.movesList
        };

        try {
            const response = await fetch('/api/runs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            if (response.ok) {
                this.loadRecentRuns();
            } else {
                console.error('Failed to log run:', await response.text());
            }
        } catch (err) {
            console.error('Network error saving game run:', err);
        }
    }

    async loadRecentRuns() {
        try {
            const response = await fetch('/api/runs?limit=10');
            if (response.ok) {
                const runs = await response.json();
                this.updateLeaderboard(runs);
            }
        } catch (err) {
            console.error('Network error fetching runs:', err);
        }
    }

    updateLeaderboard(runs) {
        this.runsTableBody.innerHTML = '';
        if (runs.length === 0) {
            this.runsTableBody.innerHTML = `
                <tr id="noRunsFallbackRow">
                    <td colspan="4" class="px-3 py-8 text-center text-xs text-slate-500 font-mono">
                        No runs recorded yet.<br>Complete a game to log stats!
                    </td>
                </tr>
            `;
            return;
        }

        runs.forEach(run => {
            const elapsedSeconds = run.end_time 
                ? Math.round((new Date(run.end_time) - new Date(run.start_time)) / 1000)
                : '—';
            
            const row = document.createElement('tr');
            row.className = 'hover:bg-slate-800/30 transition-colors duration-150';
            row.innerHTML = `
                <td class="px-3 py-3 whitespace-nowrap text-sm font-semibold text-slate-300">#${run.id}</td>
                <td class="px-3 py-3 whitespace-nowrap text-sm text-indigo-400 text-center font-bold">${run.num_disks}</td>
                <td class="px-3 py-3 whitespace-nowrap text-sm text-slate-300 text-center font-mono font-medium">${run.total_moves}</td>
                <td class="px-3 py-3 whitespace-nowrap text-sm text-slate-400 text-right font-mono">${elapsedSeconds}s</td>
            `;
            this.runsTableBody.appendChild(row);
        });
    }
}

// Instantiate client game on page load
document.addEventListener('DOMContentLoaded', () => {
    window.gameClient = new HanoiGameClient();
});
