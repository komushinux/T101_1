"""Creates knowledge base"""

from random import choice, shuffle, randint
from time import time


def generate_simple_rules(code_max, n_max, n_generate, log_op_choice=None):
    """generate_simple_rules"""
    if log_op_choice is None:
        log_op_choice = ["and", "or", "not"]
    rules_list = []
    for j in range(0, n_generate):
        log_opera = choice(log_op_choice)  # not means and-not (neither)
        n_max = max(2, n_max)
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_opera: items
            },
            'then': code_max + j
        }
        rules_list.append(rule)
    shuffle(rules_list)
    return rules_list


def generate_stairway_rules(code_max, n_max, n_generate, log_op_choice=None):
    """generate_stairway_rules"""
    if log_op_choice is None:
        log_op_choice = ["and", "or", "not"]
    rules_list = []
    for j in range(0, n_generate):

        log_opera = choice(log_op_choice)  # not means and-not (neither)
        n_max = max(n_max, 2)
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(i + j)
        rule = {
            'if': {
                log_opera: items
            },
            'then': code_max + j + 1
        }
        rules_list.append(rule)
    shuffle(rules_list)
    return rules_list


def generate_ring_rules(code_max, n_max, n_generate, log_op_choice=None):
    """generate_ring_rules"""
    if log_op_choice is None:
        log_op_choice = ["and", "or", "not"]
    rules_list = generate_stairway_rules(code_max, n_max, n_generate - 1, log_op_choice)
    log_opera = choice(log_op_choice)  # not means and-not (neither)
    n_max = max(2, n_max)
    n_items = randint(2, n_max)
    items = []
    for i in range(0, n_items):
        items.append(code_max - i)
    rule = {
        'if': {
            log_opera: items
        },
        'then': 0
    }
    rules_list.append(rule)
    shuffle(rules_list)
    return rules_list


def generate_random_rules(code_max, n_max, n_generate, log_op_choice=None):
    """generate_random_rules"""
    if log_op_choice is None:
        log_op_choice = ["and", "or", "not"]
    rules_list = []
    for j in range(0, n_generate):

        log_opera = choice(log_op_choice)  # not means and-not (neither)
        n_max = max(2, n_max)
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_opera: items
            },
            'then': randint(1, code_max)
        }
        rules_list.append(rule)
    shuffle(rules_list)
    return rules_list


def generate_seq_facts(max_value):
    """generate_seq_facts"""
    facts_list = list(range(0, max_value))
    shuffle(facts_list)
    return facts_list


def generate_rand_facts(code_max, max_value):
    """generate_rand_facts"""
    facts_list = []
    for i in range(0, max_value):
        facts_list.append(randint(0, code_max))
    return facts_list


# generate rules and facts and check time
time_start = time()
N = 10000
M = 1000
rules = generate_simple_rules(100, 4, N)
facts = generate_rand_facts(100, M)
print(f"{N} rules generated in {time() - time_start} seconds")


# facts = [1, 2]
# rules = [
#     {'if': {'and': [1, 2]}, 'then': 3},
#     {'if': {'or': [5, 7]}, 'then': 1},
#     {'if': {'or': [3, 2]}, 'then': 5},
#     {'if': {'not': [1234, 2213]}, 'then': 3},
#
#     {'if': {'not': [9]}, 'then': 8},
#     {'if': {'not': [8]}, 'then': 9},
#
#     {'if': {'or': [1, 2]}, 'then': 9},
#     {'if': {'not': [2, 1]}, 'then': 9},
# ]


def neg_or_pos_rules(rules_list):
    """gets all rules and returns or/and/not-rules massive"""
    not_rules = []
    and_rules = []
    or_rules = []
    for rule in rules_list:
        lus = [{1: list(rule['if'].values())[0]}, rule['then']]
        if 'not' in rule['if'].keys():
            if lus not in not_rules:
                not_rules.append(lus)
        elif 'and' in rule['if'].keys():
            if lus not in and_rules:
                and_rules.append(lus)
        else:
            if lus not in or_rules:
                or_rules.append(lus)
    return [not_rules, and_rules, or_rules]


def controversy_ab_not_ab(not_rules, and_rules, or_rules):
    """resolves the contradiction like (a->b), (not a->b)"""
    for neg in not_rules:
        for pos in and_rules:
            if neg[1] == pos[1] and sorted(list(pos[0].values())[0]) == sorted(list(neg[0].values())[0]):
                not_rules.remove(neg)
                and_rules.remove(pos)
        for pos in or_rules:
            if neg[1] == pos[1] and sorted(list(pos[0].values())[0]) == sorted(list(neg[0].values())[0]):
                not_rules.remove(neg)
                or_rules.remove(pos)


def controversy_not_a_b_not_b_a(not_rules):
    """resolves the contradiction like (not a->b), (not b->a)"""
    for rule_i in not_rules:
        buf = list(rule_i[0].values())[0]
        if len(buf) == 1:
            for rule_j in not_rules:
                if buf[0] == rule_j[1]:
                    not_rules.remove(rule_i)
                    not_rules.remove(rule_j)


