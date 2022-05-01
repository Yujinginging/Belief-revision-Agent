# Imports
from BaseBelief import BaseBelief, bb


# Define a new belief base
def newBeliefBase(base):
    globals()[base] = BaseBelief()


# Define a function to add a belief to a certain base
def addBelief(base, sentence, rank):
    base.add(sentence, rank)
    
    
# Printing the belief base
def printBase(base):
    print(base)