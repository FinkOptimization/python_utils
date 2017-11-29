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
from .. import Node, get_cliques_kou_stockmeyer_wong


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
        number_of_cliques = 5
        
        with self.subTest("Number of cliques"):
            cliques = get_cliques_kou_stockmeyer_wong(nodes)
    
            self.assertEqual(len(cliques), number_of_cliques,
                             "The number of cliques in the graph should be {}".format(number_of_cliques))
        
        with self.subTest("Finding cliques"):
            # The following are the cliques in the graph
            real_cliques = [
                {nodes[0], nodes[1], nodes[4]},
                {nodes[1], nodes[2]},
                {nodes[2], nodes[3]},
                {nodes[3], nodes[4]},
                {nodes[3], nodes[5]}
            ]
            for clique in real_cliques:
                clique_found = False
                for other_clique in cliques:
                    if len(clique ^ other_clique) == 0:
                        clique_found = True
                        break
                self.assertTrue(clique_found, "Clique ({}) could not be found".format(clique))


if __name__ == '__main__':
    unittest.main()
