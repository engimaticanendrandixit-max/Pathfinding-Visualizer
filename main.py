import pygame
import sys
import time
import heapq
from collections import deque

# ===================== CONFIG =====================
ROWS, COLS = 25, 45
CELL_SIZE = 24
GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE
TOPBAR_HEIGHT = 60
STATSBAR_HEIGHT = 34
WINDOW_WIDTH = GRID_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT + TOPBAR_HEIGHT + STATSBAR_HEIGHT

# ===================== COLORS =====================
BG = (15, 17, 21)
PANEL = (23, 26, 33)
GRID_LINE = (38, 43, 54)
EMPTY = (23, 26, 33)
WALL = (42, 47, 58)
START = (79, 209, 197)
END = (255, 107, 107)
WEIGHT = (245, 166, 35)
VISITED = (63, 127, 219)
PATH = (255, 224, 102)
TEXT = (231, 233, 238)
TEXT_DIM = (138, 144, 162)
BTN_ACTIVE = (43, 107, 100)

# ===================== CELL STATES =====================
EMPTY_S, WALL_S, START_S, END_S, WEIGHT_S, VISITED_S, PATH_S = (
    'empty', 'wall', 'start', 'end', 'weight', 'visited', 'path'
)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pathfinder Visualizer")
font = pygame.font.SysFont("segoeui", 16)
font_bold = pygame.font.SysFont("segoeui", 18, bold=True)
clock = pygame.time.Clock()

