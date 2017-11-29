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


def get_cliques_kou_stockmeyer_wong(nodes):
    temp_cliques = []  # type: [set[int]]
    
    for i in range(0, len(nodes)):
        w = set()  # type: set[int]
        for j in range(0, i):
            if nodes[j] in nodes[i].adjacent:
                w.add(j)
        if len(w) == 0:
            temp_cliques.append({i})
            continue
        v = set()  # type: set[int]
        m = 0
        while m < len(temp_cliques) and w != v:
            if temp_cliques[m] <= w:
                temp_cliques[m].add(i)
                v |= temp_cliques[m]
            m += 1
        w -= v
        while len(w) > 0:
            min_m = len(temp_cliques)
            max_cardinality = -1
            for m in range(0, len(temp_cliques)):
                card = len(temp_cliques[m] & w)
                if card > max_cardinality:
                    max_cardinality = card
                    min_m = m
                elif card == max_cardinality and m < min_m:
                    max_cardinality = card
                    min_m = m
            temp_cliques.append((temp_cliques[m] & w) | {i})
            w -= temp_cliques[m]
    
    cliques = [set(nodes[i] for i in temp_cliques[0])]
    for k in range(1, len(temp_cliques)):
        edges = {(nodes[i], nodes[j])
                 for i in temp_cliques[k]
                 for j in temp_cliques[k]
                 if i < j}
        
        for clique in cliques:
            edges -= {(u, v)
                      for u in clique
                      for v in clique
                      if u != v}
        
        if len(edges) > 0:
            cliques.append({nodes[i]
                            for i in temp_cliques[k]})

    return cliques
