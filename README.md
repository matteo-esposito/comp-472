https://github.com/matteo-esposito/comp-472

# COMP472 - Project 1

## Usage (General)

First, clone the repo and cd into the src folder.

```bash
git clone https://github.com/matteo-esposito/comp-472.git
cd comp-472/project-1/src/
```

## Usage (Algorithms)

**Note:** If you want to provide your own test cases, modify the .txt file at the filepath in the `testfile` variable of `input_parser.py`.

### 1. DFS

```bash
python dfs.py
```

### 2. A*

To choose a heuristic, simply modify line 19 of the `node.py` file: 

```python
self.h = self.calculate_h1() or self.h = self.calculate_h2()
```

then,

```bash
python a_star.py
```

### 3. BFS

The run procedure is the same as A* but set;

```python
use_g = False
```
on line 40 for node class to indicate that no g(n) function is used. Then,

```bash
python bfs.py
```