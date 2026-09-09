import random

def generate_maze(width, height, wall_prob=0.3):
    """
    Generates a maze represented as a 2D grid.
    0 = Open path
    1 = Wall
    2 = Start
    3 = Destination
    """
    # Initialize with walls (1)
    grid = [[1 for _ in range(width)] for _ in range(height)]
    
    # Simple randomized DFS algorithm to generate a solvable maze (carving paths)
    def carve_passages_from(c_r, c_c):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        for dr, dc in directions:
            nr, nc = c_r + dr*2, c_c + dc*2
            
            if 0 <= nr < height and 0 <= nc < width and grid[nr][nc] == 1:
                grid[c_r + dr][c_c + dc] = 0
                grid[nr][nc] = 0
                carve_passages_from(nr, nc)
                
    # Start carving from (1, 1) to make sure there's an outer wall if we want, 
    # but for simplicity, let's just create a completely random grid with a guaranteed path?
    # Actually, a purely random grid with wall_prob is easier for students to understand.
    # Wait, the user asked for a generated maze that is solvable, or at least mostly solvable.
    # A true maze generation algorithm (like Randomized DFS carving) creates perfect mazes. Let's do that.
    
    # First, make everything a wall
    grid = [[1 for _ in range(width)] for _ in range(height)]
    
    # Force width and height to be odd for standard maze generation
    # if width % 2 == 0: width += 1
    # if height % 2 == 0: height += 1
    
    start_r, start_c = 1, 1
    if height > 2 and width > 2:
        grid[start_r][start_c] = 0
        carve_passages_from(start_r, start_c)
    
    # After carving, we might want to punch some random holes to create multiple paths
    # Because standard carved mazes only have one path (perfect maze), which makes BFS and DFS find the same path length usually.
    # By punching holes, we create cycles, making BFS and DFS behave differently! Let's do that.
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            if grid[r][c] == 1 and random.random() < 0.1: # 10% chance to break a wall
                grid[r][c] = 0
                
    # Ensure start and end are placed in open cells
    start_r, start_c = 1, 1
    end_r, end_c = height - 2, width - 2
    
    # If the maze is too small, fallback gracefully
    if height <= 2 or width <= 2:
        grid = [[0 for _ in range(width)] for _ in range(height)]
        start_r, start_c = 0, 0
        end_r, end_c = height - 1, width - 1

    # Ensure start and end are open
    grid[start_r][start_c] = 2 # Start
    grid[end_r][end_c] = 3 # Destination
    
    # Also ensure there's at least a 1-cell radius opening around them so it's clearly visible
    for dr, dc in [(0,1), (1,0)]:
        if start_r + dr < height and start_c + dc < width:
            grid[start_r + dr][start_c + dc] = 0
    for dr, dc in [(0,-1), (-1,0)]:
        if end_r + dr >= 0 and end_c + dc >= 0:
            grid[end_r + dr][end_c + dc] = 0
            
    # Set them back to 2 and 3 just in case they were overwritten
    grid[start_r][start_c] = 2 
    grid[end_r][end_c] = 3
    
    return grid, (start_r, start_c), (end_r, end_c)
