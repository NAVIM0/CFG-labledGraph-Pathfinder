import json
from collections import defaultdict
from CFG2CNF import START, TERM, BIN, DEL, UNIT
from helper import prettyForm


def cfg_paths(graph, cfg):
    dp = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

    # Base case (Initialize for terminal edges)
    for u, v, label in graph.edges:
        for lhs, rhs_list in cfg.productions.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs[0] == label:  # Unary rule (A → terminal)
                    dp[u][v][lhs].add((label,))

    # Iterative updates using dp
    changed = True
    while changed:
        changed = False
        updates = []
        all_pairs = [(A, B) for A in dp.keys() for B in dp[A].keys()]

        for A, B in all_pairs:
            for C in dp[B].keys():

                for lhs1, paths1 in list(dp[A][B].items()):
                    for lhs2, paths2 in list(dp[B][C].items()):
                        for lhs3, rhs_list in cfg.productions.items():
                            for rhs in rhs_list:
                                if len(rhs) == 2 and rhs[0] == lhs1 and rhs[1] == lhs2:
                                    for path1 in paths1:
                                        for path2 in paths2:

                                            new_path = path1 + path2
                                            if new_path not in dp[A][C][lhs3]:
                                                updates.append((A, C, lhs3, new_path))

        #Applys updates after iteration
        for A, C, lhs3, new_path in updates:
            if new_path not in dp[A][C][lhs3]:
                dp[A][C][lhs3].add(new_path)
                changed = True

    # Collect paths derivable from the start symbol
    valid_paths = defaultdict(list)
    start_symbol = cfg.start_symbol
    for u in dp.keys():
        for v in dp[u].keys():
            if start_symbol in dp[u][v]:
                valid_paths[(u, v)].extend(dp[u][v][start_symbol])

    return valid_paths


class LabeledGraph:
    def __init__(self, file_path, start_node=None):

        with open(file_path, 'r') as file:
            inputGraph = json.load(file)

        # Builds an adjacency list
        adjacency_list = defaultdict(list)
        for edge in inputGraph["Edges"]:
            u, v, label = edge.split(",")
            u, v, label = u.strip(), v.strip(), label.strip()
            adjacency_list[u].append((v, label))

        # If start_node exists, prune the graph
        if start_node:
            self.prune_graph(inputGraph, adjacency_list, start_node)
        else:
            self.vertices = inputGraph["Vertices"]
            self.edges = [(u.strip(), v.strip(), label.strip()) for edge in inputGraph["Edges"]
                          for u, v, label in [edge.split(",")]]

    def prune_graph(self, inputGraph, adjacency_list, start_node):

        #BFS to find reachable nodes
        reachable_nodes = set()
        queue = [start_node]

        while queue:
            node = queue.pop(0)
            if node not in reachable_nodes:
                reachable_nodes.add(node)
                for neighbor, _ in adjacency_list[node]:
                    if neighbor not in reachable_nodes:
                        queue.append(neighbor)

        reachable_edges = []

        for edge in inputGraph["Edges"]:
            u, v, label = edge.split(",")
            u, v, label = u.strip(), v.strip(), label.strip()

            if u in reachable_nodes and v in reachable_nodes:
                reachable_edges.append((u, v, label))

        self.vertices, self.edges = list(reachable_nodes), reachable_edges


class CFGParser:
    def __init__(self, grammar_file):

        with open(grammar_file, 'r') as file:
            grammar_input = json.load(file)

        self.terminals = list(grammar_input["terminals"])
        self.non_terminals = list(grammar_input["non_terminals"])
        self.productions = [
            (lhs, rhs) for lhs, rhs_list in grammar_input["productions"].items() for rhs in rhs_list
        ]
        self.start_symbol = "S0"
        self.transform_to_cnf()

    def transform_to_cnf(self):

        self.productions = START(self.productions, self.non_terminals)
        self.productions = TERM(self.productions, self.non_terminals)
        self.productions = BIN(self.productions, self.non_terminals)
        self.productions = DEL(self.productions)
        self.productions = UNIT(self.productions, self.non_terminals)

        formatted_output = prettyForm(self.productions)
        print("\n#CFG converted to CNF:\n" + formatted_output + '\n')
        self.convert_to_json(formatted_output)

    def convert_to_json(self, formatted_output):

        cnf_grammar = {"productions": defaultdict(list)}
        for line in formatted_output.strip().split('\n'):
            if '->' in line:
                lhs, rhs = line.split('->')
                lhs = lhs.strip()
                rhs_options = [r.strip().split() for r in rhs.split('|')]
                cnf_grammar["productions"][lhs] = rhs_options

        self.productions = cnf_grammar["productions"]


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
