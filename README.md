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
   git clone https://github.com/NAVIMO/CFG-Graph-Pathfinder.git
   cd CFG-Graph-Pathfinder
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

    # Main Algorithm Section
    graph_input = LabeledGraph("graph.json")
    cfg_input = CFGParser("grammar.json")

    result = cfg_paths(graph_input, cfg_input)

    print(f"#All compliant paths:")
    for (start, end), paths in result.items():
        print(f"Paths from {start} to {end}:")
        for path in paths:
            print(" -> ".join(path))

    # Extra Points Section
    startNode = "A"
    pruned_graph = LabeledGraph("graph.json", startNode)

    result = cfg_paths(pruned_graph, cfg_input)

    print(f"\n#Paths starting from node {startNode}:")
    for (start, end), paths in result.items():
        print(f"Paths from {start} to {end}:")
        for path in paths:
            print(" -> ".join(path))
```

## Input Format
### Graph (`graph.json`)
```json
{
        "Vertices": ["A", "B", "C", "D", "E", "F"],
        "Edges": ["A, B, x", "A, C, y", "C, D, k", "D, B, y", "D, C, j", "E, C, x", "F, E, k", "F, D, x"]
}
```

### Grammar (`grammar.json`)
```json
{
    "terminals": ["j", "k", "x", "y"],
    "non_terminals": ["S", "H", "P", "O", "W", "R", "G"],
    "productions": {
        "S": [["H", "P"], ["P", "G"]],
        "H": [["O", "R"]],
        "P": [["W", "R"]],
        "O": [["y"]],
        "W": [["j"]],
        "R": [["k"]],
        "G": [["x"]]
    },
    "start_symbol": "S"
}
```

## Output Example
```
#CFG converted to CNF:
S -> H P | P G
H -> O R
P -> W R
O -> y
W -> j
R -> k
G -> x
S0 -> H P | P G


#All compliant paths:
Paths from A to D:
y -> k -> j -> k

#Paths starting from node A:
Paths from A to D:
y -> k -> j -> k
```

## Contributing
Contributions are welcome! Feel free to submit **issues** or **pull requests**.

## License
📜 MIT License

