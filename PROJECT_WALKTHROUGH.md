# How It Works

## Overview

Pathfinding Visualizer is an interactive application built using Python and Pygame. It demonstrates how different graph traversal and shortest-path algorithms work by visualizing their execution on a grid.

The user can place walls, weighted nodes, change the start and end points, and observe how each algorithm finds a path.

---

## Step 1: Initial Grid

<img width="1081" height="724" alt="image" src="https://github.com/user-attachments/assets/856a833f-c9d3-48c1-9aa0-50f9929dfd68" />


When the application starts, a grid is generated with predefined start and end nodes.

- Green node → Start point
- Red node → Destination
- Empty cells → Traversable area

---

## Step 2: Creating Obstacles

<img width="1077" height="722" alt="image" src="https://github.com/user-attachments/assets/89c871ca-9fcc-4805-88d1-53583cc1b27d" />


Users can place walls to block certain paths.

- Left click to create walls.
- Right click to erase walls.
- Walls force the algorithms to search for alternative routes.

---

## Step 3: Adding Weighted Nodes

<img width="1080" height="726" alt="image" src="https://github.com/user-attachments/assets/d2301c20-25e0-4c1f-a433-cb4f4599b1e7" />


Weighted nodes increase the traversal cost.

- Yellow cells represent weighted nodes.
- Dijkstra's Algorithm and A* Algorithm take weights into account.
- BFS and DFS ignore weights.

---

## Step 4: Selecting an Algorithm

<img width="1075" height="81" alt="image" src="https://github.com/user-attachments/assets/461d57e8-2df0-4675-ba6b-22c59b437cce" />
<img width="1081" height="87" alt="image" src="https://github.com/user-attachments/assets/99445bf2-bcc6-4726-a613-866a2e1bf6e7" />
<img width="1076" height="86" alt="image" src="https://github.com/user-attachments/assets/9b8b4003-1da5-4118-923e-ccb974507b98" />
<img width="1076" height="91" alt="image" src="https://github.com/user-attachments/assets/263b47ef-4d29-41a8-be29-1a3107300248" />


Users can switch between different algorithms:

- Breadth First Search (BFS)
- Depth First Search (DFS)
- Dijkstra's Algorithm
- A* Search Algorithm

Press `TAB` to cycle through algorithms.

---

## Step 5: Running the Visualization

<img width="1024" height="713" alt="image" src="https://github.com/user-attachments/assets/62a7aa32-7fda-4818-9a6c-18cadeb2dcf1" />


Press `V` or click the **Visualize** button to start the animation.

During execution:

- Blue cells represent visited nodes.
- Yellow cells represent the final shortest path.
- The statistics panel displays:
  - Number of visited nodes
  - Path length
  - Execution time
  - Animation speed

---

## Step 6: Maze Generation

<img width="1084" height="726" alt="image" src="https://github.com/user-attachments/assets/ad9ac1b9-343c-417d-a936-bd1a001e088a" />


Press `R` to generate a random maze automatically.

The algorithms will then attempt to find a valid path through the generated obstacles.

---

## Algorithms Used

### Breadth First Search (BFS)

- Uses a queue.
- Guarantees the shortest path in an unweighted graph.

### Depth First Search (DFS)

- Uses a stack.
- Does not guarantee the shortest path.

### Dijkstra's Algorithm

- Uses a priority queue.
- Supports weighted nodes.

### A* Search Algorithm

- Uses a heuristic function.
- Explores fewer nodes and is generally faster.

---

## Controls

| Key | Action |
|-------|--------|
| 1 | Wall Mode |
| 2 | Start Node |
| 3 | End Node |
| 4 | Weight Mode |
| V | Visualize |
| TAB | Change Algorithm |
| C | Clear Grid |
| R | Random Maze |
| + | Increase Speed |
| - | Decrease Speed |

---

## Technologies Used

- Python
- Pygame
- Queue
- Stack
- Heap Queue
- Graph Algorithms
