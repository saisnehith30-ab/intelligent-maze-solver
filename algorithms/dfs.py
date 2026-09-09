def solve_dfs(grid, start, end):
    """
    Depth-First Search algorithm to solve a maze.
    Returns a tuple: (visited_order, final_path)
    visited_order: list of coordinates in the order they were visited
    final_path: list of coordinates representing the path from start to end
    """
    rows, cols = len(grid), len(grid[0])
    
    # Stack stores tuples of (current_position, path_taken_so_far)
    stack = []
    stack.append((start, [start]))
    
    visited = set()
    visited_order = []
    
    # Directions: Up, Right, Down, Left
    # The order of directions can affect which way DFS goes first.
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    while stack:
        current_pos, path = stack.pop()
        
        # In DFS we mark as visited when we pop, or we can mark it when we push.
        # Marking when popping allows us to see back-tracking if we revisit,
        # but to prevent infinite loops, checking if it's in visited is crucial.
        if current_pos in visited:
            continue
            
        visited.add(current_pos)
        visited_order.append(current_pos)
        
        # If we reach the destination, we are done
        if current_pos == end:
            return visited_order, path
            
        r, c = current_pos
        
        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check boundaries, valid path, and not already visited
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] != 1:
                # We push the neighbor onto the stack
                stack.append(((nr, nc), path + [(nr, nc)]))
                
    # If stack is empty and no path found
    return visited_order, []
