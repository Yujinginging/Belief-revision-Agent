from ToCNF import to_cnf
from sympy.logic.boolalg import Or, And


def removeall(item, seq):
    return [x for x in seq if x != item]

def unique(seq):
    return list(set(seq))

def disjuncts(clause):
    return dissociate(Or, [clause])

def conjuncts(clause):
    return dissociate(And, [clause])

def associate(op, args):
    args = dissociate(op, args)
    if len(args) == 0:
        return op.identity
    elif len(args) == 1:
        return args[0]
    else:
        return op(*args)

def dissociate(op, args):
    result = []

    def collect(args):
        for arg in args:
            if isinstance(arg, op):
                collect(arg.args)
            else:
                result.append(arg)

    collect(args)
    return result


def entailment(base, formula):
    """
    Resolution-based entailment check for base |- formula.
    """

    formula = to_cnf(formula)

    # Split base into conjuncts
    clauses = []
    for f in base:
        clauses += conjuncts(f)
    # Add contradiction to start resolution
    clauses += conjuncts(to_cnf(~formula))

    # Special case if one clause is already False
    if False in clauses:
        return True

    result = set()
    while True:
        n = len(clauses)
        pairs = [
            (clauses[i], clauses[j])
            for i in range(n) for j in range(i + 1, n)
        ]

        for ci, cj in pairs:
            resolvents = resolve(ci, cj)
            if False in resolvents:
                return True
            result = result.union(set(resolvents))

        if result.issubset(set(clauses)):
            return False
        for c in result:
            if c not in clauses:
                clauses.append(c)


def resolve(ci, cj):
    """
    Generate all clauses that can be obtained by applying
    the resolution rule on ci and cj.
    """

    clauses = []
    dci = disjuncts(ci)
    dcj = disjuncts(cj)

    for di in dci:
        for dj in dcj:
            # If di, dj are complementary
            if di == ~dj or ~di == dj:
                # Create list of all disjuncts except di and dj
                res = removeall(di, dci) + removeall(dj, dcj)
                # Remove duplicates
                res = unique(res)
                # Join into new clause
                dnew = associate(Or, res)

                clauses.append(dnew)

    return clauses



#test entailment
import sympy as sp

def test():
    kb = sp.parse_expr("p | q").binary_symbols
    #kb ="p & q"
    formula = sp.parse_expr("z")
    print(kb)
    kb_entails_formula = entailment(kb, formula)
    print(kb_entails_formula)

    kb = sp.parse_expr("p & q").binary_symbols
    formula = sp.parse_expr("p >> q")

    kb_entails_formula = entailment(kb, formula)
    print(kb_entails_formula)

    kb = sp.parse_expr("p & q").binary_symbols
    formula = sp.parse_expr("z >> q")

    kb_entails_formula = entailment(kb, formula)
    print(kb_entails_formula)

    kb = sp.parse_expr("p & q").binary_symbols
    formula = sp.parse_expr("~q >> p")

    kb_entails_formula = entailment(kb, formula)
    print(kb_entails_formula)

    kb = sp.parse_expr("(a|b)&c&d").binary_symbols
    formula = sp.parse_expr("c")

    kb_entails_formula = entailment(kb, formula)
    print(kb_entails_formula)
    
    
test()
