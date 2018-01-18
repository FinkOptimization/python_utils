# -*- coding: utf-8 -*-
# MIT LICENSE
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import math

class Node:
    def __init__(self, name: str = ""):
        self.name = name
        self.adjacent = set()  # type: set[Node]
        self.bron_kerbosch_cell_index = 0
        self.visited = False
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name


def print_statistics(nodes: [Node]):
    print("Graph statistics")
    edges = math.floor(sum(len(n.adjacent) for n in nodes) / 2)
    density = edges / len(nodes) / (len(nodes) + 1)
    print("  Nodes      : {:8}\n  Edges      : {:8}\n  Density    : {:8.2%}".format(len(nodes),edges,density))
    print("  Expected maximal cliques in random graph = {}".format(
        expected_maximal_cliques_in_random_graph(len(nodes),density)))
    queue = []
    visited = set()
    components = []
    for node in nodes:
        if node in visited:
            continue
        queue.append(node)
        visited.add(node)
        new_component = []
        while len(queue) > 0:
            next_node = queue.pop()
            new_component.append(next_node)
            for neighbour in next_node.adjacent:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        components.append(new_component)
    print("\n  Components : {:8}".format(len(components)))
    for (i, component) in enumerate(components):
        print("    Component: {:8}".format(i))
        edges = math.floor(sum(len(n.adjacent) for n in component) / 2)
        density = edges / len(component) / (len(component) + 1)
        print("    Nodes      : {:8}\n    Edges      : {:8}\n    Density    : {:8.2%}".format(len(component),
                                                                                              edges,
                                                                                              density))
        print("    Expected maximal cliques in random graph = {}".format(
            expected_maximal_cliques_in_random_graph(len(component), density)))


def expected_maximal_cliques_in_random_graph(nodes: int, edge_probability: float) -> float:
    last_term = nodes * math.pow(1 - edge_probability, nodes - 1)
    expected_maximal = last_term
    for d in range(1, nodes):
        mult = (nodes - d) / (d + 1) * math.pow(edge_probability, d)
        mult *= math.pow(1 - math.pow(edge_probability, d + 1), nodes - d - 1)
        mult /= math.pow(1 - math.pow(edge_probability, d), nodes - d)
        new_term = last_term * mult
        expected_maximal += new_term
        last_term = new_term
    return expected_maximal
