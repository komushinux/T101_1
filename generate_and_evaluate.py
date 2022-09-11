import bisect
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


# samples:
print(generate_simple_rules(100, 4, 10))
print(generate_random_rules(100, 4, 10))
print(generate_stairway_rules(100, 4, 10, ["or"]))
print(generate_ring_rules(100, 4, 10, ["or"]))

# generate rules and facts and check time
time_start = time()
N = 100000
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
            neg = [list(rule['if'].values())[0], list(rule['then'])]
            negative.append(neg)
        else:
            pos = [list(rule['if'].values())[0], list(rule['then'])]
            positive.append(pos)

    negative = list(set(negative))
    positive = list(set(positive))

    negative.sort(key=lambda s: len(s[0]))
    positive.sort(key=lambda s: len(s[0]))

    return[negative, positive]


def controversy_ab_not_ab(negative, positive):
    for neg in negative:
        for pos in positive:
            if neg[0] == pos[0] and neg[1] == pos[1]:
                negative.remove(neg)
                positive.remove(pos)
                break
            if len(neg[0]) > len(pos[0]):
                break
    return [negative, positive]

def controversy_not_ab_not_ca(negative):
    flag = 0
    for neg_i in negative:
        for neg_j in negative:
            if len(neg_j[0] > 1):
                break
            if neg_i[0] == neg_j[1]:
                negative.remove(neg_j)
                negative.remove(neg_i)
                flag = 1
                break
        if flag == 1:
            flag = 0
            break
    return negative


def and_or_or_rules(rules):
    and_rules = []
    or_rules = []
    for rule in rules:
        if 'and' in rule['if'].keys():
            and_rule = [list(rule['if'].values())[0], list(rule['then'])]
            and_rules.append(and_rule)
        else:
            or_rule = [list(rule['if'].values())[0], list(rule['then'])]
            and_rules.append(or_rule)

    and_rules = list(set(and_rules))
    or_rules = list(set(or_rules))

    return [and_rules, or_rules]


def check_and(and_rules):
    new_facts = []
    flag = 1
    for rule in and_rules:
        for i in range(len(rule[0])):
            if rule[0][i] not in facts:
                flag = 0
                break
        if flag == 1:
            new_facts.append(rule[1])
    return new_facts


def check_or(or_rules):
    new_facts = []
    for rule in or_rules:
        for i in range(len(rule[0])):
            if rule[0][i] in facts:
                new_facts.append(rule[1])
                break
    return new_facts


def check_not(not_rules):
    new_facts = []
    flag = 1
    for rule in not_rules:
        for i in range(len(rule[0])):
            if rule[0][i] in facts:
                flag = 0
                break
        if flag == 1:
            new_facts.append(rule[1])
    return new_facts


def main():



# check facts vs rules
time_start = time()

# YOUR CODE HERE

if __name__ == '__main__':
    main()

print("%d facts validated vs %d rules in %f seconds" % (M, N, time() - time_start))
