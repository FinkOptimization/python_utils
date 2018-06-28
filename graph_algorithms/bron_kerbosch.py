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


from typing import Set
from math import pow
from . import Node, get_degeneracy_ordering


def get_cliques_bron_kerbosch(nodes, ordered_nodes=False):
    p = set(nodes)
    r = set()
    x = set()
    if ordered_nodes:
        nodes_ordered = nodes
    else:
        _, nodes_ordered = get_degeneracy_ordering(nodes)
    for v in nodes_ordered:
        for clique in bron_kerbosch(r | {v}, p & v.adjacent, x & v.adjacent):
            yield clique
        p.remove(v)
        x.add(v)


def bron_kerbosch(r: Set[Node], p: Set[Node], x: Set[Node]):
    if len(p) == len(x) == 0:
        yield r
    else:
        px = p | x
        u = px.pop()
        adjacency = len(p & u.adjacent)
        for node in px:
            local_adjacency = len(p & node.adjacent)
            if local_adjacency > adjacency:
                adjacency = local_adjacency
                u = node
        iter_nodes = p - u.adjacent
        for v in sorted(iter_nodes, key=lambda x: x.name):
            for clique in bron_kerbosch(r | {v}, p & v.adjacent, x & v.adjacent):
                yield clique
            p.remove(v)
            x.add(v)


def worst_case_running_time_bron_kerbosch(nodes, d=None):
    if not d:
        d, _ = get_degeneracy_ordering(nodes)
    return d * len(nodes) * pow(3, d / 3)
