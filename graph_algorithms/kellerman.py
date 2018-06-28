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


from math import pow
from . import get_components, get_degeneracy_ordering


def get_cliques_kellerman(nodes, ordered_nodes=False):
    for component in get_components(nodes):
        for clique in _get_cliques_kellerman(component, ordered_nodes):
            yield clique


def _get_cliques_kellerman(nodes_list, ordered_nodes):
    cliques = []  # type: [set[int]]
    if ordered_nodes:
        nodes = nodes_list
    else:
        _, nodes = get_degeneracy_ordering(nodes_list)
    neighbours_less_uncovered = []
    neighbours_less = []
    neighbours_greater = []
    can_add_to_clique = []
    in_cliques = []
    intersection = []
    for i in range(len(nodes)):
        neighbours_less_uncovered.append(set())
        neighbours_less.append(set())
        neighbours_greater.append(set())
        can_add_to_clique.append(set())
        in_cliques.append(set())
        intersection.append({})
        for j in range(len(nodes)):
            if nodes[j] in nodes[i].adjacent:
                if j < i:
                    neighbours_less_uncovered[i].add(j)
                    neighbours_less[i].add(j)
                elif j > i:
                    neighbours_greater[i].add(j)
    
    for i in range(len(nodes)):
        if len(neighbours_less_uncovered[i]) == 0:
            for j in neighbours_greater[i]:
                can_add_to_clique[j].add(len(cliques))
                intersection[j].update({len(cliques): 1})
            in_cliques[i].add(len(cliques))
            cliques.append({i})
            continue
        
        for l in can_add_to_clique[i]:
            if cliques[l] <= neighbours_less[i] and l in intersection[i] and intersection[i][l] > 0:
                cliques[l].add(i)
                in_cliques[i].add(l)
                for j in neighbours_greater[i]:
                    if l in can_add_to_clique[j] and i not in neighbours_less[j]:
                        can_add_to_clique[j].remove(l)
                    if i in neighbours_less_uncovered[j]:
                        if l not in intersection[j]:
                            intersection[j].update({l: 1})
                        else:
                            intersection[j][l] += 1
                
                for j in neighbours_less_uncovered[i]:
                    if j in cliques[l]:
                        for cl in in_cliques[j]:
                            if cl in intersection[i]:
                                intersection[i][cl] -= 1
                                if intersection[i][cl] == 0:
                                    del intersection[i][cl]
                    
                neighbours_less_uncovered[i] -= cliques[l]
                if len(neighbours_less_uncovered[i]) == 0:
                    break
        
        while len(neighbours_less_uncovered[i]) > 0:
            min_l = -1
            max_val = -1
            
            for (l, size) in intersection[i].items():
                size = intersection[i][l]
                if size > max_val:
                    max_val = size
                    min_l = l
            
            new_clique = (cliques[min_l] & neighbours_less_uncovered[i])
            for j in new_clique:
                for l in in_cliques[j]:
                    if l in intersection[i]:
                        intersection[i][l] -= 1
                        if intersection[i][l] == 0:
                            del intersection[i][l]
            
            neighbours_less_uncovered[i] -= new_clique
            new_clique.add(i)
            
            all_neighbours = set(neighbours_greater[i])
            intersected_neighbours = set(neighbours_greater[i])
            for j in new_clique:
                in_cliques[j].add(len(cliques))
                if i != j:
                    intersected_neighbours &= neighbours_greater[j]
                    for h in neighbours_greater[j]:
                        if h > i and h not in all_neighbours:
                            all_neighbours.add(h)
            
            for j in intersected_neighbours:
                can_add_to_clique[j].add(len(cliques))
            
            for h in all_neighbours:
                size = len(new_clique & neighbours_less_uncovered[h])
                if size > 0:
                    intersection[h].update({len(cliques): size})

            cliques.append(new_clique)
    
    return [{nodes[n]
             for n in clique}
            for clique in cliques]


def worst_case_running_time_kellerman(nodes):
    return len(nodes) * pow(sum([len(node.adjacent) for node in nodes]) / 2, 2)
