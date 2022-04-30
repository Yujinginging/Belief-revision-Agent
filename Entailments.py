import sympy as sp
from sympy.logic.boolalg import  And, Or, Implies, Not
from ToCNF import to_cnf



def entailment(kb, formula):
    #kb |= a
    formula = to_cnf(formula)
    symbols = (kb & formula).binary_symbols
    return check_all(kb, formula, symbols, {})


def check_all(kb, formula, symbols, model):
    if not symbols:
        if kb.subs(model) == True:
            result = formula.subs(model)
            assert result in (True, False)
            return result
        else:
            return True
    else:
        P = symbols.pop()
        m_true = model.copy();    
        m_false = model.copy()
        m_true[P] = True;         
        m_false[P] = False

        result = check_all(kb, formula, symbols.copy(), m_true) and check_all(kb, formula, symbols.copy(), m_false)
        return result



#test entailment
def test():
    kb = sp.parse_expr("p & q")
    formula = sp.parse_expr("z")

    kb_entails_formula = entailment(kb, formula)
    print(kb_entails_formula)

    kb = sp.parse_expr("p & q")
    formula = sp.parse_expr("p >> q")

    kb_entails_formula = entailment(kb, formula)
    print(kb_entails_formula)

    kb = sp.parse_expr("p & q")
    formula = sp.parse_expr("z >> q")

    kb_entails_formula = entailment(kb, formula)
    print(kb_entails_formula)

    kb = sp.parse_expr("p & q")
    formula = sp.parse_expr("~q >> p")

    kb_entails_formula = entailment(kb, formula)
    print(kb_entails_formula)

    kb = sp.parse_expr("(a|b)&c&d")
    formula = sp.parse_expr("c")

    kb_entails_formula = entailment(kb, formula)
    print(kb_entails_formula)
    
test()