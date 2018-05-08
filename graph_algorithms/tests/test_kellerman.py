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

import unittest
import math

from .. import Node, get_cliques_kellerman


class TestBasicKouStockMeyerWongFunctionality(unittest.TestCase):
    def test_finding_cliques_in_small_graph(self):
        
        """
        The graph:

             5
              \
               3 -- 4
               |    | \
               |    |  0
               |    | /
               2 -- 1

        The cliques of the graph:

            0, 1, 4
            1, 2
            2, 3
            3, 4
            3, 5
        """
        nodes = [Node(str(i)) for i in range(6)]
        nodes[0].adjacent.update({nodes[1], nodes[4]})
        nodes[1].adjacent.update({nodes[0], nodes[2], nodes[4]})
        nodes[2].adjacent.update({nodes[1], nodes[3]})
        nodes[3].adjacent.update({nodes[2], nodes[4], nodes[5]})
        nodes[4].adjacent.update({nodes[0], nodes[1], nodes[3]})
        nodes[5].adjacent.update({nodes[3]})
        
        print("Kellerman worst case run time: O(n * m) = {}".format(
            len(nodes) * math.pow(sum([len(node.adjacent) for node in nodes]) / 2, 2)))

        cliques = [clique for clique in get_cliques_kellerman(nodes)]
        
        with self.subTest("Is covering all edges"):
            # The following are the cliques in the graph
            for n1 in range(len(nodes) - 1):
                for n2 in range(n1 + 1, len(nodes)):
                    if nodes[n2] in nodes[n1].adjacent:
                        edge_found = False
                        for clique in cliques:
                            if nodes[n1] in clique and nodes[n2] in clique:
                                edge_found = True
                                break
                        self.assertTrue(edge_found, "Edge ({},{}) could not be found".format(n1, n2))


if __name__ == '__main__':
    unittest.main()
2