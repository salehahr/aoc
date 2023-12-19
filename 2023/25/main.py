import math
import re

import networkx as nx
from tools import parse_lines, print_part


@print_part
def solve(filepath: str, part: int):
    graph = nx.Graph()

    for line in parse_lines(filepath):
        c1, *c2s = re.findall(r"(\w+)", line)
        for c2 in c2s:
            graph.add_edge(c1, c2)

    to_remove = nx.minimum_edge_cut(graph)
    graph.remove_edges_from(to_remove)

    result = math.prod([len(cutset) for cutset in nx.connected_components(graph)])
    print(result)


if __name__ == "__main__":
    FILEPATH = "input_short.txt"
    # FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
