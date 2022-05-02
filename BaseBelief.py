import math
from sortedcontainers import SortedList
from operator import neg
from sympy.logic.boolalg import to_cnf, And, Or, Equivalent
#from utils import associate
from Entailments import entailment
from functools import reduce

class Belief:

    def __init__(self, formula, rank=None):
        self.formula = formula
        self.rank = rank

    def __eq__(self, other):
        return self.rank == other.rank and self.formula == other.formula

    def __lt__(self, other):
        return self.rank < other.rank

    def __repr__(self):
        return f'Belief({self.formula}, order={self.rank})'


class BaseBelief:

    def __init__(self):

        # base beilief Sorted by decreasing order that is rank
        self.beliefs = SortedList(key=lambda b: neg(b.rank))

        # a command queue to add formulas to the belief base
        self._rerank_formulas = []

    def _add_rerank_formulas(self, belief, rank):

        # add a formula to command queue
        return self._rerank_formulas + [to_cnf(belief), rank]

    def _run_rerank_formulas(self):

        # run the command queue to change the formulas' rank
        for belief, rank in self._rerank_formulas:
            self.beliefs.remove(belief)
            # Ignore beliefs with rank = 0
            if rank >= 0:
                belief.rank = rank
                self.beliefs.add(belief)
        self._rerank_formulas = []

    def _remove_rerank_formulas(self, formula):

        # remove any command with the given formula if it is already in the base belief
        for belief in self.beliefs:
            if belief.formula == formula:
                self._add_rerank_formulas(belief, 0)
        self._run_rerank_formulas()

    def add(self, formula, rank):

        # add a formula(sentence) to the base belief without checking the formula validity
        formula = to_cnf(formula)
        # validate rank
        if not (0 <= rank <= 1):
            raise ValueError

            # drop a formula in command queue if it is already in the base belief
        self._remove_rerank_formulas(formula)

        # beliefs with rank
        if rank >= 0:
            belief = Belief(formula, rank)
            self.beliefs.add(belief)

    def iterate_by_rank(self):

        # Generator that groups beliefs in the  base belief by decreasing rank.
        result = []
        last_rank = None

        for belief in self.beliefs:

            # If it is the first belief that we examine, add it and set last_rank
            if last_rank == None:
                result.append(belief)
                last_rank = belief.rank
                continue

            # If the rank of this belief is "equal" to the previous, add it to the group
            # a boolean method returns true if they are equal
            if math.isclose(belief.rank, last_rank):
                result.append(belief)

            # Otherwise, yield the group and reset
            else:
                yield last_rank, result
                result = []
                result.append(belief)
                last_rank = belief.rank

        # Yield last rank
        yield last_rank, result
        
        
    def contraction(self, formula):
        if entailment(True, formula):
            print("{formula} is a tautology")
            return

        old_rank = self.rank(formula)
        x = BaseBelief()
        
        for belief in self.beliefs:
            # check if the rank is less or equal to old rank
            if belief.rank <= old_rank:
                belifbase = to_cnf(x.formula) 
                if not entailment(belifbase, formula | belief.formula):
                    rank_ = x.rank(belief.formula)
                    x.beliefs.remove(belief)
                    print(f" {belief} removed")
                    if rank_ < old_rank:
                        for i in self.beliefs:
                            if formula >> belief.formula == i.formula:
                                x.beliefs.remove(i)
                        y = Belief(formula >> belief.formula, rank_)
                        x.beliefs.add(y)
                        print(f" {y} is added to belief basis")
        self.beliefs = x.beliefs

    def clear(self):
        # clear base belief
        self.beliefs.clear()

    def __len__(self):
        # how may beliefs in the base belief
        return len(self.beliefs)

    def __getitem__(index):
        # get belief by index
        return self.beliefs[index]

    def __iter__(self):
        return iter(self.beliefs)

    def __reversed__(self):
        return reversed(self.beliefs)

    def __repr__(self):
        if len(self.beliefs) == 0:
            return 'empty'
        return '\n'.join(str(x) for x in self.beliefs)


# testing the base belief
bb = BaseBelief()
bb.add('a', 0.5)
bb.add('b', 0.5)
bb.add('a|b', 0.6)
bb.add('a&d', 0.3)
for it in bb.iterate_by_rank():
    print(it)

#_add_rerank_formulas
ba = BaseBelief()
bc= ba._add_rerank_formulas('a&b', 0.5)
print(bc)
