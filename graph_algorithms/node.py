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
from collections import Iterable
from iterable import first


class Node:
    def __init__(self, name: str = ""):
        self.name = name
        self.adjacent = set()
        self.degeneracy_cell_index = 0
        self.visited = False

    def add_adjacent(self, *args):
        for element in args:
            if isinstance(element, Iterable):
                for node in element:
                    self.add_adjacent(node)
            elif isinstance(element, Node):
                self.adjacent.add(element)
            else:
                raise ValueError(
                    'Input must either be of class node or an iterable of Node. Received {} instead'.format(
                        type(element)))
    
    def __str__(self):
        return self.name
    
    __repr__ = __str__


def print_statistics(nodes: [Node]):
    print("Graph statistics")
    edges = math.floor(sum(len(n.adjacent) for n in nodes) / 2)
    density = edges / len(nodes) / (len(nodes) + 1)
    print("  Nodes      : {:8}\n  Edges      : {:8}\n  Density    : {:8.2%}".format(len(nodes),edges,density))
    print("  Expected maximal cliques in random graph = {}".format(
        expected_maximal_cliques_in_random_graph(len(nodes),density)))
    queue = []
    components = []
    for node in nodes:
        node.visited = False
    for node in nodes:
        if node.visited:
            continue
        queue.append(node)
        new_component = []
        while len(queue) > 0:
            next_node = queue.pop()
            new_component.append(next_node)
            for neighbour in next_node.adjacent:
                if not neighbour.visited:
                    neighbour.visited = True
                    queue.append(neighbour)
        components.append(new_component)
    print("\n  Components : {:8}".format(len(components)))
    print("    Smallest component: {}".format(min([len(component) for component in components])))
    print("    Largest component : {}".format(max([len(component) for component in components])))
    min_expected_cliques = len(nodes) + edges
    max_expected_cliques = 0
    total_expected_cliques = 0
    for (i, component) in enumerate(components):
        edges = math.floor(sum(len(n.adjacent) for n in component) / 2)
        density = edges / len(component) / (len(component) + 1)
        expected_cliques = expected_maximal_cliques_in_random_graph(len(component), density)
        if expected_cliques < min_expected_cliques:
            min_expected_cliques = expected_cliques
        if expected_cliques > max_expected_cliques:
            max_expected_cliques = expected_cliques
        total_expected_cliques += expected_cliques
    avg_expected_cliques = total_expected_cliques / len(components)
    
    print("    Expected maximal cliques in random graphs")
    print("      Min             : {}".format(min_expected_cliques))
    print("      Avg             : {}".format(avg_expected_cliques))
    print("      Max             : {}".format(max_expected_cliques))
    print("      Total           : {}".format(total_expected_cliques))


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


def get_degeneracy_ordering(nodes) -> (int, [Node]):
    max_degree = max(len(n.adjacent) for n in nodes)
    nodes_of_degree = [set() for _ in range(max_degree + 1)]
    smallest_index = len(nodes)
    degeneracy_ordering = []
    for node in nodes:
        degree = len(node.adjacent)
        nodes_of_degree[degree].add(node)
        node.degeneracy_cell_index = degree
        node.visited = False
        if degree < smallest_index:
            smallest_index = degree
    degeneracy_number = 0
    for _ in nodes:
        while len(nodes_of_degree[smallest_index]) == 0:
            smallest_index += 1
        if smallest_index > degeneracy_number:
            degeneracy_number = smallest_index
        node = first(nodes_of_degree[smallest_index])
        for n in nodes_of_degree[smallest_index]:
            if n.name < node.name:
                node = n
        nodes_of_degree[smallest_index].remove(node)
        node.visited = True
        for n in node.adjacent:
            if not n.visited:
                nodes_of_degree[n.degeneracy_cell_index].remove(n)
                n.degeneracy_cell_index -= 1
                nodes_of_degree[n.degeneracy_cell_index].add(n)
                if n.degeneracy_cell_index < smallest_index:
                    smallest_index = n.degeneracy_cell_index
    
        degeneracy_ordering.append(node)
    return degeneracy_number, degeneracy_ordering


def get_components(nodes) -> []:
    components = []
    for node in nodes:
        node.visited = False
    queue = []
    for node in nodes:
        if node.visited:
            continue
        new_component = []
        node.visited = True
        queue.append(node)
        while len(queue) > 0:
            next_node = queue.pop()
            new_component.append(next_node)
            for neighbour in next_node.adjacent:
                if not neighbour.visited:
                    neighbour.visited = True
                    queue.append(neighbour)
        components.append(new_component)
    return components
