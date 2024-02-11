import random

def manhattan_distance(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return abs(dx) + abs(dy)

def create_open_space(width, height):
    # Create a 2D array of width x height
    open_space = [[0 for i in range(width)] for j in range(height)]

    # Add walls
    for i in range(width):
        open_space[0][i] = 1
        open_space[height-1][i] = 1
    for i in range(height):
        open_space[i][0] = 1
        open_space[i][width-1] = 1

    # Add start and end
    while True:
        start = (random.randint(1, width-2), random.randint(1, height-2))
        end = (random.randint(1, width-2), random.randint(1, height-2))
        if start != end:
            if manhattan_distance(start, end) > (width+height)/2:
                break
    open_space[start[1]][start[0]] = 2
    open_space[end[1]][end[0]] = 3

    # Add random obstacles
    nb_obstacles = random.randint(0, width+height)
    obstacles_positions = []

    for i in range(nb_obstacles):
        while True:
            obstacle = (random.randint(1, width-2), random.randint(1, height-2))
            if obstacle != start and obstacle != end:
                break
        open_space[obstacle[1]][obstacle[0]] = 1
        obstacles_positions.append(obstacle)

    # Improve the size of the obstacles
    for obstacle in obstacles_positions:
        if random.randint(0, 1):
            for i in range(random.randint(1, 3)):
                if obstacle[0]+i < width-1:
                    if open_space[obstacle[1]][obstacle[0]+i] == 0:
                        open_space[obstacle[1]][obstacle[0]+i] = 1
                if obstacle[0]-i > 0:
                    if open_space[obstacle[1]][obstacle[0]-i] == 0:
                        open_space[obstacle[1]][obstacle[0]-i] = 1
        else:
            for i in range(random.randint(1, 3)):
                if obstacle[1]+i < height-1:
                    if open_space[obstacle[1]+i][obstacle[0]] == 0:
                        open_space[obstacle[1]+i][obstacle[0]] = 1
                if obstacle[1]-i > 0:
                    if open_space[obstacle[1]-i][obstacle[0]] == 0:
                        open_space[obstacle[1]-i][obstacle[0]] = 1

    return open_space