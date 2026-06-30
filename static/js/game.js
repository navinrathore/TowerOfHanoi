class HanoiGameClient {
    constructor() {
        this.numDisks = 3;
        this.pegs = [[], [], []];
        this.moveCount = 0;
        this.startTime = null;
        this.endTime = null;
        this.timerInterval = null;
        this.accumulatedSeconds = 0; // for persistence
        this.lastTickTime = null; // for persistence
        this.selectedPeg = null; // for click-to-move
        this.movesList = []; // list of {from_peg, to_peg}
        this.isPlaying = false;

        // Auto-Solver state variables
        this.isVisualizing = false;
        this.visualMoves = [];
        this.currentMoveIndex = -1;
        this.isPlayingVisual = false;
        this.playbackSpeed = 500; // ms per step
        this.visualInterval = null;
        this.visualStartTime = null;
        this.visualTimeElapsed = 0;
        this.visualTimerInterval = null;
        this.solverType = null;
        this.solverComputeTime = 0.0;

        // Element bindings
        this.diskCountSelect = document.getElementById('diskCount');
        this.playerNameInput = document.getElementById('playerNameInput');
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

        // Resume Modal bindings
        this.resumeGameModal = document.getElementById('resumeGameModal');
        this.resumeGameBtn = document.getElementById('resumeGameBtn');
        this.discardGameBtn = document.getElementById('discardGameBtn');

        // Solver bindings
        this.solveBtn = document.getElementById('solveBtn');
        this.solverTypeSelect = document.getElementById('solverType');
        this.solverPlaybackControls = document.getElementById('solverPlaybackControls');
        this.stepBackBtn = document.getElementById('stepBackBtn');
        this.playPauseBtn = document.getElementById('playPauseBtn');
        this.stepForwardBtn = document.getElementById('stepForwardBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.playbackSpeedSlider = document.getElementById('playbackSpeed');
        this.speedValue = document.getElementById('speedValue');
        this.stepProgressText = document.getElementById('stepProgressText');
        this.stepProgressBar = document.getElementById('stepProgressBar');
        this.playIcon = document.getElementById('playIcon');
        this.pauseIcon = document.getElementById('pauseIcon');
        this.winTitle = document.getElementById('winTitle');
        this.winDescription = document.getElementById('winDescription');

        // Q-learning configuration elements
        this.qlearningConfigContainer = document.getElementById('qlearningConfigContainer');
        this.qEpisodesInput = document.getElementById('qEpisodes');
        this.qAlphaInput = document.getElementById('qAlpha');
        this.qGammaInput = document.getElementById('qGamma');
        this.qEpsilonInput = document.getElementById('qEpsilon');
        this.trainQBtn = document.getElementById('trainQBtn');
        this.qTrainingStatus = document.getElementById('qTrainingStatus');
        this.qTrainingStatusText = document.getElementById('qTrainingStatusText');
        this.qMetricsContainer = document.getElementById('qMetricsContainer');
        this.qTrainTimeVal = document.getElementById('qTrainTimeVal');
        this.qTrainSuccessVal = document.getElementById('qTrainSuccessVal');
        this.qRewardSvgChart = document.getElementById('qRewardSvgChart');

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
        
        // Solver event listeners
        this.solveBtn.addEventListener('click', () => this.startVisualization());
        this.playPauseBtn.addEventListener('click', () => this.togglePlayback());
        this.stepBackBtn.addEventListener('click', () => this.stepBackward());
        this.stepForwardBtn.addEventListener('click', () => this.stepForward());
        this.stopBtn.addEventListener('click', () => this.stopVisualization(true));
        this.playbackSpeedSlider.addEventListener('input', (e) => this.handleSpeedChange(e));
        this.solverTypeSelect.addEventListener('change', () => this.handleSolverTypeChange());
        this.trainQBtn.addEventListener('click', () => this.trainQAgent());

        // Setup peg columns click, drag, and keyboard handlers
        document.querySelectorAll('.peg-column').forEach(column => {
            column.addEventListener('click', (e) => this.handlePegClick(column, e));
            
            // Keyboard event handlers
            column.addEventListener('keydown', (e) => {
                if (!this.isPlaying || this.isVisualizing) return;
                const pegIndex = parseInt(column.getAttribute('data-peg-index'), 10);
                
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.selectPegAction(pegIndex);
                } else if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
                    e.preventDefault();
                    const nextPegIndex = (pegIndex + 1) % 3;
                    document.querySelectorAll('.peg-column')[nextPegIndex].focus();
                } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
                    e.preventDefault();
                    const prevPegIndex = (pegIndex - 1 + 3) % 3;
                    document.querySelectorAll('.peg-column')[prevPegIndex].focus();
                }
            });
            
            // Drag and drop event listeners
            column.addEventListener('dragover', (e) => this.handleDragOver(column, e));
            column.addEventListener('dragenter', (e) => this.handleDragEnter(column, e));
            column.addEventListener('dragleave', (e) => this.handleDragLeave(column, e));
            column.addEventListener('drop', (e) => this.handleDrop(column, e));
        });

        // Document keydown hotkeys (1, 2, 3)
        document.addEventListener('keydown', (e) => {
            if (!this.isPlaying || this.isVisualizing) return;
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
            
            if (e.key === '1') {
                this.selectPegAction(0);
            } else if (e.key === '2') {
                this.selectPegAction(1);
            } else if (e.key === '3') {
                this.selectPegAction(2);
            }
        });

        // Setup player name
        if (this.playerNameInput) {
            const savedName = localStorage.getItem('hanoi_player_name');
            if (savedName) {
                this.playerNameInput.value = savedName;
            }
            this.playerNameInput.addEventListener('change', () => {
                localStorage.setItem('hanoi_player_name', this.playerNameInput.value.trim());
            });
        }

        // Initialize state on page load
        if (localStorage.getItem('hanoi_saved_game')) {
            if (this.resumeGameModal) {
                this.resumeGameModal.classList.remove('hidden');
                
                this.resumeGameBtn.addEventListener('click', () => {
                    this.loadGameFromStorage();
                    this.resumeGameModal.classList.add('hidden');
                });
                
                this.discardGameBtn.addEventListener('click', () => {
                    this.clearGameFromStorage();
                    this.startNewGame();
                    this.resumeGameModal.classList.add('hidden');
                });
            } else {
                if (!this.loadGameFromStorage()) {
                    this.startNewGame();
                }
            }
        } else {
            this.startNewGame();
        }
        
        // Save on unload
        window.addEventListener('beforeunload', () => {
            if (this.isPlaying) {
                this.saveGameToStorage();
            }
        });
    }

    saveGameToStorage() {
        if (!this.isPlaying) return;
        const state = {
            numDisks: this.numDisks,
            pegs: this.pegs,
            moveCount: this.moveCount,
            movesList: this.movesList,
            accumulatedSeconds: this.accumulatedSeconds
        };
        localStorage.setItem('hanoi_saved_game', JSON.stringify(state));
    }

    loadGameFromStorage() {
        const saved = localStorage.getItem('hanoi_saved_game');
        if (!saved) return false;
        try {
            const state = JSON.parse(saved);
            this.numDisks = state.numDisks;
            this.pegs = state.pegs;
            this.moveCount = state.moveCount;
            this.movesList = state.movesList;
            this.accumulatedSeconds = state.accumulatedSeconds;

            // Sync UI
            this.diskCountSelect.value = this.numDisks;
            this.moveCounter.textContent = this.moveCount.toString();
            this.optimalMoves.textContent = (Math.pow(2, this.numDisks) - 1).toString();
            this.updateEfficiency();
            
            const totalSeconds = Math.floor(this.accumulatedSeconds);
            const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
            const seconds = (totalSeconds % 60).toString().padStart(2, '0');
            this.timeCounter.textContent = `${minutes}:${seconds}`;

            this.gameStatusText.textContent = 'Playing (Resumed)';
            this.gameStatusText.className = 'text-indigo-400 font-semibold';
            
            this.winOverlay.classList.add('opacity-0', 'pointer-events-none');
            
            this.isPlaying = true;
            this.startTime = new Date(); // Reset start time for session API but logic uses accumulated
            this.renderBoard();
            this.startTimer();
            return true;
        } catch (e) {
            console.error('Failed to load saved game', e);
            return false;
        }
    }

    clearGameFromStorage() {
        localStorage.removeItem('hanoi_saved_game');
    }

    startNewGame() {
        this.clearGameFromStorage();
        // Clean up visualizer if active
        this.stopVisualization(false);

        this.numDisks = parseInt(this.diskCountSelect.value, 10);
        this.moveCount = 0;
        this.selectedPeg = null;
        this.movesList = [];
        this.endTime = null;
        this.accumulatedSeconds = 0;
        this.lastTickTime = null;
        
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
        
        // Reset overlay texts to manual defaults
        if (this.winTitle) this.winTitle.textContent = "Victory Achieved!";
        if (this.winDescription) {
            this.winDescription.innerHTML = `Puzzle solved in <span id="winMoves" class="text-emerald-400 font-bold font-mono">0</span> moves and <span id="winTime" class="text-emerald-400 font-bold font-mono">0</span> seconds.`;
            // Re-bind the elements that were inside winDescription
            this.winMoves = document.getElementById('winMoves');
            this.winTime = document.getElementById('winTime');
        }

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
        this.lastTickTime = Date.now();
        this.timerInterval = setInterval(() => {
            if (!this.isPlaying) return;
            const now = Date.now();
            this.accumulatedSeconds += (now - this.lastTickTime) / 1000;
            this.lastTickTime = now;

            const totalSeconds = Math.floor(this.accumulatedSeconds);
            const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
            const seconds = (totalSeconds % 60).toString().padStart(2, '0');
            this.timeCounter.textContent = `${minutes}:${seconds}`;
        }, 200); // Check 5 times a second for smoother state accumulation
    }

    renderBoard() {
        for (let p = 0; p < 3; p++) {
            const stackContainer = document.getElementById(`stack-${p}`);
            stackContainer.innerHTML = '';
            
            const currentStack = this.pegs[p];
            const pegColumn = document.querySelector(`.peg-column[data-peg-index="${p}"]`);
            if (pegColumn) {
                const disksText = currentStack.length > 0 
                    ? `contains ${currentStack.length} disks: size ${currentStack.join(', ')}`
                    : 'empty';
                pegColumn.setAttribute('aria-label', `Peg ${String.fromCharCode(65 + p)}: ${disksText}`);
            }

            currentStack.forEach((diskSize, index) => {
                const isTopDisk = (index === currentStack.length - 1);
                const diskEl = document.createElement('div');
                
                // Base classes for the disk (using responsive h-5 sm:h-7 for mobile)
                diskEl.className = 'h-5 sm:h-7 rounded-lg flex items-center justify-center font-bold text-xs shadow-md border select-none disk-transition z-10';
                
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
        if (!this.isPlaying || this.isVisualizing) return;
        const pegIndex = parseInt(column.getAttribute('data-peg-index'), 10);
        this.selectPegAction(pegIndex);
    }

    // DRAG AND DROP HANDLERS
    handleDragStart(pegIndex, e) {
        if (!this.isPlaying || this.isVisualizing) {
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
            this.announceAria('Invalid move: Source peg has no disks!');
            return false;
        }
        
        const movingDisk = sourceStack[sourceStack.length - 1];
        const targetTopDisk = targetStack[targetStack.length - 1];
        
        if (targetTopDisk && targetTopDisk < movingDisk) {
            this.showError('Cannot place larger disk on smaller disk!');
            this.announceAria('Invalid move: Cannot place larger disk on smaller disk!');
            return false;
        }
        
        // Execute move with FLIP slide animation
        this.animateMove(from, to, movingDisk, () => {
            sourceStack.pop();
            targetStack.push(movingDisk);
            this.moveCount++;
            this.movesList.push({ from_peg: from, to_peg: to });
            
            this.moveCounter.textContent = this.moveCount.toString();
            this.updateEfficiency();
            
            this.announceAria(`Moved disk ${movingDisk} from Peg ${String.fromCharCode(65 + from)} to Peg ${String.fromCharCode(65 + to)}.`);

            this.saveGameToStorage();

            if (this.pegs[2].length === this.numDisks) {
                this.handleWin();
            }
        });
        
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
        
        // Add any remaining fractional seconds from the last tick
        const now = Date.now();
        if (this.lastTickTime) {
            this.accumulatedSeconds += (now - this.lastTickTime) / 1000;
        }
        
        const secondsElapsed = Math.floor(this.accumulatedSeconds);
        
        this.gameStatusText.textContent = 'Winner!';
        this.gameStatusText.className = 'text-emerald-400 font-semibold';
        
        // Show Win Overlay
        this.winMoves.textContent = this.moveCount.toString();
        this.winTime.textContent = secondsElapsed.toString();
        this.winOverlay.classList.remove('opacity-0', 'pointer-events-none');
        
        this.clearGameFromStorage();
        
        // Log stats and save to DB
        this.saveRunToDB(secondsElapsed);
    }

    async saveRunToDB(secondsElapsed) {
        // Adjust start time so DB duration exactly matches accumulated seconds
        const syntheticStartTime = new Date(this.endTime.getTime() - secondsElapsed * 1000);
        const pName = this.playerNameInput ? (this.playerNameInput.value.trim() || null) : null;

        const payload = {
            num_disks: this.numDisks,
            solver_type: 'manual',
            player_name: pName,
            start_time: syntheticStartTime.toISOString(),
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
                <td class="px-3 py-3 whitespace-nowrap text-sm font-semibold text-slate-300">
                    #${run.id} ${run.player_name ? `<span class="text-xs text-slate-500 font-normal ml-1">(${run.player_name})</span>` : ''}
                </td>
                <td class="px-3 py-3 whitespace-nowrap text-sm text-indigo-400 text-center font-bold">${run.num_disks}</td>
                <td class="px-3 py-3 whitespace-nowrap text-sm text-slate-300 text-center font-mono font-medium">${run.total_moves}</td>
                <td class="px-3 py-3 whitespace-nowrap text-sm text-slate-400 text-right font-mono">${elapsedSeconds}s</td>
            `;
            this.runsTableBody.appendChild(row);
        });
    }

    // AUTO-SOLVER PLAYBACK & SIMULATION MECHANICS
    async startVisualization() {
        // Stop any active manual game
        this.isPlaying = false;
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
        }

        this.numDisks = parseInt(this.diskCountSelect.value, 10);
        this.solverType = this.solverTypeSelect.value;

        const isSearchOrRL = (this.solverType === 'search' || this.solverType === 'qlearning');
        const isAlreadySolved = (this.pegs[2].length === this.numDisks);

        if (!isSearchOrRL || isAlreadySolved) {
            // Reset to standard configuration
            this.pegs = [
                Array.from({ length: this.numDisks }, (_, i) => this.numDisks - i),
                [],
                []
            ];
            this.renderBoard();
        }

        this.moveCount = 0;

        // Update top stats panel
        this.moveCounter.textContent = '0';
        this.optimalMoves.textContent = (Math.pow(2, this.numDisks) - 1).toString();
        this.efficiencyRate.textContent = '100%';
        this.efficiencyRate.className = 'text-2xl font-black text-indigo-400 font-mono';
        this.timeCounter.textContent = '00:00';
        this.gameStatusText.textContent = 'Solving...';
        this.gameStatusText.className = 'text-violet-400 font-semibold';

        // Hide win overlay
        this.winOverlay.classList.add('opacity-0', 'pointer-events-none');

        // Build API URL
        let url = `/api/solve/${this.solverType}?num_disks=${this.numDisks}`;
        if (isSearchOrRL) {
            const stateParam = encodeURIComponent(JSON.stringify(this.pegs));
            url += `&state=${stateParam}`;
        }

        try {
            const response = await fetch(url);
            if (response.ok) {
                const data = await response.json();
                this.visualMoves = data.moves;
                this.solverComputeTime = data.compute_time_ms || 0.0;
                this.isVisualizing = true;
                this.currentMoveIndex = -1;
                this.visualTimeElapsed = 0;
                
                // Show playback panel
                this.solverPlaybackControls.classList.remove('hidden');
                this.updatePlaybackUI();
                
                // Set status to playing visualization
                this.gameStatusText.textContent = 'Simulating';
                this.gameStatusText.className = 'text-violet-400 font-semibold animate-pulse';

                // Automatically start playing
                this.startPlayback();
                this.startVisualTimer();
            } else {
                this.showError('Failed to retrieve solver steps from API.');
                this.gameStatusText.textContent = 'Error';
                this.gameStatusText.className = 'text-rose-400 font-semibold';
            }
        } catch (err) {
            console.error('Error fetching solver solution:', err);
            this.showError('Network error connecting to solver API.');
            this.gameStatusText.textContent = 'Error';
            this.gameStatusText.className = 'text-rose-400 font-semibold';
        }
    }

    startPlayback() {
        this.isPlayingVisual = true;
        
        // Toggle play/pause buttons
        this.playIcon.classList.add('hidden');
        this.pauseIcon.classList.remove('hidden');

        if (this.visualInterval) clearInterval(this.visualInterval);
        this.visualInterval = setInterval(() => {
            if (this.currentMoveIndex < this.visualMoves.length - 1) {
                this.stepForward();
            } else {
                this.handleVisualComplete();
            }
        }, this.playbackSpeed);
    }

    pausePlayback() {
        this.isPlayingVisual = false;
        
        // Toggle play/pause buttons
        this.playIcon.classList.remove('hidden');
        this.pauseIcon.classList.add('hidden');

        if (this.visualInterval) clearInterval(this.visualInterval);
    }

    togglePlayback() {
        if (this.isPlayingVisual) {
            this.pausePlayback();
        } else {
            this.startPlayback();
        }
    }

    startVisualTimer() {
        if (this.visualTimerInterval) clearInterval(this.visualTimerInterval);
        this.visualTimerInterval = setInterval(() => {
            if (!this.isPlayingVisual) return;
            this.visualTimeElapsed++;
            const minutes = Math.floor(this.visualTimeElapsed / 60).toString().padStart(2, '0');
            const seconds = (this.visualTimeElapsed % 60).toString().padStart(2, '0');
            this.timeCounter.textContent = `${minutes}:${seconds}`;
        }, 1000);
    }

    stopVisualization(resetToManual = true) {
        this.isVisualizing = false;
        this.isPlayingVisual = false;

        if (this.visualInterval) clearInterval(this.visualInterval);
        if (this.visualTimerInterval) clearInterval(this.visualTimerInterval);

        // Hide playback panel
        this.solverPlaybackControls.classList.add('hidden');
        this.playIcon.classList.remove('hidden');
        this.pauseIcon.classList.add('hidden');

        if (resetToManual) {
            this.startNewGame();
        }
    }

    stepForward() {
        if (this.currentMoveIndex >= this.visualMoves.length - 1) return;

        this.currentMoveIndex++;
        const move = this.visualMoves[this.currentMoveIndex];

        const sourceStack = this.pegs[move.from_peg];
        const targetStack = this.pegs[move.to_peg];

        if (sourceStack.length > 0) {
            const disk = sourceStack[sourceStack.length - 1];
            this.animateMove(move.from_peg, move.to_peg, disk, () => {
                sourceStack.pop();
                targetStack.push(disk);
                this.moveCount++;
                this.moveCounter.textContent = this.moveCount.toString();
            });
            this.announceAria(`Visualizer: Moved disk ${disk} from Peg ${String.fromCharCode(65 + move.from_peg)} to Peg ${String.fromCharCode(65 + move.to_peg)}.`);
        }

        this.updatePlaybackUI();

        // Check if finished
        if (this.currentMoveIndex === this.visualMoves.length - 1) {
            this.handleVisualComplete();
        }
    }

    stepBackward() {
        if (this.currentMoveIndex < 0) return;

        // If playing, pause first
        if (this.isPlayingVisual) {
            this.pausePlayback();
        }

        const move = this.visualMoves[this.currentMoveIndex];
        const sourceStack = this.pegs[move.from_peg];
        const targetStack = this.pegs[move.to_peg];

        if (targetStack.length > 0) {
            const disk = targetStack[targetStack.length - 1];
            this.animateMove(move.to_peg, move.from_peg, disk, () => {
                targetStack.pop();
                sourceStack.push(disk);
                this.moveCount--;
                this.moveCounter.textContent = this.moveCount.toString();
            });
            this.announceAria(`Visualizer step back: Moved disk ${disk} back to Peg ${String.fromCharCode(65 + move.from_peg)}.`);
        }

        this.currentMoveIndex--;
        this.updatePlaybackUI();
    }

    updatePlaybackUI() {
        const total = this.visualMoves.length;
        const current = this.currentMoveIndex + 1;

        this.stepProgressText.textContent = `${current} / ${total}`;
        
        const percentage = total > 0 ? (current / total) * 100 : 0;
        this.stepProgressBar.style.width = `${percentage}%`;

        // Update button states
        if (this.currentMoveIndex < 0) {
            this.stepBackBtn.disabled = true;
            this.stepBackBtn.classList.add('opacity-40', 'cursor-not-allowed');
        } else {
            this.stepBackBtn.disabled = false;
            this.stepBackBtn.classList.remove('opacity-40', 'cursor-not-allowed');
        }

        if (this.currentMoveIndex >= this.visualMoves.length - 1) {
            this.stepForwardBtn.disabled = true;
            this.stepForwardBtn.classList.add('opacity-40', 'cursor-not-allowed');
        } else {
            this.stepForwardBtn.disabled = false;
            this.stepForwardBtn.classList.remove('opacity-40', 'cursor-not-allowed');
        }
    }

    handleSpeedChange(e) {
        this.playbackSpeed = parseInt(this.playbackSpeedSlider.value, 10);
        this.speedValue.textContent = `${(this.playbackSpeed / 1000).toFixed(1)}s / step`;
        
        if (this.isPlayingVisual) {
            // Restart interval to apply speed change instantly
            this.startPlayback();
        }
    }

    handleVisualComplete() {
        this.pausePlayback();
        if (this.visualTimerInterval) clearInterval(this.visualTimerInterval);

        this.gameStatusText.textContent = 'Complete';
        this.gameStatusText.className = 'text-emerald-400 font-semibold';

        // Show completed state in Victory overlay
        if (this.winTitle) this.winTitle.textContent = "Solver Completed!";
        if (this.winDescription) {
            this.winDescription.innerHTML = `Auto-solve using <strong>${this.solverType}</strong> solver finished in <span class="text-emerald-400 font-bold font-mono">${this.moveCount}</span> optimal moves and <span class="text-emerald-400 font-bold font-mono">${this.visualTimeElapsed}</span> seconds.`;
        }
        if (this.winMoves) this.winMoves.textContent = this.moveCount.toString();
        if (this.winTime) this.winTime.textContent = this.visualTimeElapsed.toString();
        
        this.winOverlay.classList.remove('opacity-0', 'pointer-events-none');

        // Log visualizer run statistics to DB
        this.saveSolverRunToDB();
    }

    async saveSolverRunToDB() {
        const payload = {
            num_disks: this.numDisks,
            solver_type: this.solverType,
            start_time: new Date(new Date() - this.visualTimeElapsed * 1000).toISOString(),
            end_time: new Date().toISOString(),
            total_moves: this.moveCount,
            compute_time_ms: this.solverComputeTime || 0.0,
            moves: this.visualMoves.map(m => ({ from_peg: m.from_peg, to_peg: m.to_peg }))
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
                console.error('Failed to log solver run:', await response.text());
            }
        } catch (err) {
            console.error('Network error saving solver run:', err);
        }
    }

    handleSolverTypeChange() {
        const val = this.solverTypeSelect.value;
        if (val === 'qlearning') {
            this.qlearningConfigContainer.classList.remove('hidden');
        } else {
            this.qlearningConfigContainer.classList.add('hidden');
        }
    }

    async trainQAgent() {
        // Disable train button and show status
        this.trainQBtn.disabled = true;
        this.trainQBtn.classList.add('opacity-50', 'cursor-not-allowed');
        this.qTrainingStatus.classList.remove('hidden');
        this.qMetricsContainer.classList.add('hidden');
        this.qTrainingStatusText.textContent = "Training agent...";

        const payload = {
            num_disks: this.numDisks,
            episodes: parseInt(this.qEpisodesInput.value, 10) || 1000,
            alpha: parseFloat(this.qAlphaInput.value) || 0.1,
            gamma: parseFloat(this.qGammaInput.value) || 0.9,
            epsilon: parseFloat(this.qEpsilonInput.value) || 0.2
        };

        try {
            const response = await fetch('/api/solve/qlearning/train', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                const data = await response.json();
                this.qTrainingStatus.classList.add('hidden');
                
                // Show metrics
                this.qMetricsContainer.classList.remove('hidden');
                this.qTrainTimeVal.textContent = `${data.training_time_ms.toFixed(0)}ms`;
                this.qTrainSuccessVal.textContent = `${(data.final_success_rate * 100).toFixed(0)}%`;
                
                // Draw chart
                this.drawRewardChart(data.metrics);
            } else {
                const errText = await response.text();
                this.showError(`Training failed: ${errText}`);
                this.qTrainingStatus.classList.add('hidden');
            }
        } catch (err) {
            console.error('Error training agent:', err);
            this.showError('Network error training agent.');
            this.qTrainingStatus.classList.add('hidden');
        } finally {
            this.trainQBtn.disabled = false;
            this.trainQBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        }
    }

    drawRewardChart(metrics) {
        const rewards = metrics.avg_rewards;
        const episodes = metrics.episodes;
        if (!rewards || rewards.length === 0) {
            this.qRewardSvgChart.innerHTML = '<span class="text-[10px] text-slate-500 font-mono">No data.</span>';
            return;
        }

        const width = 240;
        const height = 96;
        const padding = 6;
        
        // Find min and max for scaling
        const minX = episodes[0];
        const maxX = episodes[episodes.length - 1];
        const minY = Math.min(...rewards);
        const maxY = Math.max(...rewards);
        
        const scaleX = (x) => {
            const range = maxX - minX;
            return range === 0 ? padding : padding + ((x - minX) / range) * (width - 2 * padding);
        };
        
        const scaleY = (y) => {
            const range = maxY - minY;
            return range === 0 ? height / 2 : height - padding - ((y - minY) / range) * (height - 2 * padding);
        };
        
        // Build the line path
        let pathD = "";
        let areaD = "";
        
        for (let i = 0; i < episodes.length; i++) {
            const px = scaleX(episodes[i]).toFixed(1);
            const py = scaleY(rewards[i]).toFixed(1);
            
            if (i === 0) {
                pathD += `M ${px} ${py}`;
                areaD += `M ${px} ${scaleY(minY).toFixed(1)} L ${px} ${py}`;
            } else {
                pathD += ` L ${px} ${py}`;
                areaD += ` L ${px} ${py}`;
            }
        }
        
        // Close area path for gradient fill
        const lastX = scaleX(episodes[episodes.length - 1]).toFixed(1);
        const baselineY = scaleY(minY).toFixed(1);
        areaD += ` L ${lastX} ${baselineY} Z`;
        
        const svg = `
            <svg width="100%" height="100%" viewBox="0 0 ${width} ${height}" class="overflow-visible">
                <defs>
                    <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.3"/>
                        <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0.0"/>
                    </linearGradient>
                </defs>
                <!-- Grid lines -->
                <line x1="${padding}" y1="${scaleY(minY)}" x2="${width - padding}" y2="${scaleY(minY)}" stroke="#334155" stroke-dasharray="2" stroke-width="1" />
                <line x1="${padding}" y1="${scaleY(maxY)}" x2="${width - padding}" y2="${scaleY(maxY)}" stroke="#334155" stroke-dasharray="2" stroke-width="1" />
                
                <!-- Area fill -->
                <path d="${areaD}" fill="url(#chartGrad)" />
                
                <!-- Line path -->
                <path d="${pathD}" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
        `;
        
        this.qRewardSvgChart.innerHTML = svg;
    }

    animateMove(from, to, diskSize, updateCallback) {
        const fromStack = document.getElementById(`stack-${from}`);
        let diskEl = null;
        if (fromStack) {
            diskEl = fromStack.querySelector(`[data-disk-size="${diskSize}"]`);
        }
        
        let startRect = null;
        if (diskEl) {
            startRect = diskEl.getBoundingClientRect();
        }
        
        // Update pegs state and rebuild board
        updateCallback();
        this.renderBoard();
        
        if (startRect) {
            const targetDiskEl = document.querySelector(`[data-disk-size="${diskSize}"]`);
            if (targetDiskEl) {
                const endRect = targetDiskEl.getBoundingClientRect();
                const dx = startRect.left - endRect.left;
                const dy = startRect.top - endRect.top;
                
                // FLIP Invert: temporarily position disk back at starting location without transition
                targetDiskEl.style.transform = `translate(${dx}px, ${dy}px)`;
                targetDiskEl.style.transition = 'none';
                
                // Force a layout reflow so the browser registers the non-transitioned style
                targetDiskEl.offsetHeight;
                
                // FLIP Play: animate the disk sliding back to its target position
                targetDiskEl.style.transition = 'transform 350ms cubic-bezier(0.25, 1, 0.5, 1)';
                targetDiskEl.style.transform = 'translate(0, 0)';
                
                // Clean up transition styles once animation ends
                setTimeout(() => {
                    targetDiskEl.style.transition = '';
                    targetDiskEl.style.transform = '';
                }, 350);
            }
        }
    }

    announceAria(msg) {
        const announcer = document.getElementById('ariaAnnouncer');
        if (announcer) {
            announcer.textContent = msg;
        }
    }

    selectPegAction(pegIndex) {
        if (this.selectedPeg === null) {
            if (this.pegs[pegIndex].length > 0) {
                this.selectedPeg = pegIndex;
                const topDisk = this.pegs[pegIndex][this.pegs[pegIndex].length - 1];
                this.announceAria(`Selected disk of size ${topDisk} on Peg ${String.fromCharCode(65 + pegIndex)}. Select target peg.`);
                this.renderBoard();
            } else {
                this.announceAria(`Peg ${String.fromCharCode(65 + pegIndex)} has no disks to select.`);
            }
        } else {
            const from = this.selectedPeg;
            const to = pegIndex;
            
            if (from === to) {
                this.selectedPeg = null;
                this.announceAria(`Selection cancelled.`);
                this.renderBoard();
            } else {
                this.attemptMove(from, to);
                this.selectedPeg = null;
                this.renderBoard();
            }
        }
    }
}

// Instantiate client game on page load
document.addEventListener('DOMContentLoaded', () => {
    window.gameClient = new HanoiGameClient();
});