# ===================== STATE =====================
grid = [[EMPTY_S for _ in range(COLS)] for _ in range(ROWS)]
start_pos = (ROWS // 2, 8)
end_pos = (ROWS // 2, COLS - 9)
grid[start_pos[0]][start_pos[1]] = START_S
grid[end_pos[0]][end_pos[1]] = END_S

current_mode = 'wall'   # 'wall' | 'start' | 'end' | 'weight'
mouse_down = False
mouse_button = None     # 1 = left (draw), 3 = right (erase)

# Animation / algorithm state
algo_gen = None          # active generator, or None if idle
animating = False
steps_per_frame = 4      # visualization speed (higher = faster)
stats = {'visited': 0, 'path_len': 0, 'time_ms': 0, 'status': 'Ready'}
selected_algo = 'bfs'    # 'bfs' | 'dfs' | 'dijkstra' | 'astar'
ALGO_NAMES = {'bfs': 'BFS', 'dfs': 'DFS', 'dijkstra': 'Dijkstra', 'astar': 'A*'}
ALGO_KEYS = ['bfs', 'dfs', 'dijkstra', 'astar']  # order for cycling with Tab
WEIGHT_COST = 5  # cost of stepping onto a 'weight' cell (normal cell costs 1)

# Top bar buttons: (label, mode_key, rect) -- rects computed after layout
MODES = ['wall', 'start', 'end', 'weight']
mode_buttons = {}
visualize_button = pygame.Rect(0, 0, 110, 34)  # positioned in layout_buttons


def layout_buttons():
    global visualize_button
    x = 10
    y = 10
    h = 34
    for m in MODES:
        w = 70
        mode_buttons[m] = pygame.Rect(x, y, w, h)
        x += w + 6
    x += 16
    visualize_button = pygame.Rect(x, y, 110, h)


layout_buttons()


# ===================== HELPERS =====================
def draw_text(text, x, y, color=TEXT, bold=False):
    f = font_bold if bold else font
    surf = f.render(text, True, color)
    screen.blit(surf, (x, y))


def draw_topbar():
    pygame.draw.rect(screen, PANEL, (0, 0, WINDOW_WIDTH, TOPBAR_HEIGHT))
    pygame.draw.line(screen, GRID_LINE, (0, TOPBAR_HEIGHT), (WINDOW_WIDTH, TOPBAR_HEIGHT), 1)

    for m, rect in mode_buttons.items():
        active = (m == current_mode)
        color = BTN_ACTIVE if active else (29, 33, 43)
        pygame.draw.rect(screen, color, rect, border_radius=6)
        label = m.capitalize()
        text_surf = font.render(label, True, TEXT if active else TEXT_DIM)
        screen.blit(text_surf, (rect.x + (rect.w - text_surf.get_width()) // 2,
                                 rect.y + (rect.h - text_surf.get_height()) // 2))

    # Visualize button
    v_color = (90, 60, 20) if animating else BTN_ACTIVE
    pygame.draw.rect(screen, v_color, visualize_button, border_radius=6)
    label = "Running..." if animating else f"Visualize ({ALGO_NAMES[selected_algo]})"
    text_surf = font.render(label, True, TEXT)
    screen.blit(text_surf, (visualize_button.x + (visualize_button.w - text_surf.get_width()) // 2,
                             visualize_button.y + (visualize_button.h - text_surf.get_height()) // 2))

    # Hints on the right
    hint = "V = visualize | TAB = algo | 1-4 = mode | C = clear | R = maze | +/- = speed"
    hint_surf = font.render(hint, True, TEXT_DIM)
    screen.blit(hint_surf, (WINDOW_WIDTH - hint_surf.get_width() - 12,
                             (TOPBAR_HEIGHT - hint_surf.get_height()) // 2))


def draw_statsbar():
    y = TOPBAR_HEIGHT + GRID_HEIGHT
    pygame.draw.rect(screen, PANEL, (0, y, WINDOW_WIDTH, STATSBAR_HEIGHT))
    pygame.draw.line(screen, GRID_LINE, (0, y), (WINDOW_WIDTH, y), 1)

    text = f"Visited: {stats['visited']}    Path length: {stats['path_len']}    Time: {stats['time_ms']}ms    Speed: {steps_per_frame}x"
    draw_text(text, 12, y + 8, TEXT_DIM)

    status_surf = font.render(stats['status'], True, (79, 209, 197))
    screen.blit(status_surf, (WINDOW_WIDTH - status_surf.get_width() - 12, y + 8))


def cell_color(state):
    return {
        EMPTY_S: EMPTY,
        WALL_S: WALL,
        START_S: START,
        END_S: END,
        WEIGHT_S: WEIGHT,
        VISITED_S: VISITED,
        PATH_S: PATH,
    }[state]


def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL_SIZE
            y = TOPBAR_HEIGHT + r * CELL_SIZE
            pygame.draw.rect(screen, cell_color(grid[r][c]), (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRID_LINE, (x, y, CELL_SIZE, CELL_SIZE), 1)


def pixel_to_cell(pos):
    x, y = pos
    if y < TOPBAR_HEIGHT:
        return None
    col = x // CELL_SIZE
    row = (y - TOPBAR_HEIGHT) // CELL_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col
    return None


def apply_mode(row, col, erase=False):
    global start_pos, end_pos
    cell = grid[row][col]

    if current_mode == 'start':
        if (row, col) == end_pos:
            return
        old_r, old_c = start_pos
        grid[old_r][old_c] = EMPTY_S
        start_pos = (row, col)
        grid[row][col] = START_S
        return

    if current_mode == 'end':
        if (row, col) == start_pos:
            return
        old_r, old_c = end_pos
        grid[old_r][old_c] = EMPTY_S
        end_pos = (row, col)
        grid[row][col] = END_S
        return

    if (row, col) == start_pos or (row, col) == end_pos:
        return

    if current_mode == 'wall':
        grid[row][col] = EMPTY_S if erase else WALL_S
    elif current_mode == 'weight':
        grid[row][col] = EMPTY_S if erase else WEIGHT_S


def clear_board(keep_walls=False):
    global grid
    for r in range(ROWS):
        for c in range(COLS):
            if (r, c) == start_pos:
                grid[r][c] = START_S
            elif (r, c) == end_pos:
                grid[r][c] = END_S
            elif keep_walls and grid[r][c] in (WALL_S, WEIGHT_S):
                continue
            else:
                grid[r][c] = EMPTY_S


def random_maze():
    import random
    clear_board(keep_walls=False)
    for r in range(ROWS):
        for c in range(COLS):
            if (r, c) == start_pos or (r, c) == end_pos:
                continue
            if random.random() < 0.25:
                grid[r][c] = WALL_S


# ===================== ALGORITHMS =====================
def neighbors(row, col):
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = row + dr, col + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            yield nr, nc


def reset_for_run():
    """Clear any previous visited/path highlighting but keep walls/weights."""
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] in (VISITED_S, PATH_S):
                grid[r][c] = EMPTY_S
    stats['visited'] = 0
    stats['path_len'] = 0
    stats['time_ms'] = 0
    stats['status'] = 'Running...'


def bfs_generator():
    """Yields after every cell visited so the caller can animate frame-by-frame.
    On completion, paints the final path (if any) and yields once more per path cell."""
    start_time = time.time()
    queue = deque([start_pos])
    came_from = {start_pos: None}
    visited_count = 0

    while queue:
        current = queue.popleft()

        if current != start_pos and current != end_pos:
            grid[current[0]][current[1]] = VISITED_S
            visited_count += 1
            stats['visited'] = visited_count
            yield  # pause here so main loop can redraw

        if current == end_pos:
            break

        for n in neighbors(*current):
            if n in came_from:
                continue
            if grid[n[0]][n[1]] == WALL_S:
                continue
            came_from[n] = current
            queue.append(n)

    stats['time_ms'] = int((time.time() - start_time) * 1000)

    if end_pos not in came_from:
        stats['status'] = 'No path found'
        return

    # reconstruct path
    path = []
    node = end_pos
    while node != start_pos:
        node = came_from[node]
        if node != start_pos:
            path.append(node)
    path.reverse()

    for (r, c) in path:
        grid[r][c] = PATH_S
        stats['path_len'] += 1
        yield

    stats['status'] = 'Done'


def dfs_generator():
    """Iterative DFS using an explicit stack. Explores one direction deeply
    before backtracking -- unlike BFS it does NOT guarantee the shortest path."""
    start_time = time.time()
    stack = [start_pos]
    came_from = {start_pos: None}
    visited_count = 0
    visited_set = {start_pos}

    while stack:
        current = stack.pop()

        if current != start_pos and current != end_pos:
            grid[current[0]][current[1]] = VISITED_S
            visited_count += 1
            stats['visited'] = visited_count
            yield

        if current == end_pos:
            break

        for n in neighbors(*current):
            if n in visited_set:
                continue
            if grid[n[0]][n[1]] == WALL_S:
                continue
            visited_set.add(n)
            came_from[n] = current
            stack.append(n)

    stats['time_ms'] = int((time.time() - start_time) * 1000)

    if end_pos not in came_from:
        stats['status'] = 'No path found'
        return

    path = []
    node = end_pos
    while node != start_pos:
        node = came_from[node]
        if node != start_pos:
            path.append(node)
    path.reverse()

    for (r, c) in path:
        grid[r][c] = PATH_S
        stats['path_len'] += 1
        yield

    stats['status'] = 'Done'


def dijkstra_generator():
    """Uses a min-heap priority queue keyed by total cost from start.
    Weight cells cost WEIGHT_COST to step onto, normal cells cost 1 --
    this is what makes Dijkstra route around 'expensive' cells."""
    start_time = time.time()
    dist = {start_pos: 0}
    came_from = {start_pos: None}
    visited = set()
    heap = [(0, start_pos)]
    visited_count = 0

    while heap:
        cost, current = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)

        if current != start_pos and current != end_pos:
            grid[current[0]][current[1]] = VISITED_S
            visited_count += 1
            stats['visited'] = visited_count
            yield

        if current == end_pos:
            break

        for n in neighbors(*current):
            if grid[n[0]][n[1]] == WALL_S or n in visited:
                continue
            step_cost = WEIGHT_COST if grid[n[0]][n[1]] == WEIGHT_S else 1
            new_cost = cost + step_cost
            if n not in dist or new_cost < dist[n]:
                dist[n] = new_cost
                came_from[n] = current
                heapq.heappush(heap, (new_cost, n))

    stats['time_ms'] = int((time.time() - start_time) * 1000)

    if end_pos not in came_from:
        stats['status'] = 'No path found'
        return

    path = []
    node = end_pos
    while node != start_pos:
        node = came_from[node]
        if node != start_pos:
            path.append(node)
    path.reverse()

    for (r, c) in path:
        grid[r][c] = PATH_S
        stats['path_len'] += 1
        yield

    stats['status'] = 'Done'


def heuristic(a, b):
    """Manhattan distance -- admissible for a 4-directional grid."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_generator():
    """Like Dijkstra, but the priority queue is ordered by (cost-so-far + estimated
    cost-to-goal) instead of just cost-so-far. The heuristic pulls the search
    toward the end node, so far fewer cells get explored."""
    start_time = time.time()
    g_score = {start_pos: 0}
    came_from = {start_pos: None}
    visited = set()
    heap = [(heuristic(start_pos, end_pos), start_pos)]
    visited_count = 0

    while heap:
        _, current = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)

        if current != start_pos and current != end_pos:
            grid[current[0]][current[1]] = VISITED_S
            visited_count += 1
            stats['visited'] = visited_count
            yield

        if current == end_pos:
            break

        for n in neighbors(*current):
            if grid[n[0]][n[1]] == WALL_S or n in visited:
                continue
            step_cost = WEIGHT_COST if grid[n[0]][n[1]] == WEIGHT_S else 1
            new_g = g_score[current] + step_cost
            if n not in g_score or new_g < g_score[n]:
                g_score[n] = new_g
                came_from[n] = current
                f_score = new_g + heuristic(n, end_pos)
                heapq.heappush(heap, (f_score, n))

    stats['time_ms'] = int((time.time() - start_time) * 1000)

    if end_pos not in came_from:
        stats['status'] = 'No path found'
        return

    path = []
    node = end_pos
    while node != start_pos:
        node = came_from[node]
        if node != start_pos:
            path.append(node)
    path.reverse()

    for (r, c) in path:
        grid[r][c] = PATH_S
        stats['path_len'] += 1
        yield

    stats['status'] = 'Done'


# ===================== MAIN LOOP =====================
def start_visualization():
    global algo_gen, animating
    if animating:
        return
    reset_for_run()
    if selected_algo == 'bfs':
        algo_gen = bfs_generator()
    elif selected_algo == 'dfs':
        algo_gen = dfs_generator()
    elif selected_algo == 'dijkstra':
        algo_gen = dijkstra_generator()
    elif selected_algo == 'astar':
        algo_gen = astar_generator()
    animating = True


def main():
    global current_mode, mouse_down, mouse_button, algo_gen, animating, steps_per_frame, selected_algo

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if animating:
                    continue  # ignore board edits while an algorithm is running
                mouse_down = True
                mouse_button = event.button
                cell = pixel_to_cell(event.pos)
                if cell:
                    apply_mode(*cell, erase=(event.button == 3))
                elif event.pos[1] < TOPBAR_HEIGHT:
                    if visualize_button.collidepoint(event.pos):
                        start_visualization()
                    for m, rect in mode_buttons.items():
                        if rect.collidepoint(event.pos):
                            current_mode = m

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                mouse_button = None

            elif event.type == pygame.MOUSEMOTION and mouse_down and not animating:
                if current_mode in ('wall', 'weight'):
                    cell = pixel_to_cell(event.pos)
                    if cell:
                        apply_mode(*cell, erase=(mouse_button == 3))

            elif event.type == pygame.KEYDOWN:
                if animating and event.key not in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_MINUS):
                    continue  # only allow speed changes mid-run
                if event.key == pygame.K_1:
                    current_mode = 'wall'
                elif event.key == pygame.K_2:
                    current_mode = 'start'
                elif event.key == pygame.K_3:
                    current_mode = 'end'
                elif event.key == pygame.K_4:
                    current_mode = 'weight'
                elif event.key == pygame.K_c:
                    clear_board(keep_walls=False)
                    stats.update(visited=0, path_len=0, time_ms=0, status='Ready')
                elif event.key == pygame.K_r:
                    random_maze()
                elif event.key == pygame.K_v:
                    start_visualization()
                elif event.key == pygame.K_TAB:
                    idx = ALGO_KEYS.index(selected_algo)
                    selected_algo = ALGO_KEYS[(idx + 1) % len(ALGO_KEYS)]
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    steps_per_frame = min(steps_per_frame + 2, 50)
                elif event.key == pygame.K_MINUS:
                    steps_per_frame = max(steps_per_frame - 2, 1)

        # advance the running algorithm a few steps per frame
        if animating and algo_gen is not None:
            for _ in range(steps_per_frame):
                try:
                    next(algo_gen)
                except StopIteration:
                    animating = False
                    algo_gen = None
                    break

        screen.fill(BG)
        draw_topbar()
        draw_grid()
        draw_statsbar()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
