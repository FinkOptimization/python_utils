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


from . import Node


def get_cliques_bron_kerbosch(nodes):
    p = set(nodes)
    r = set()
    x = set()
    return bron_kerbosch(r, p, x, True)


def bron_kerbosch(
        r,  # type: set[Node]
        p,  # type: set[Node]
        x,  # type: set[Node]
        inner=False
):
    if len(p) == len(x) == 0:
        yield r
    else:
        iter_nodes = set()
        if inner:
            px = p | x
            u = px.pop()
            adjacency = len([n for n in u.adjacent if n in p])
            for node in px:
                local_adjacency = len(node.adjacent & p)
                if local_adjacency > adjacency:
                    adjacency = local_adjacency
                    u = node
            iter_nodes.update(p - u.adjacent)
        else:
            max_degree = max(len(n.adjacent) for n in p)
            nodes_of_degree = [set() for _ in range(max_degree + 1)]
            smallest_index = len(p)
            for node in p:
                degree = len(node.adjacent)
                nodes_of_degree[degree].add(node)
                node.bron_kerbosch_cell_index = degree
                node.visited = False
                if degree < smallest_index:
                    smallest_index = degree
            for _ in p:
                i = smallest_index
                while len(nodes_of_degree[i]) == 0:
                    i += 1
                node = nodes_of_degree[i].pop()
                node.visited = True
                for n in node.adjacent:
                    if not n.visited:
                        nodes_of_degree[n.bron_kerbosch_cell_index].remove(n)
                        n.bron_kerbosch_cell_index -= 1
                        nodes_of_degree[n.bron_kerbosch_cell_index].add(n)
                        if n.bron_kerbosch_cell_index < smallest_index:
                            smallest_index = n.bron_kerbosch_cell_index
                
                iter_nodes.add(node)
        
        for v in iter_nodes:
            r_copy = set(r)
            r_copy.add(v)
            p_copy = p & v.adjacent
            x_copy = x & v.adjacent
            for clique in bron_kerbosch(r_copy, p_copy, x_copy, True):
                yield clique
            p.remove(v)
            x.add(v)
