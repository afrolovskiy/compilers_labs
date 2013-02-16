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
from pygraph.classes.exceptions import AdditionError


SPECIAL_SYMBOLS = ['(', ')', '*', '|']


def get_alphabet(regexp):
    return set(regexp) - set(SPECIAL_SYMBOLS)


class FA:
    EMPTY = 'empty'
    
    def __init__(self, transition_table, initial_state, final_state, alphabet=None):
        self.transition_table = transition_table
        self.initial_state = initial_state
        self.final_state = final_state
        self.alphabet = alphabet

    def draw(self, filename):
        print "initial state:", self.initial_state
        print "final states", self.final_state	
        print "transition table:", self.transition_table 

        vertexes = self.transition_table.keys()
        edges = self._edges()

        gr = digraph()        
        #gr.add_nodes([str(vertex) for vertex in vertexes])
        for vertex in vertexes:
            attrs = []
            
            if ((isinstance(self.final_state, list) and vertex in self.final_state) or
                    (isinstance(self.final_state, int) and vertex == self.final_state)):
                attrs.append('final')
            gr.add_node(str(vertex), attrs=attrs)

        for edge, label in edges.items():
            label = ', '.join(label)
            gr.add_edge(edge=edge, label=label)

        dot = write(gr)
        gvv = gv.readstring(dot)
        gv.layout(gvv, 'dot')
        gv.render(gvv, 'png', '%s.png' % filename)

    def _edges(self):
        edges = {}
        vertexes = self.transition_table.keys()
        for initial_vertex in vertexes:
            edges.update(self._outgoing_edges(initial_vertex))
        return edges

    def _outgoing_edges(self, initial_vertex):
        edges = {}
        transitions = self.transition_table[initial_vertex]
        for label in transitions.keys():
            final_vertexes = transitions.get(label, [])
            for final_vertex in final_vertexes:
                if edges.get((str(initial_vertex), str(final_vertex)), None):
                    edges[(str(initial_vertex), str(final_vertex))].append(label)
                else:
                    edges[(str(initial_vertex), str(final_vertex))] = [label]
        return edges


################################################################
class WrongRegularExpressionError(Exception):
    pass


class TompsonAlgorithm:

    def __init__(self, regexp):
        self.regexp = regexp
        self.last_vertex = 0

    def buildNFA(self):
        fa = self._buildNFA(self.regexp)
        fa.alphabet = get_alphabet(self.regexp)
        return fa
        
    def _buildNFA(self, regexp):
        stack = []
        idx = 0
        while idx < len(regexp):
            ch = regexp[idx]
            if ch == '(':
                group, idx = self._select_group(regexp, idx)
                stack.append(self._buildNFA(group))
            elif ch == '*':
                stack.append(self._iterationNFA(stack.pop()))
            elif ch == '|':
                left_fa = self._concatenateNFAlist(stack)
                right_fa = self._buildNFA(regexp[idx + 1:])
                return self._orNFA(left_fa, right_fa)
            else:
                stack.append(self._symbolNFA(ch))
            idx += 1
        return self._concatenateNFAlist(stack)            

    def _select_group(self, regexp, sidx):
        level = 0
        idx = sidx + 1
        group = ''
        while idx < len(regexp):
            ch = regexp[idx]
            if ch == ')':
                if level == 0:
                    return group, idx
                level -= 1
            elif ch == '(':
                level += 1
            group += ch
            idx += 1
        raise WrongRegularExpressionError()
            
    def _iterationNFA(self, fa):
        initial_state = self.last_vertex
        final_state = self.last_vertex + 1
        
        transition_table = fa.transition_table
        transition_table[initial_state] = {
            FA.EMPTY: [fa.initial_state, final_state]
        }
        transition_table[fa.final_state] = {
            FA.EMPTY: [fa.initial_state, final_state]
        }
        transition_table[final_state] = {
            FA.EMPTY: []
        }

        self.last_vertex += 2
        return FA(transition_table, initial_state, final_state)

    def _concatenateNFAlist(self, fa_list):
        right_fa = fa_list.pop()
        while fa_list:
            left_fa = fa_list.pop()
            right_fa = self._concatenateNFA(left_fa, right_fa)
        return right_fa        

    def _concatenateNFA(self, fa1, fa2):
        initial_state = fa1.initial_state
        final_state = fa2.final_state

        transition_table = fa1.transition_table
        transition_table.update(fa2.transition_table)
        transition_table[fa1.final_state] = {
            FA.EMPTY: [fa2.initial_state]
        }

        return FA(transition_table, initial_state, final_state)      

    def _orNFA(self, fa1, fa2):
        initial_state = self.last_vertex
        final_state = self.last_vertex + 1

        transition_table = fa1.transition_table
        transition_table.update(fa2.transition_table)
        transition_table.update({
            initial_state: {
                FA.EMPTY: [fa1.initial_state, fa2.initial_state]
            },
            fa1.final_state: {
                FA.EMPTY: [final_state]
            },
            fa2.final_state: {
                FA.EMPTY: [final_state]
            },
            final_state: {},
        })

        self.last_vertex += 2        
        return FA(transition_table, initial_state, final_state)        
              
    def _symbolNFA(self, symbol):
        initial_state = self.last_vertex
        final_state = self.last_vertex + 1

        transition_table = {
            initial_state: {
                symbol: [final_state]
            },
            final_state: {}
        }

        self.last_vertex += 2
        return FA(transition_table, initial_state, final_state)
