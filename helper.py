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
        if production[left] in variables and production[right][0] in terms and len(production[right]) == 1:
            result[production[right][0]] = production[left]
    return result


def rewrite(target, production):
    result = []
    positions = [i for i, x in enumerate(production[right]) if x == target]

    for i in range(len(positions) + 1):

        for element in list(itertools.combinations(positions, i)):

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
