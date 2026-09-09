from collections import deque

def solve_bfs(grid, start, end):
    """
    Breadth-First Search algorithm to solve a maze.
    Returns a tuple: (visited_order, final_path)
    visited_order: list of coordinates in the order they were visited
    final_path: list of coordinates representing the shortest path from start to end
    """
    rows, cols = len(grid), len(grid[0])
    
    # Queue stores tuples of (current_position, path_taken_so_far)
    # Using collections.deque because it has O(1) append and popleft operations
    queue = deque()
    queue.append((start, [start]))
    
    visited = set()
    visited.add(start)
    
    visited_order = []
    
    # Directions: Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        current_pos, path = queue.popleft()
        visited_order.append(current_pos)
        
        # If we reach the destination, we are done
        if current_pos == end:
            return visited_order, path
            
        r, c = current_pos
        
        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check boundaries and if it's a valid path (not a wall)
            # grid[nr][nc] != 1 means it's not a wall (0=path, 2=start, 3=end)
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] != 1:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
                
    # If queue is empty without reaching the end, no path exists
    return visited_order, []
