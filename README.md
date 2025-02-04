# CFG-Based Graph Pathfinding

🚀 A Python-based algorithm to find all valid paths in a graph that comply with a given **Context-Free Grammar (CFG)**. The algorithm supports **CNF conversion**, **graph traversal**, and **dynamic path refinement**.

## Features
- ✅ Parses **graph structures** and **context-free grammars (CFGs)**  
- ✅ Converts **CFG to CNF** to ensure compatibility  
- ✅ Uses **dynamic programming (DP)** and a **worklist algorithm** for pathfinding  
- ✅ Supports an **extra feature** where paths starting from a specific node are extracted  

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/CFG-Graph-Pathfinder.git
   cd CFG-Graph-Pathfinder
   ```
2. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Run the Algorithm
```bash
python main.py
```
By default, it loads a **graph from `graph.json`** and a **CFG from `grammar.json`**.

### Example
```python
if __name__ == "__main__":
    graph_input = LabeledGraph("graph.json")
    cfg_input = CFGParser("grammar.json")

    # Find all compliant paths
    result = cfg_paths(graph_input, cfg_input)

    # Extract paths starting from a specific node (optional)
    start_node = "A"
    filtered_result = {key: paths for key, paths in result.items() if key[0] == start_node}

    print(f"\nPaths starting from node {start_node}:")
    for (start, end), paths in filtered_result.items():
        print(f"{start} -> {end}:")
        for path in paths:
            print(" -> ".join(path))
```

## Input Format
### Graph (`graph.json`)
```json
{
    "Vertices": ["A", "B", "C", "D"],
    "Edges": ["A, B, x", "B, C, y", "C, D, z"]
}
```

### Grammar (`grammar.json`)
```json
{
    "terminals": ["x", "y", "z"],
    "non_terminals": ["S", "A", "B"],
    "productions": {
        "S": [["A", "B"], ["B", "C"]],
        "A": [["x"]],
        "B": [["y"]],
        "C": [["z"]]
    },
    "start_symbol": "S"
}
```

## Output Example
```
Paths starting from node A:
A -> B:
x
A -> C:
x -> y
```

## Contributing
Contributions are welcome! Feel free to submit **issues** or **pull requests**.

## License
📜 MIT License

