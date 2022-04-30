from sympy.logic.boolalg import And, Or, Implies, Not


_op_identity = {And: True, Or: False}

def dissociate(op, args):
    #Given an associative operator, return a flattened list result
    result = []

    def collect(subargs):
        for arg in subargs:
            if arg.func == op:
                collect(arg.args)
            else:
                result.append(arg)

    collect(args)
    return result

def associate(op, args):
    # Given an associative operator, return an flattened expression 
    #such that nested instances of the same operator is at the top level.
    
    args = dissociate(op, args)
    if len(args) == 0:
        return _op_identity[op]
    elif len(args) == 1:
        return args[0]
    else:
        return op(*args)


def firstInIterable(iterable, default=None):
    return next(iter(iterable), default)



def convert_implications(s):
    if s.is_symbol:
        return s

    if s.func == Implies:
        a, b = s.args
        s = Or(b, Not(a))
    
    args = []
    for arg in s.args:
        args.append(convert_implications(arg))

    return s.func(*args)


def negation_inward(s):

    if s.is_symbol:
        return s

    if s.func == Not:
        def NOTTING(b):
            return negation_inward(Not(b))

        a = s.args[0]
        if a.is_symbol:
            return s

        if a.func == Not:
            return negation_inward(a.args[0])

        if a.func == And:
            return associate(Or, list(map(NOTTING, a.args)))

        if a.func == Or:
            return associate(And, list(map(NOTTING, a.args)))
        return s

    return s.func(*list(map(negation_inward, s.args)))


def cnf_equivalent_S(s):
   #distribute and over or
    #s is a sentence that contains literals conjuct and disconjuct
    #it returns an equivalent sentence in CNF
    if s.func == Or:
        s = associate(Or, s.args)
        if s.func != Or:
            return cnf_equivalent_S(s)
        if len(s.args) == 0:
            return False
        if len(s.args) == 1:
            return cnf_equivalent_S(s.args[0])
        conj = firstInIterable(arg for arg in s.args if arg.func == And)
        if not conj:
            return s
        others = [a for a in s.args if a is not conj]
        rest = associate(Or, others)
        return associate(And, [cnf_equivalent_S(c | rest)
                               for c in conj.args])
    elif s.func == And:
        return associate(And, list(map(cnf_equivalent_S, s.args)))
    else:
        return s



def to_cnf(s):
    #Converts the given propositional logical sentence to CNF 
    s = convert_implications(s)
    s = negation_inward(s)
    s = cnf_equivalent_S(s)
    return s

