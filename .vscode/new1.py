from collections import deque  


GOAL_STATE = [
    [1, 2, 3],[4, 5, 6],[7, 8, 0]  
]


DIRECTIONS = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}


def is_goal(state):
    return state == GOAL_STATE


def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j 


def move(state, direction):
    r, c = find_zero(state)  
    dr, dc = DIRECTIONS[direction]  
    new_r, new_c = r + dr, c + dc  

    
    if 0 <= new_r < 3 and 0 <= new_c < 3:
        new_state = [row[:] for row in state]          
        new_state[r][c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[r][c]
        return new_state 
    return None 


def serialize(state):
    return tuple(tuple(row) for row in state) 


def bfs(start_state):
    queue = deque()  
    visited = set()  
    parent_map = {}  

    
    queue.append((start_state, [])) 
    visited.add(serialize(start_state)) 
    
    while queue:
        current_state, path = queue.popleft()  

        if is_goal(current_state):
            return path 

    
        for direction in DIRECTIONS:
            next_state = move(current_state, direction) 
            if next_state and serialize(next_state) not in visited:
                visited.add(serialize(next_state))  
                queue.append((next_state, path + [direction]))  

    return None 

initial_state = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
]

solution = bfs(initial_state)
if solution:
    print("Solution found in", len(solution), "moves:", solution)
else:
    print("No solution found.")