def check_or(or_rules, rang, res, or_mass, max_rang):
    """
        Searching new facts in or_rules

            Params:
                or_rules(list) - list of all or_rules
                rang(int) - current rang, where we are searching new facts'
                res(list) - list with flags, where indexes = facts
                or_mass(list) - list of dicts, where key = rang, value = new fact
                max_rang(int) - current max_rang
            Returns:
                max_rang
    """

    for rule in or_rules:
        # из условной части беру массив фактов
        buf = list(rule[0].values())[0]
        # сработает, если ранг = 1
        if rang in rule[0]:
            for i in range(len(buf)):
                if buf[i] in facts:
                    max_rang = 2  # чтоб потом знать до какого ранга обходить
                    or_mass.append({2: rule[1]})
                    res[rule[1]] = 1
                    break

        else:
            # тут же проверка на наличие полученного ранее факта в каком-либо из правил or
            for or_mini in or_mass:
                # Если есть в res, то нового факта не появится, возможен цикл
                if rang in or_mini and res[rule[1]] != 1:
                    if list(or_mini.values())[0] in buf:
                        max_rang = rang + 1  # чтоб потом знать до какого ранга обходить
                        or_mass.append({max_rang: rule[1]})
                        res[rule[1]] = 1
    return max_rang


def check_and(and_rules, rang, res, and_mass, or_mass, max_rang):
    """
        Searching new facts in AND_rules

            Params:
                and_rules(list) - list of all and_rules
                rang(int) - current rang, where we are searching new facts'
                res(list) - list with flags, where indexes = facts
                and_mass(list) - list of dicts, where key = rang, value = new fact
                max_rang(int) - current max_rang
            Returns:
                max_rang
    """

    for rule in and_rules:
        flag_and = 1
        # из условной части беру массив фактов
        buf = list(rule[0].values())[0]

        # сработает, если ранг = 1
        if rang in rule[0]:
            for i in range(len(buf)):
                if buf[i] not in facts:
                    flag_and = 0
                    break
            if flag_and == 1:
                # если все есть, то в res
                max_rang = 2  # чтоб потом знать до какого ранга обходить
                and_mass.append({rang + 1: rule[1]})
                res[rule[1]] = 1
        else:
            # Сбор фактов с большим рангом
            and_facts = []
            or_facts = []
            for fact in and_mass:
                and_facts.append(list(fact.values())[0])
            for fact in or_mass:
                and_facts.append(list(fact.values())[0])

            # Если ранг>1 и как минимум из and правил хоть одно ранее срабатывало
            for and_mini in and_mass:
                # Если из части "then" уже добавлен, то нового факта нет, но возможен цикл
                if res[rule[1]] != 1 and rang in and_mini:
                    for i in range(len(buf)):
                        # Хоть 1 факт не совпал - дропаем
                        if buf[i] not in facts and buf[i] not in and_facts and buf[i] not in or_facts:
                            flag_and = 0
                            break
                    if flag_and == 1:
                        # если все есть, то в res
                        max_rang = max(rang + 1, max_rang)
                        and_mass.append({rang + 1: rule[1]})
                        res[rule[1]] = 1
    return max_rang


def check_not(not_rules, res):
    """
        Searching new facts in not_rules

            Params:
                not_rules(list) - list of all not_rules
                res(list) - list with flags, where indexes = facts
    """
    for rule in not_rules:
        flag = 1
        # из условной части беру массив фактов
        buf = list(rule[0].values())[0]
        for i in range(len(rule[0])):
            # Если где-то есть, то дропаем
            if buf[i] in facts or buf[i] in res:
                flag = 0
                break
        if flag == 1:
            res[rule[1]] = 1


def main():
    """
        Main func, where in cycle searches new facts for all ranges
        Returns:
            res_facts(list) - list of all facts in knowledge base
    """
    res = [None] * 10100
    res_facts = []
    or_mass = []
    and_mass = []
    rang = 1  # начальный ранг
    max_rang = 1  # максимальный ранг

    not_rules, and_rules, or_rules = neg_or_pos_rules(rules)
    # Факты только появляются, этот тип противоречий не будет расти с ростом бз
    controversy_not_a_b_not_b_a(not_rules)

    flag_time = time()
    while rang <= max_rang:
        # каждый раз изменяется пул фактов, заново ищем противоречия
        controversy_ab_not_ab(not_rules, and_rules, or_rules)

        max_rang = max(check_or(or_rules, rang, res, or_mass, max_rang),
                       check_and(and_rules, rang, res, and_mass, or_mass, max_rang))

        check_not(not_rules, res)
        rang += 1

    index = 0
    while index < 10100:
        if res[index] == 1:
            res_facts.append(index)
        index += 1

    print(f"{M} facts validated vs {N} rules in {time() - flag_time} seconds")

    return res_facts


time_start = time()

if __name__ == '__main__':
    result = main()
    print(result)
