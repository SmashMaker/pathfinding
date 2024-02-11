import random

def manhattan_distance(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return abs(dx) + abs(dy)

def is_not_around_another_room(room, rooms_positions, size_rooms):
    for i in range(len(rooms_positions)):
        if manhattan_distance(room, rooms_positions[i]) < (size_rooms[i][0] + size_rooms[i][1])/2:
            return False
    return True

def connect_rooms(close_space, room1, room2, passage_width=2):
    x1, y1 = room1
    x2, y2 = room2

    # Trace the diagonal between the two rooms
    while True:
        if x1 < x2:
            x1 += 1
        elif x1 > x2:
            x1 -= 1
        for i in range(passage_width):
            if close_space[y1 + i][x1] == 1:
                close_space[y1 + i][x1] = 0
            if close_space[y1 - i][x1] == 1:
                close_space[y1 - i][x1] = 0

        if y1 < y2:
            y1 += 1
        elif y1 > y2:
            y1 -= 1
        for i in range(passage_width):
            if close_space[y1][x1 + i] == 1:
                close_space[y1][x1 + i] = 0
            if close_space[y1][x1 - i] == 1:
                close_space[y1][x1 - i] = 0

        if (x1, y1) == room2:
            break

def create_close_space(width, height):
    # Create a 2D array of width x height
    close_space = [[1 for i in range(width)] for j in range(height)]

    # Add Indescructible walls
    for i in range(width):
        close_space[0][i] = -1
        close_space[height-1][i] = -1
    for i in range(height):
        close_space[i][0] = -1
        close_space[i][width-1] = -1

    # Add start and end
    while True:
        start = (random.randint(1, width-2), random.randint(1, height-2))
        end = (random.randint(1, width-2), random.randint(1, height-2))
        if start != end:
            if manhattan_distance(start, end) > (width+height)/2:
                break
    close_space[start[1]][start[0]] = 2
    close_space[end[1]][end[0]] = 3

    # Add rooms around the start and end
    for i in range(3):
        for j in range(3):
            # Check if the space is not already taken by an indescructible wall
            if close_space[start[1]-1+i][start[0]-1+j] == 1:
                close_space[start[1]-1+i][start[0]-1+j] = 0
            if close_space[end[1]-1+i][end[0]-1+j] == 1:
                close_space[end[1]-1+i][end[0]-1+j] = 0

    # Add random rooms
    nb_rooms = random.randint(int((width + height)/8), int((width + height)/4))
    rooms_positions = [start, end]
    size_rooms = [(3, 3), (3, 3)]

    for i in range(nb_rooms):
        while True:
            room = (random.randint(1, width-2), random.randint(1, height-2))
            if manhattan_distance(start, room) > (width+height)/6:
                if manhattan_distance(end, room) > (width+height)/6:
                    if is_not_around_another_room(room, rooms_positions, size_rooms):
                        break
        close_space[room[1]][room[0]] = 0
        rooms_positions.append(room)
        size_rooms.append((random.randint(2, 4), random.randint(2, 4)))

    # Improve the size of the rooms
    for i in range(2,len(rooms_positions)):
        for j in range(size_rooms[i][0]):
            for k in range(size_rooms[i][1]):
                if rooms_positions[i][0] + j < width-1 and rooms_positions[i][1] + k < height-1:
                    close_space[rooms_positions[i][1] + k][rooms_positions[i][0] + j] = 0
                if rooms_positions[i][0] - j > 0 and rooms_positions[i][1] - k > 0:
                    close_space[rooms_positions[i][1] - k][rooms_positions[i][0] - j] = 0

    # Put the end room at the end of the list
    end_index = rooms_positions.index(end)
    rooms_positions.pop(end_index)
    rooms_positions.append(end)

    # Connect random rooms from the list
    for i in range(len(rooms_positions)-1):
        connect_rooms(close_space, rooms_positions[i], rooms_positions[i+1])

    # Replace umbreakable walls by normal walls
    for i in range(width):
        for j in range(height):
            if close_space[j][i] == -1:
                close_space[j][i] = 1

    return close_space