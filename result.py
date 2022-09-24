from random import choice, shuffle, randint
from time import time


def generate_simple_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = []
    for j in range(0, n_generate):
        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_oper: items
            },
            'then': code_max + j
        }
        rules.append(rule)
    shuffle(rules)
    return rules


def generate_stairway_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = []
    for j in range(0, n_generate):

        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(i + j)
        rule = {
            'if': {
                log_oper: items
            },
            'then': i + j + 1
        }
        rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_ring_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = generate_stairway_rules(code_max, n_max, n_generate - 1, log_oper_choice)
    log_oper = choice(log_oper_choice)  # not means and-not (neither)
    if n_max < 2:
        n_max = 2
    n_items = randint(2, n_max)
    items = []
    for i in range(0, n_items):
        items.append(code_max - i)
    rule = {
        'if': {
            log_oper: items
        },
        'then': 0
    }
    rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_random_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = []
    for j in range(0, n_generate):

        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_oper: items
            },
            'then': randint(1, code_max)
        }
        rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_seq_facts(M):
    facts = list(range(0, M))
    shuffle(facts)
    return facts


def generate_rand_facts(code_max, M):
    facts = []
    for i in range(0, M):
        facts.append(randint(0, code_max))
    return facts


# generate rules and facts and check time
time_start = time()
N = 10000
M = 1000
rules = generate_simple_rules(100, 4, N)
facts = generate_rand_facts(100, M)
print("%d rules generated in %f seconds" % (N, time() - time_start))


# load and validate rules
# YOUR CODE HERE


def neg_or_pos_rules(rules):
    negative = []
    positive = []
    for rule in rules:
        if 'not' in rule['if'].keys():
            neg = [{1: list(rule['if'].values())[0]}, rule['then']]
            if neg not in negative:
                negative.append(neg)
        else:
            pos = [{1: list(rule['if'].values())[0]}, rule['then'], list(rule['if'].keys())[0]]
            if pos not in positive:
                positive.append(pos)

    # negative.sort(key=lambda s: len(s[0]))
    # positive.sort(key=lambda s: len(s[0]))
    return [negative, positive]


def controversy_ab_not_ab(negative, positive):
    for neg in negative:
        for pos in positive:
            # print(list(pos[0].values())[0])
            if neg[1] == pos[1] and list(neg[0]).sort == list(pos[0]).sort:
                negative.remove(neg)
                positive.remove(pos)
    return [negative, positive]


def and_or_or_rules(positive):
    and_rules = []
    or_rules = []
    for pos in positive:
        if pos[2] == 'and':
            and_rules.append([pos[0], pos[1]])
        else:
            or_rules.append([pos[0], pos[1]])
    return [and_rules, or_rules]


def check_or(or_rules, rang, res, or_mass, max_rang):
    is_found = 0
    for rule in or_rules:
        buf = list(rule[0].values())[0]
        if rang in rule[0]:
            for i in range(len(buf)):
                if buf[i] in facts:
                    max_rang += 1  # чтоб потом знать до какого ранга обходить
                    or_mass.append({rang + 1: rule[1]})
                    res[rule[1]] = 1
                    is_found = 1
                    break
        else:
            # тут же проверка на наличие полученного ранее факта в каком-либо из правил or
            for or_mini in or_mass:
                if rang in or_mini:
                    if list(or_mini.values())[0] in buf:
                        max_rang += 1  # чтоб потом знать до какого ранга обходить
                        or_mass.append({rang + 1: rule[1]})
                        res[rule[1]] = 1
                        is_found = 1
    return is_found


def check_and(and_rules, rang, res, and_mass, max_rang):
    is_found = 0
    for rule in and_rules:
        flag_and = 1
        # из условной части беру массив фактов
        buf = list(rule[0].values())[0]

        if rang in rule[0]:
            for i in range(len(buf)):
                if buf[i] not in facts:
                    flag_and = 0
                    break
            if flag_and == 1:
                # если все есть то бахаю их в res
                for i in range(len(buf)):
                    if rang + 1 > max_rang:
                        max_rang = rang + 1  # чтоб потом знать до какого ранга обходить
                    and_mass.append({rang + 1: rule[1]})
                    res[rule[1]] = 1
                    is_found = 1
        else:
            # тут же проверка на наличие полученного ранее факта в каком-либо из правил or
            for and_mini in and_mass:
                # если факт уже добавлен, то не нужно проверять правило
                if res[rule[1]] != 1 and rang in and_mini:
                    for i in range(len(buf)):
                        if buf[i] not in facts:
                            flag_and = 0
                            break
                    if flag_and == 1:
                        # если все есть то бахаю их в res
                        for i in range(len(buf)):
                            if rang + 1 > max_rang:
                                max_rang = rang + 1  # чтоб потом знать до какого ранга обходить
                            and_mass.append({rang + 1: rule[1]})
                            res[rule[1]] = 1
                            is_found = 1
    return is_found


def check_not(not_rules, res):
    is_found = 0
    for rule in not_rules:
        flag = 1
        buf = list(rule[0].values())[0]
        for i in range(len(rule[0])):
            if buf[i] in facts or buf[i] in res:
                flag = 0
                break
        if flag == 1:
            res[rule[1]] = 1
            is_found = 1
    return is_found


def main():
    res = [None] * 10100
    res_facts = []
    or_mass = []
    and_mass = []
    rang = 1  # начальный ранг
    max_rang = 1  # максимальный ранг

    neg, pos = neg_or_pos_rules(rules)
    neg, pos = controversy_ab_not_ab(neg, pos)
    and_rules, or_rules = and_or_or_rules(pos)

    while 1:
        flag = 0
        flag += check_and(and_rules, rang, res, and_mass, max_rang)
        flag += check_or(or_rules, rang, res, or_mass, max_rang)
        flag += check_not(neg, res)
        # если ранг не вырос, то вложенностей больше нет
        if flag == 0:
            break
        rang += 1

    index = 0
    while index < 10100:
        if res[index] == 1:
            res_facts.append(index)
        index += 1

    return res_facts


# check facts vs rules
time_start = time()

# YOUR CODE HERE

if __name__ == '__main__':
    result = main()

print("%d facts validated vs %d rules in %f seconds" % (M, N, time() - time_start))
print(result)
