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
N = 100000
M = 1000
rules = generate_simple_rules(100, 4, N)
facts = generate_rand_facts(100, M)
print("%d rules generated in %f seconds" % (N, time() - time_start))


# load and validate rules
# YOUR CODE HERE

def neg_or_pos_rules(rules):
    negative = []
    and_rules = []
    or_rules = []

    for rule in rules:
        keys = rule['if'].keys()
        if 'not' in keys:
            neg = (tuple(tuple(rule['if'].values())[0]), rule['then'])
            negative.append(neg)
        elif 'and' in keys:
            and_rule = (tuple(tuple(rule['if'].values())[0]), rule['then'])
            and_rules.append(and_rule)
        elif 'or' in keys:
            or_rule = (tuple(tuple(rule['if'].values())[0]), rule['then'])
            or_rules.append(or_rule)

    negative = list(set(negative))
    and_rules = list(set(and_rules))
    or_rules = list(set(or_rules))
    return [and_rules, or_rules, negative]


def controversy_ab_not_ab(negative, and_rules, or_rules):
    for neg in negative:
        for pos in list(set(and_rules + or_rules)):
            if neg[1] == pos[1] and list(neg[0]).sort == list(pos[0]).sort:
                negative.remove(neg)
                if pos in and_rules:
                    and_rules.remove(pos)
                else:
                    or_rules.remove(pos)
    return [negative, and_rules, or_rules]


def check_and(and_rules):
    new_facts = []

    for rule in and_rules:
        flag_and = 1
        for i in range(len(rule[0])):
            if rule[0][i] not in facts:
                flag_and = 0
                break
        if flag_and == 1:
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
    for rule in not_rules:
        flag = 1
        for i in range(len(rule[0])):
            if rule[0][i] in facts:
                flag = 0
                break
        if flag == 1:
            new_facts.append(rule[1])
    return new_facts


def main():
    and_rules, or_rules, neg = neg_or_pos_rules(rules)
    neg, and_rules, or_rules = controversy_ab_not_ab(neg, and_rules, or_rules)

    new_facts_and = check_and(and_rules)
    new_facts_or = check_or(or_rules)
    new_facts_not = check_not(neg)

    return set(new_facts_or + new_facts_not + new_facts_and + facts)


# check facts vs rules
time_start = time()

# YOUR CODE HERE

if __name__ == '__main__':
    res_facts = main()

print("%d facts validated vs %d rules in %f seconds" % (M, N, time() - time_start))
print(res_facts)
