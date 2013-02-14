# Import graphviz
import sys
sys.path.append('..')
sys.path.append('/usr/lib/graphviz/python/')
sys.path.append('/usr/lib64/graphviz/python/')
import gv

# Import pygraph
from pygraph.classes.digraph import digraph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write


class FA:
    EMPTY = 'empty'
    
    def __init__(self, transition_table, initial_state, final_state):
        self.transition_table = transition_table
        self.initial_state = initial_state
        self.final_state = final_state  

    def draw(self, filename):
        print "transition table:", self.transition_table 
        gr = digraph()
        vertexes = self.transition_table.keys()
        gr.add_nodes([str(vertex) for vertex in vertexes])
        for initial_vertex in vertexes:
            transitions = self.transition_table[initial_vertex]
            for label in transitions.keys():
                final_vertexes = transitions.get(label, [])
                for final_vertex in final_vertexes:
                    gr.add_edge(edge=(str(initial_vertex), str(final_vertex)), label=label)
        dot = write(gr)
        gvv = gv.readstring(dot)
        gv.layout(gvv, 'dot')
        gv.render(gvv, 'png', '%s.png' % filename)


GROUP_START = '('
GROUP_END = ')'
ITERATION = '*'
OR = '|'
SPECIAL_SYMBOLS = [GROUP_START, GROUP_END, ITERATION, OR]

def get_alphabet(self, regexp):
    return set(regexp) - set(SPECIAL_SYMBOLS)
