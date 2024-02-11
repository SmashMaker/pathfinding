import Grid
import heapq

def manhattan_distance(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return abs(dx) + abs(dy)

def get_neighbors_informations(maze, current, useless_neighbors):
    # Get raw neighbors
    neighbors_without_info = maze.getNeighbors(current[0], current[1])

    # Get neighbors coordinates and cases types
    neighbors_with_useless = []  # [x, y, case_type]
    for neighbor in neighbors_without_info:
        neighbors_with_useless.append([neighbor[0], neighbor[1], maze.getCase(neighbor[0], neighbor[1])])

    # Remove useless neighbors
    neighbors = []
    for neighbor in neighbors_with_useless:
        if not neighbor[2] in useless_neighbors:
            neighbors.append(neighbor)

    return neighbors

def is_in_list(list, to_find):
    for index, value in enumerate(list):
        if (to_find[0], to_find[1]) == (value[1][0], value[1][1]):
            return index
    return -1  # Return -1 if not found

def solve(gridobjoriginal: Grid, step_by_step=False):
    gridobj = gridobjoriginal.copy()

    start = gridobj.findCase('start')
    end = gridobj.findCase('end')

    # Get useless neighbors (get their number)
    useless_neighbors = [gridobj.possible_cases[key] for key in ["Indestructible wall", "visited cell", "path cell", "wall", "current cell", "start"]]

    start_node = (manhattan_distance(start, end), start + (gridobj.possible_cases['start'], 0, manhattan_distance(start, end), 0, None))  # (F, (x, y, type, F, H, G, parent))

    open_list = []
    heapq.heappush(open_list, start_node)
    closed_set = set()

    while open_list:
        current_F, current = heapq.heappop(open_list)
        closed_set.add((current[0], current[1]))

        # Check if current is end
        if (current[0], current[1]) == end:
            path = []
            while current[6] is not None:
                path.append((current[0], current[1]))
                current = current[6]
            path.append((start[0], start[1]))
            path.reverse()
            for coords in path:
                if coords not in [start, end]:
                    gridobj.setCase(coords[0], coords[1], 'path cell')
            return path, gridobj

        neighbors = get_neighbors_informations(gridobj, current, useless_neighbors)
        for neighbor in neighbors:
            if (neighbor[0], neighbor[1]) in closed_set:
                continue
            neighbor_pos = (neighbor[0], neighbor[1])
            G = current[5] + 1
            H = manhattan_distance(neighbor_pos, end)
            F = G + H
            if not any((neighbor_pos == (n[1][0], n[1][1]) and G < n[1][5]) for n in open_list):
                neighbor_updated = (neighbor[0], neighbor[1], neighbor[2], F, H, G, current)
                heapq.heappush(open_list, (F, neighbor_updated))
                gridobj.setCase(neighbor[0], neighbor[1], "visited cell")

    return None, gridobj  # No path found