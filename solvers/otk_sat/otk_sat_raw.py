import random
import sys

if __name__ == '__main__':
    clauses = []
    count = 0
    for line in open(sys.argv[1]):

        if line[0] == 'c':
            continue
        if line[0] == 'p':
            n_vars = int(line.split()[2])
            lit_clause = [[] for _ in xrange(n_vars * 2 + 1)]
            continue

        clause = []
        for literal in line[:-2].split():
            literal = int(literal)
            clause.append(literal)
            lit_clause[literal].append(count)
        clauses.append(clause)
        count += 1

    max_flips = n_vars * 4

    while 1:

        interpretation = [i if random.random() < 0.5 else -i for i in xrange(n_vars + 1)]
        true_sat_lit = [0 for _ in clauses]
        for index, clause in enumerate(clauses):
            for lit in clause:
                if interpretation[abs(lit)] == lit:
                    true_sat_lit[index] += 1

        for _ in xrange(max_flips):

            unsatisfied_clauses_index = [index for index, true_lit in enumerate(true_sat_lit) if
                                         not true_lit]

            if not unsatisfied_clauses_index:
                print 's SATISFIABLE'
                print 'v ' + ' '.join(map(str, interpretation[1:])) + ' 0'
                sys.exit()

            clause_index = random.choice(unsatisfied_clauses_index)
            unsatisfied_clause = clauses[clause_index]

            break_min = sys.maxint
            best_literals = []
            for literal in unsatisfied_clause:

                break_score = 0

                for clause_index in lit_clause[-literal]:
                    if true_sat_lit[clause_index] == 1:
                        break_score += 1

                if break_score < break_min:
                    break_min = break_score
                    best_literals = [literal]
                elif break_score == break_min:
                    best_literals.append(literal)

            if break_min != 0 and random.random() < 0.4:
                best_literals = unsatisfied_clause

            lit_to_flip = random.choice(best_literals)

            for clause_index in lit_clause[lit_to_flip]:
                true_sat_lit[clause_index] += 1
            for clause_index in lit_clause[-lit_to_flip]:
                true_sat_lit[clause_index] -= 1

            interpretation[abs(lit_to_flip)] *= -1
