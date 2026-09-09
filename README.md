# Intelligent Maze Solver (PBL Project)

## Project Title
Intelligent Maze Solver using BFS & DFS

## Project Description
A complete, interactive web application built with Streamlit that visually demonstrates how Breadth-First Search (BFS) and Depth-First Search (DFS) algorithmically solve maze pathfinding problems. Designed specifically for university Project-Based Learning (PBL) presentations, it includes interactive generation, live algorithmic step-animation, comparative statistics, and built-in educational theory notes for Viva preparation.

## Features
- **Random Maze Generation**: Dynamically generate mazes using randomized DFS carving with cycle injections for varied AI behavior.
- **Algorithm Switcher**: Toggle instantly between BFS and DFS.
- **Live Search Visualization**: Watch exactly how the Queue (BFS) vs Stack (DFS) explores nodes via adjustable animation speeds. 
- **Analytics Dashboard**: Compare Cells Explored vs Final Path Length to prove that BFS guarantees the shortest route while DFS does not.
- **Educational Hub**: Built-in definitions, Big-O complexities, and Viva notes.

## Technologies Used
- Python 3.x
- Streamlit (Web Application Framework)
- Standard Library (`collections.deque`, `random`, `time`)
- HTML/CSS (For blazing-fast grid rendering inside Streamlit)

## How BFS Works
Breadth-First Search (BFS) explores the maze level-by-level spreading out evenly in all directions. It uses a **Queue (FIFO)**. Because it systematically tests all paths of length `N` before checking length `N+1`, it perfectly guarantees finding the shortest possible path between start and finish.

## How DFS Works 
Depth-First Search (DFS) picks a direction and aggressively goes as deep as possible until reaching a dead-end, then backtracks. It uses a **Stack (LIFO)**. Because it prioritizes depth, it wanders aimlessly and often produces a very winding, suboptimal solution.

## Installation Steps
1. Make sure Python 3.8+ is installed.
2. Clone or open the project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Application
Run the following command from the root directory of the project:
```bash
streamlit run app.py
```
This will automatically open the web application in your default browser at `http://localhost:8501`.

## Project Structure
```text
intelligent-maze-solver/
│
├── app.py                  # Main Streamlit web application & UI
├── requirements.txt        # Required Python packages
├── README.md               # You are here
│
├── algorithms/
│   ├── bfs.py              # Breadth-First Search mathematical logic
│   └── dfs.py              # Depth-First Search mathematical logic
│
└── maze/
    └── generator.py        # Algorithmic maze generation (Randomized DFS)
```

## Expected Output
When run, you should see a clean sidebar with Maze Settings up to 41x31. The main view contains three tabs: Maze Visualizer, Statistics, and Educational Demo. Clicking "Solve Maze" renders a visually satisfying flow of visited state blocks leading from the green start 'S' to the red end 'E', culminating in a thick yellow solution path.

## Future Enhancements
- Addition of A* (A-Star) search using Heuristics.
- Custom maze drawing (click-to-add walls).
- Weighted grids with terrain costs.
