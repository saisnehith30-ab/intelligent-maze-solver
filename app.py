import streamlit as st
import time
import math
from maze.generator import generate_maze
from algorithms.bfs import solve_bfs
from algorithms.dfs import solve_dfs

# --- Page Configuration ---
st.set_page_config(
    page_title="Intelligent Maze Solver",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Styling ---
st.markdown("""
<style>
    .maze-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        overflow-x: auto;
    }
    .maze-row {
        display: flex;
    }
    .maze-cell {
        width: 25px;
        height: 25px;
        border: 1px solid #dee2e6;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        transition: background-color 0.1s;
    }
    .cell-path { background-color: #ffffff; }
    .cell-wall { background-color: #343a40; border-color: #343a40; }
    .cell-start { background-color: #28a745; color: white; font-weight: bold; }
    .cell-end { background-color: #dc3545; color: white; font-weight: bold; }
    .cell-visited { background-color: #17a2b8; opacity: 0.7; }
    .cell-final-path { background-color: #ffc107; font-weight: bold; }
    .cell-current { background-color: #fd7e14; }
</style>
""", unsafe_allow_html=True)


# --- Helper to render maze HTML ---
def render_maze(grid, visited=None, path=None, current=None):
    if visited is None: visited = set()
    if path is None: path = set()
    
    html = '<div class="maze-container">'
    rows = len(grid)
    cols = len(grid[0])
    
    for r in range(rows):
        html += '<div class="maze-row">'
        for c in range(cols):
            val = grid[r][c]
            classes = ['maze-cell']
            content = ''
            
            coord = (r, c)
            
            if val == 1:
                classes.append('cell-wall')
            else:
                if val == 2:
                    classes.append('cell-start')
                    content = 'S'
                elif val == 3:
                    classes.append('cell-end')
                    content = 'E'
                else:
                    classes.append('cell-path')

                # Overrides based on algorithm state
                if coord == current and val not in [2, 3]:
                    classes.append('cell-current')
                elif coord in path and val not in [2, 3]:
                    classes.append('cell-final-path')
                    content = '•'
                elif coord in visited and val not in [2, 3]:
                    classes.append('cell-visited')
                    
            html += f'<div class="{" ".join(classes)}">{content}</div>'
        html += '</div>'
    html += '</div>'
    
    return html

# --- Session State Initialization ---
if 'maze_generated' not in st.session_state:
    st.session_state.maze_generated = False
    st.session_state.grid = None
    st.session_state.start_pos = None
    st.session_state.end_pos = None

if 'animation_running' not in st.session_state:
    st.session_state.animation_running = False

# --- UI Sidebar ---
st.sidebar.title("Controls ⚙️")

# Maze Generation Controls
st.sidebar.subheader("Maze Settings")
width = st.sidebar.slider("Maze Width", min_value=9, max_value=41, value=25, step=2)
height = st.sidebar.slider("Maze Height", min_value=9, max_value=31, value=15, step=2)

if st.sidebar.button("Generate New Maze 🎲", type="primary"):
    grid, start, end = generate_maze(width, height)
    st.session_state.grid = grid
    st.session_state.start_pos = start
    st.session_state.end_pos = end
    st.session_state.maze_generated = True
    st.session_state.visited_order = []
    st.session_state.final_path = []
    st.session_state.algo_stats = None

st.sidebar.markdown("---")

# Algorithm Controls
st.sidebar.subheader("Algorithm")
algorithm = st.sidebar.selectbox("Select Search Algorithm", ["Breadth-First Search (BFS)", "Depth-First Search (DFS)"])

speed_label = st.sidebar.select_slider("Animation Speed", options=["Slow", "Medium", "Fast", "Instant"], value="Medium")
speed_map = {"Slow": 0.1, "Medium": 0.03, "Fast": 0.005, "Instant": 0.0}
animation_delay = speed_map[speed_label]

start_solve = st.sidebar.button("Solve Maze 🚀")

st.sidebar.markdown("---")
st.sidebar.info("This is a Project Based Learning (PBL) application. See the 'Educational Demo' tab below for theory and Viva prep.")

# --- Main Page Layout ---
st.title("🧠 Intelligent Maze Solver")
st.markdown("**Pathfinding using BFS & DFS** • A visual demonstration of graph search algorithms.")

# Create tabs
tab_visualizer, tab_compare, tab_theory = st.tabs(["Maze Visualizer 🎮", "Statistics 📊", "Educational Demo & Viva Prep 📚"])

with tab_visualizer:
    if not st.session_state.maze_generated:
        st.info("👈 Please generate a maze from the sidebar to begin!")
    else:
        # Placeholder for maze
        maze_placeholder = st.empty()
        
        if not start_solve:
            # Render initial maze
            maze_placeholder.markdown(render_maze(st.session_state.grid), unsafe_allow_html=True)
            
        if start_solve:
            if algorithm == "Breadth-First Search (BFS)":
                algo_func = solve_bfs
                algo_name = "BFS"
            else:
                algo_func = solve_dfs
                algo_name = "DFS"
                
            with st.spinner(f"Running {algo_name}..."):
                start_time = time.time()
                visited_order, final_path = algo_func(st.session_state.grid, st.session_state.start_pos, st.session_state.end_pos)
                execution_time = time.time() - start_time
                
            # Stats recording
            st.session_state.algo_stats = {
                "Algorithm": algo_name,
                "Nodes Explored": len(visited_order),
                "Path Length": len(final_path),
                "Execution Time (s)": round(execution_time, 5),
                "Destination Reached": len(final_path) > 0
            }
            
            # Animation
            visited_set = set()
            path_set = set()
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            if animation_delay > 0:
                total_steps = len(visited_order)
                for i, pos in enumerate(visited_order):
                    visited_set.add(pos)
                    # Every N steps, update to avoid browser lag, unless slow
                    if speed_label == "Fast" and i % 5 != 0 and i != total_steps - 1:
                        pass
                    else:
                        maze_placeholder.markdown(render_maze(st.session_state.grid, visited_set, path_set, current=pos), unsafe_allow_html=True)
                        time.sleep(animation_delay)
                    
                    status_text.text(f"Exploring... {i+1}/{total_steps} cells visited.")
                    progress_bar.progress((i + 1) / total_steps)
            else:
                # Instant fill
                visited_set = set(visited_order)
            
            # Show final path
            path_set = set(final_path)
            maze_placeholder.markdown(render_maze(st.session_state.grid, visited_set, path_set), unsafe_allow_html=True)
            status_text.text(f"Solve complete! Found path length: {len(final_path)}")
            progress_bar.progress(1.0)
            
            st.success(f"Algorithm finished. Switch to the Statistics tab for details.")

with tab_compare:
    st.header("Algorithm Statistics")
    if 'algo_stats' in st.session_state and st.session_state.algo_stats is not None:
        stats = st.session_state.algo_stats
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Algorithm", stats["Algorithm"])
        col2.metric("Cells Explored", stats["Nodes Explored"])
        col3.metric("Path Length", stats["Path Length"])
        
        # Color coding success
        success_color = "green" if stats["Destination Reached"] else "red"
        col4.markdown(f"Status: **<span style='color:{success_color}'>{'Success' if stats['Destination Reached'] else 'Failed'}</span>**", unsafe_allow_html=True)
        
        st.markdown(f"**Execution Time (Backend Logic):** {stats['Execution Time (s)']} seconds")
        
        st.info("💡 **Tip:** Generate a new maze and try running the *other* algorithm at 'Instant' speed to compare how many cells each algorithm explores on the exact same map!")
        
        st.markdown("""
        ### Performance Insights:
        * **BFS (Breadth-First Search):** Explores all cells at distance $k$ before distance $k+1$. It usually explores *more* cells but **guarantees the shortest path**.
        * **DFS (Depth-First Search):** Explores deeply down one path before backtracking. It sometimes finds *a* path very quickly if it gets lucky, but it **does not guarantee the shortest path**, often producing a very winding and long route.
        """)
    else:
        st.info("Run an algorithm on the Maze Visualizer tab to see statistics here.")

with tab_theory:
    st.header("📚 PBL Project Theory & Presentation")
    
    st.markdown("### What is a Graph in this context?")
    st.write("""
    A maze is a 2D grid, but in AI, we treat it as an unweighted graph. 
    Every open cell is a 'Node' (or Vertex), and we can move to the open cells (Up, Down, Left, Right). 
    These valid moves form the 'Edges' connecting the nodes. Pathfinding is simply searching this graph for a route from the Start node to the Destination node.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔵 Breadth-First Search (BFS)")
        st.markdown("""
        **What it is:** BFS is an algorithm that searches level-by-level outward from the starting point.
        
        **How it works (Data Structure):** It uses a **Queue (FIFO - First In, First Out)**. 
        It looks at all neighbors, adds them to the queue, and then evaluates them in the exact order they were discovered.
        
        **Advantages:** 
        * In an unweighted graph (like our maze grid), BFS is mathematically guaranteed to find the shortest possible path.
        
        **Complexity:** 
        * **Time:** O(V + E) where V is vertices (cells) and E is edges. In worst case it visits every open cell.
        * **Space:** O(V) for the visited list and the Queue.
        """)

    with col2:
        st.markdown("### 🔴 Depth-First Search (DFS)")
        st.markdown("""
        **What it is:** DFS is an algorithm that goes as deep as possible down a single path until it hits a dead-end, then it backtracks.
        
        **How it works (Data Structure):** It uses a **Stack (LIFO - Last In, First Out)**, or recursion.
        It looks at a neighbor, immediately goes to that neighbor, and keeps going until it can't.
        
        **Disadvantages:** 
        * It is NOT guaranteed to find the shortest path. It just finds the *first* path it stumbles upon.
        
        **Complexity:** 
        * **Time:** O(V + E). It might visit every cell in the worst case (like a maze with no solution).
        * **Space:** O(V) for the Stack memory (or recursion call stack).
        """)
        
    st.divider()
    
    st.markdown("### 🗣️ Common Viva Questions")
    with st.expander("Q1: Which algorithm gives the shortest path and why?"):
        st.write("BFS always provides the shortest path in an unweighted grid because it naturally explores all paths of length 1, then length 2, and so on. The first time it touches the destination, it must be via the shortest possible sequence of moves.")
    with st.expander("Q2: Why does BFS use a Queue while DFS uses a Stack?"):
        st.write("BFS needs a Queue (First In First Out) to enforce fairness—exploring nodes in the exact order they were discovered. DFS needs a Stack (Last In First Out) to prioritize the most recently discovered nodes, pushing it to explore deeper immediately rather than exploring sideways.")
    with st.expander("Q3: Does DFS have any advantages over BFS?"):
        st.write("Yes. In scenarios like puzzle solving (e.g. Sudoku or a maze) where there is only one solution deep inside a massive tree, DFS uses less memory space (the depth of the tree) compared to BFS (which stores the entire incredibly wide level).")
    with st.expander("Q4: What happens if there is no path (unsolvable maze)?"):
        st.write("Both algorithms will systematically explore every single accessible cell. Because they maintain a 'Visited' set, they won't get stuck in an infinite loop. Once the Queue (BFS) or Stack (DFS) is empty, they terminate and report failure safely.")
    with st.expander("Q5: How did you implement animation?"):
        st.write("The backend algorithm fully solves the maze instantly and records the `visited_order`. The Streamlit frontend then loops through this order list, injecting time delays (`time.sleep`) and rendering partial HTML grids to create a visual animation.")
