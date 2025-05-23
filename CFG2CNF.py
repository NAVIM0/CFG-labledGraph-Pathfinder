#It's assumed that starting variable is the first typed
import helper

left, right = 0, 1

K, V, Productions = [], [], []
variablesJar = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
                "W", "X", "Y", "Z"]


def isUnary(rule, variables):
    if rule[left] in variables and rule[right][0] in variables and len(rule[right]) == 1:
        return True
    return False


def isSimple(rule):
    if rule[left] in V and rule[right][0] in K and len(rule[right]) == 1:
        return True
    return False


for nonTerminal in V:
    if nonTerminal in variablesJar:
        variablesJar.remove(nonTerminal)


#Add S0->S rule––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––START
def START(productions, variables):
    variables.append('S0')
    return [('S0', [variables[0]])] + productions


#Removes rules containing both terms and variables, like A->Bc, replaced by A->BZ and Z->c----–––––––––––TERM
def TERM(productions, variables):
    newProductions = []
    dictionary = helper.setupDict(productions, variables, terms=K)
    for production in productions:
        if isSimple(production):

            newProductions.append(production)
        else:
            for term in K:
                for index, value in enumerate(production[right]):
                    if term == value and not term in dictionary:

                        dictionary[term] = variablesJar.pop()
                        V.append(dictionary[term])
                        newProductions.append((dictionary[term], [term]))

                        production[right][index] = dictionary[term]
                    elif term == value:
                        production[right][index] = dictionary[term]
            newProductions.append((production[left], production[right]))

    return newProductions


#Eliminates non unit rules––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––BIN
def BIN(productions, variables):
    result = []
    for production in productions:
        k = len(production[right])

        if k <= 2:
            result.append(production)
        else:
            newVar = variablesJar.pop(0)
            variables.append(newVar + '1')
            result.append((production[left], [production[right][0]] + [newVar + '1']))

            for i in range(1, k - 2):
                var, var2 = newVar + str(i), newVar + str(i + 1)
                variables.append(var2)
                result.append((var, [production[right][i], var2]))
            result.append((newVar + str(k - 2), production[right][k - 2:k]))
    return result


#Delete non terminal rules–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––DEL
def DEL(productions):
    newSet = []
    outlaws, productions = helper.seekAndDestroy(target='e', productions=productions)

    for outlaw in outlaws:
        for production in productions + [e for e in newSet if e not in productions]:

            if outlaw in production[right]:
                newSet = newSet + [e for e in helper.rewrite(outlaw, production) if e not in newSet]

    return newSet + ([productions[i] for i in range(len(productions))
                      if productions[i] not in newSet])


def unit_routine(rules, variables):
    unities, result = [], []

    for aRule in rules:
        if isUnary(aRule, variables):
            unities.append((aRule[left], aRule[right][0]))
        else:
            result.append(aRule)

    for uni in unities:
        for rule in rules:
            if uni[right] == rule[left] and uni[left] != rule[left]:
                result.append((uni[left], rule[right]))

    return result


def UNIT(productions, variables):
    i = 0
    result = unit_routine(productions, variables)
    tmp = unit_routine(result, variables)
    while result != tmp and i < 1000:
        result = unit_routine(tmp, variables)
        tmp = unit_routine(result, variables)
        i += 1
    return result
