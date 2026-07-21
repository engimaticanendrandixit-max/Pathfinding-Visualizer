# Pathfinding Visualizer

An interactive pathfinding visualizer built using Python and Pygame. This project demonstrates how popular graph traversal and shortest-path algorithms work by animating their execution on a grid.

Users can create walls, weighted nodes, generate random mazes, and compare the behavior of different algorithms in real time.

---

## Features

- Interactive grid-based interface
- Visualize multiple pathfinding algorithms
- Add and remove walls
- Create weighted nodes
- Generate random mazes
- Real-time animation
- Adjustable visualization speed
- Live statistics panel

---

## Implemented Algorithms

### Breadth First Search (BFS)

- Guarantees shortest path in an unweighted graph.
- Uses a queue.

### Depth First Search (DFS)

- Explores one branch completely before backtracking.
- Uses a stack.
- Does not guarantee shortest path.

### Dijkstra's Algorithm

- Finds the shortest path with weighted nodes.
- Uses a priority queue.

### A* Search Algorithm

- Optimized shortest-path algorithm.
- Uses Manhattan distance heuristic.

---

## Technologies Used

- Python 3
- Pygame
- Heap Queue
- Collections (Deque)
- VS Code 
---

## Controls

| Key | Action |
|------|------|
| 1 | Wall Mode |
| 2 | Start Node |
| 3 | End Node |
| 4 | Weight Mode |
| V | Start Visualization |
| TAB | Change Algorithm |
| C | Clear Grid |
| R | Generate Random Maze |
| + | Increase Speed |
| - | Decrease Speed |

---

## Mouse Controls

- Left Click → Draw
- Right Click → Erase

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/Pathfinding-Visualizer.git
```

Move into the project directory:

```bash
cd Pathfinding-Visualizer
```

Install dependencies:

```bash
pip install pygame
```

Run the project:

```bash
python main.py
```

---

## Project Structure

```

Pathfinding-Visualizer/
│
├── main.py
├── README.md
├── requirements.txt
└── screenshots/

```

---

## Algorithms Comparison

| Algorithm | Shortest Path | Weighted Graph |
|------------|------------|------------|
| BFS | Yes | No |
| DFS | No | No |
| Dijkstra | Yes | Yes |
| A* | Yes | Yes |

---

## Future Improvements

- Diagonal movement
- Additional algorithms
- Custom maze generators
- Dark/light themes
- Save and load maps

---

## License

This project is open-source and available under the MIT License.

---

## Author

Anendra Narayan Dixit
