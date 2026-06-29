# MyTowerOfHanoi

A visual, educational platform designed to explore the classic Tower of Hanoi mathematical puzzle through different solving approaches. It bridges classic computer science algorithms with modern agentic AI by demonstrating recursive, search-based, and reinforcement learning solvers.

## Features
- Interactive drag-and-drop or click-to-move gameplay
- Multiple solvers: Recursive, Iterative, A* Search, and Q-learning
- Local persistence using SQLite (stored in the `artefacts` directory)
- Leaderboard and Analytics Dashboard

## Requirements
- Python 3.10+
- Dependencies listed in `requirements.txt`

## Running Instructions

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the development server**:
   ```bash
   uvicorn main:app --reload
   ```

3. **Open the application**:
   Open your web browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** Vanilla JS, Jinja2 Templates, Tailwind CSS
- **Database:** SQLite & SQLAlchemy
