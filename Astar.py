import Grid

def manhattan_distance(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return abs(dx) + abs(dy)


def find_lowest_F(list):
    lowest_value = list[0][3]
    lowest_index = 0

    for index, value in enumerate(list):
        if value[3] < lowest_value:
            lowest_value = value[3]
            lowest_index = index

    return lowest_index


def get_neighbors_informations(maze, current, useless_neighbors):
    # Get raw neighbors
    neighbors_without_info = maze.getNeighbors(current[0], current[1])

    # Get neighbors coordinates and cases types
    neighbors_with_uselees = []  # [x, y, case_type]
    for neighbor in neighbors_without_info:
        neighbors_with_uselees.append([neighbor[0], neighbor[1], maze.getCase(neighbor[0], neighbor[1])])

    # Remove useless neighbors
    neighbors = []
    for neighbor in neighbors_with_uselees:
        if not neighbor[2] in useless_neighbors:
            neighbors.append(neighbor)

    # [x, y, case_type]
    return neighbors


def is_in_list(list, to_find):
    for index, value in enumerate(list):
        if (to_find[0], to_find[1]) == (value[0], value[1]):
            return index
    return False


def solve(gridobjoriginal: Grid, step_by_step = False):
    gridobj = gridobjoriginal.copy()

    start = gridobj.findCase('start')
    end = gridobj.findCase('end')

    # Get useless neighbors (get their number)
    useless_neighbors = ["Indescructible wall", "visited cell", "path cell", "wall", "current cell", "start"]
    for key in useless_neighbors:
        useless_neighbors[useless_neighbors.index(key)] = gridobj.possible_cases[key]

    start = start + (gridobj.possible_cases['start'], 0, 0, 0, None)
    open_list = [start]
    closed_list = []

    is_searching = True
    while is_searching:
        if not open_list:
            return None, gridobj
        current_index = find_lowest_F(open_list)
        current = open_list.pop(current_index)

        # Check if current is end

        if (current[0], current[1]) == end:
            open_list = [current]
            break

        closed_list.append(current)

        neighbors = get_neighbors_informations(gridobj, current, useless_neighbors)
        for neighbor in neighbors:
            # Already evaluated
            if is_in_list(closed_list, neighbor) != False:
                continue
            G = current[5] + 1
            H = manhattan_distance(neighbor, end)
            F = G + H  # Total cost

            # Check if the neighbor is in open_list and if it has a higher G value
            neighbor_index = is_in_list(open_list, neighbor)
            if neighbor_index != False and open_list[neighbor_index][5] <= G:
                continue  # This is not a better path

            # Update neighbor with new values and parent
            neighbor_updated = [neighbor[0], neighbor[1], neighbor[2], F, H, G, (current[0], current[1])]
            if neighbor_index == False:
                open_list.append(neighbor_updated)  # Add new neighbor
            else:
                open_list[neighbor_index] = neighbor_updated  # Update existing neighbor in open_list

            # Mark as visited
            gridobj.setCase(neighbor[0], neighbor[1], "visited cell")


    if not open_list:
        return None, gridobj

    else:
        # The goal is reached; backtrack to find the path
        gridobj.setCase(current[0], current[1], 'end') # End is delete before so we reput it
        path = [(current[0], current[1])]
        current = closed_list[-1]  # Start backtracking from the goal

        while current[6] is not None:  # Check if current node has a parent
            path.append((current[0], current[1]))
            parent_coords = current[6]
            # Find the parent in the closed list
            for node in closed_list:
                if (node[0], node[1]) == parent_coords:
                    current = node
                    break
        path.append((start[0], start[1]))  # Add the start position to the path
        path.reverse()  # Reverse the path to start from the beginning

        # Mark the path in the maze
        for coords in path:
            if gridobj.getCase(coords[0], coords[1]) not in [gridobj.possible_cases['start'], gridobj.possible_cases['end']]:
                gridobj.setCase(coords[0], coords[1], 'path cell')

    return path, gridobj
