from fa import FA, get_alphabet
from tompson_algorithm import TompsonAlgorithm
from determinization_algorithm import DeterminizationAlgorithm


class MinimizationAlgorithm:
    
    def __init__(self, fa, alphabet):
        self.fa = fa
        self.alphabet = alphabet

    def minimize(self):
        partition = self._build_equivalence_classes()
        return self._build_equivalent_fa(partition)
        
    def _build_equivalence_classes(self):
        states = set(self.fa.transition_table.keys())
        final_states = set(self.fa.final_state)

        partition = [list(states.difference(final_states)), list(final_states)] 
        #print "partition:", partition
        new_partition = self._build_new_partitions(partition)
        #print "new partition:", new_partition

        while partition != new_partition:
            partition = new_partition
            new_partition = self._build_new_partitions(partition)
            #print "new partition:", new_partition

        return partition

    def _build_new_partitions(self, partition):
        new_partition = []
        for group in partition: 
            #print "group:", group
            subgroups = [group]
            #print "subgroups:", subgroups
            for symbol in self.alphabet:
                #print "symbol:", symbol
                new_subgroups = []
                for sg in subgroups:
                    #print "subgroup:", sg
                    new_subgroups.extend(self._build_group_partitions(sg, symbol, partition))
                    #print "new_subgroups:", new_subgroups
                subgroups = new_subgroups
                #print "subgroups:", subgroups
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
            #print "state:", state
            states = self.fa.transition_table.get(state, {}).get(symbol, [])
            #print "states:", states
            if states:
                group_idx = self._group_index(states[0], partition)
            else:
                group_idx = FA.EMPTY
            transitions[group_idx].append(state)

        #print "transitions:", transitions
        
        new_subgroups = []
        for new_subgroup in transitions.values():
            if new_subgroup:
                new_subgroups.append(new_subgroup)

        #print "new_subgroups:", new_subgroups
        return new_subgroups

    def _group_index(self, state, partition):
        for idx in range(len(partition)):
            group = partition[idx]
            if state in group:
                return idx
            
    def _build_equivalent_fa(self, partition):
        #print "partition:", partition

        new_transition_table = {}
        for idx in range(len(partition)):
            state = partition[idx][0]
            #print "state:", state

            new_transition_table[idx] = {}
            for symbol in self.alphabet:
                transitions = self.fa.transition_table.get(state, {}).get(symbol, [])
                if transitions:
                    group_idx = [self._group_index(transitions[0], partition)]
                else:
                    group_idx = []
                new_transition_table[idx][symbol] = group_idx

        initial_state = self._group_index(self.fa.initial_state, partition)
        final_state = [self._group_index(self.fa.final_state[0], partition)]
        return FA(new_transition_table, initial_state, final_state)


#regexp = "a(a*|b)*b"
regexp = "a|b"
alg1 = TompsonAlgorithm(regexp)
fa = alg1.buildNFA()
fa.draw('graph')

alg2 = DeterminizationAlgorithm(fa, ['a', 'b'])
fa2 = alg2.build_subsets()

fa2.draw('graph2') 

alg3 = MinimizationAlgorithm(fa2, ['a', 'b'])
fa3 = alg3.minimize()
fa3.draw('graph3') 
