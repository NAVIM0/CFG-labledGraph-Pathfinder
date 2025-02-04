import itertools

left, right = 0, 1


def seekAndDestroy(target, productions):
    trash, erased = [], []
    for production in productions:
        if target in production[right] and len(production[right]) == 1:
            trash.append(production[left])
        else:
            erased.append(production)

    return trash, erased


def setupDict(productions, variables, terms):
    result = {}
    for production in productions:
        #
        if production[left] in variables and production[right][0] in terms and len(production[right]) == 1:
            result[production[right][0]] = production[left]
    return result


def rewrite(target, production):
    result = []
    #get positions corresponding to the occurrences of target in production right side
    #positions = [m.start() for m in re.finditer(target, production[right])]
    positions = [i for i, x in enumerate(production[right]) if x == target]
    #for all found targets in production
    for i in range(len(positions) + 1):
        #for all combinations of all possible length phrases of targets
        for element in list(itertools.combinations(positions, i)):
            #Example: if positions is [1 4 6]
            #now I've got: [] [1] [4] [6] [1 4] [1 6] [4 6] [1 4 6]
            #erease position corresponding to the target in production right side
            tadan = [production[right][i] for i in range(len(production[right])) if i not in element]
            if tadan:
                result.append((production[left], tadan))
    return result


def prettyForm(rules):
    dictionary = {}
    for rule in rules:
        if rule[left] in dictionary:
            dictionary[rule[left]] += ' | ' + ' '.join(rule[right])
        else:
            dictionary[rule[left]] = ' '.join(rule[right])
    result = ""
    for key in dictionary:
        result += key + " -> " + dictionary[key] + "\n"
    return result