################################################################

################################################################
class DeterminizationAlgorithm:

    def __init__(self, nfa):
        self.nfa = nfa    
        self.alphabet = nfa.alphabet

    def build_subsets(self):
        last_state = 0
        generalized_states = {}
        transition_table ={}
        initial_state = None
        final_state = []	

        closure = self._closure([self.nfa.initial_state], self.nfa.transition_table)
        generalized_states = {last_state: set(closure)}
        if self.nfa.final_state in closure:
            final_state.append(last_state)
        initial_state = last_state
        last_state += 1

        d_states = [set(closure)]
        unmarked = [set(closure)]

        while unmarked:
            T = unmarked.pop()
            transitions = {}
            for a in self.alphabet:   
                mv = self._move(list(T), a, self.nfa.transition_table)
                U = set(self._closure(mv, self.nfa.transition_table))
                if U:
                    if U not in d_states:
                        d_states.append(U)
                        generalized_states[last_state] = U
                        if self.nfa.final_state in U:
                            final_state.append(last_state)
                        last_state += 1
                        unmarked.append(U)
                    transitions.update({a: [self.get_key_by_value(generalized_states, U)]})
            transition_table[self.get_key_by_value(generalized_states, T)] = transitions   
        return FA(transition_table, initial_state, final_state, self.alphabet)

    def get_key_by_value(self, dictionary, value):
        for key, item in dictionary.items():
            if item == value:
                return key

    def _closure(self, T, transition_table):
        stack = list(T)
        closure = list(T)
        while stack:
            t = stack.pop()
            for u in transition_table[t].get(FA.EMPTY, []):
                if u not in closure:
                    closure.append(u)
                    stack.append(u)
        return closure

    def _move(self, T, a, transition_table):
        result = set()
        for s in T:
            states = set(transition_table[s].get(a, []))
            result = result.union(states)
        return result
################################################################


################################################################
class MinimizationAlgorithm:
    
    def __init__(self, fa):
        self.fa = fa
        self.alphabet = fa.alphabet

    def minimize(self):
        partition = self._build_equivalence_classes()
        return self._build_equivalent_fa(partition)
        
    def _build_equivalence_classes(self):
        states = set(self.fa.transition_table.keys())
        final_states = set(self.fa.final_state)

        partition = [list(states.difference(final_states)), list(final_states)] 
        new_partition = self._build_new_partitions(partition)

        while partition != new_partition:
            partition = new_partition
            new_partition = self._build_new_partitions(partition)

        return partition

    def _build_new_partitions(self, partition):
        new_partition = []
        for group in partition: 
            subgroups = [group]
            for symbol in self.alphabet:
                new_subgroups = []
                for sg in subgroups:
                    new_subgroups.extend(self._build_group_partitions(sg, symbol, partition))
                subgroups = new_subgroups
            new_partition.extend(subgroups)
        return new_partition

    def _build_group_partitions(self, subgroup, symbol, partition):
        if len(subgroup) == 1:
            return [subgroup]

        transitions = {}
        for idx in range(len(partition)):
            transitions[idx] = []  
        transitions[FA.EMPTY] = []      

        for state in subgroup:
            states = self.fa.transition_table.get(state, {}).get(symbol, [])
            if states:
                group_idx = self._group_index(states[0], partition)
            else:
                group_idx = FA.EMPTY
            transitions[group_idx].append(state)

        new_subgroups = []
        for new_subgroup in transitions.values():
            if new_subgroup:
                new_subgroups.append(new_subgroup)

        return new_subgroups

    def _group_index(self, state, partition):
        for idx in range(len(partition)):
            group = partition[idx]
            if state in group:
                return idx
            
    def _build_equivalent_fa(self, partition):
        new_transition_table = {}
        for idx in range(len(partition)):
            state = partition[idx][0]
            new_transition_table[idx] = {}
            for symbol in self.alphabet:
                transitions = self.fa.transition_table.get(state, {}).get(symbol, [])
                if transitions:
                    group_idx = [self._group_index(transitions[0], partition)]
                else:
                    group_idx = []
                new_transition_table[idx][symbol] = group_idx

        initial_state = self._group_index(self.fa.initial_state, partition)
        final_state = list(set([self._group_index(final_state, partition) for final_state in self.fa.final_state]))
        return FA(new_transition_table, initial_state, final_state, self.alphabet)
################################################################


################################################################
class WrongString(Exception):
    pass

class ModellingAlgorithm:
    
    def __init__(self, fa):
        self.fa = fa
        self.alphabet = fa.alphabet

    def model(self, source):
        state = self.fa.initial_state
        for symbol in source:
            state = self._move(state, symbol)
        if state in self.fa.final_state:
            print "string is matching"
            return True
        raise WrongString()

    def _move(self, state, symbol):
        transitions = self.fa.transition_table.get(state, {}).get(symbol, [])
        if transitions:
            return transitions[0]
        raise WrongString()
################################################################
