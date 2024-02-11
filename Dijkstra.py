import heapq
import Grid

def dijkstra(graph, start):
    shortest_paths = {vertex: float('infinity') for vertex in graph}
    shortest_paths[start] = 0
    previous_nodes = {vertex: None for vertex in graph}
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < shortest_paths[neighbor]:
                shortest_paths[neighbor] = distance
                previous_nodes[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    return shortest_paths, previous_nodes

def reconstruct_path(previous_nodes, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = previous_nodes[current]
        if current is None:  # Goal is not reachable from start
            return None
    path.append(start)  # optional: include start node
    path.reverse()  # reverse the path to get the correct order
    return path

def maze_to_graph(maze):
    rows, cols = len(maze), len(maze[0])
    graph = {}

    for y in range(cols):
        for x in range(rows):
            if maze[x][y] != 1:
                if (y, x) not in graph:
                    graph[(y, x)] = {}
                for dy, dx in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1:
                        graph[(y, x)][(ny, nx)] = 1
    return graph


def solve(gridobjoriginal: Grid, step_by_step=False):
    gridobj = gridobjoriginal.copy()

    start = gridobj.findCase('start')
    end = gridobj.findCase('end')

    # Convert maze to graph
    graph = maze_to_graph(gridobj.grid)

    # Run Dijkstra's algorithm
    shortest_paths, previous_nodes = dijkstra(graph, start)

    # Reconstruct the shortest path from start to goal
    path = reconstruct_path(previous_nodes, start, end)

    return path