import sys


def _move_last_to_empty(domain_file, d1, p1, p2):
    domain_file.write("Name: M" + d1 + p1 + p2 + "-last-to-empty\n")

    domain_file.write("pre: OnPeg(" + p1 + "," + d1 + ") ")
    domain_file.write("OnDisk(" + d1 + ",None) ")
    domain_file.write("OnTop(" + p1 + "," + d1 + ") ")
    domain_file.write("OnTop(" + p2 + ",None) \n")

    domain_file.write("add: OnPeg(" + p2 + "," + d1 + ") ")
    domain_file.write("OnTop(" + p1 + ",None) ")
    domain_file.write("OnTop(" + p2 + "," + d1 + ") \n")

    domain_file.write("del: OnPeg(" + p1 + "," + d1 + ") ")
    domain_file.write("OnTop(" + p1 + "," + d1 + ") ")
    domain_file.write("OnTop(" + p2 + ",None) \n")


def _move_last_to_not_empty(domain_file, d1, d2, p1, p2):
    domain_file.write("Name: M" + d1 + p1 + p2 + "-last-to-not-empty" + d2 + "\n")

    domain_file.write("pre: OnPeg(" + p1 + "," + d1 + ") ")
    domain_file.write("OnPeg(" + p2 + "," + d2 + ") ")
    domain_file.write("OnDisk(" + d1 + ",None) ")
    domain_file.write("OnTop(" + p1 + "," + d1 + ") ")
    domain_file.write("OnTop(" + p2 + "," + d2 + ") ")
    domain_file.write("Smaller(" + d1 + "," + d2 + ") \n")

    domain_file.write("add: OnPeg(" + p2 + "," + d1 + ") ")
    domain_file.write("OnDisk(" + d1 + "," + d2 + ") ")
    domain_file.write("OnTop(" + p1 + ",None) ")
    domain_file.write("OnTop(" + p2 + "," + d1 + ") \n")

    domain_file.write("del: OnPeg(" + p1 + "," + d1 + ") ")
    domain_file.write("OnDisk(" + d1 + ",None) ")
    domain_file.write("OnTop(" + p1 + "," + d1 + ") ")
    domain_file.write("OnTop(" + p2 + "," + d2 + ") \n")


def _move_not_last_to_empty(domain_file, d1, d2, p1, p2):
    domain_file.write("Name: M" + d1 + p1 + p2 + "-not-last-to-empty" + d2 + "\n")

    domain_file.write("pre: OnPeg(" + p1 + "," + d1 + ") ")
    domain_file.write("OnPeg(" + p1 + "," + d2 + ") ")
    domain_file.write("OnDisk(" + d1 + "," + d2 + ") ")  # d1 on d2
    domain_file.write("OnTop(" + p1 + "," + d1 + ") ")
    domain_file.write("OnTop(" + p2 + ",None) \n")

    domain_file.write("add: OnPeg(" + p2 + "," + d1 + ") ")
    domain_file.write("OnDisk(" + d1 + ",None) ")
    domain_file.write("OnTop(" + p2 + "," + d1 + ") ")
    domain_file.write("OnTop(" + p1 + "," + d2 + ") \n")

    domain_file.write("del : OnPeg(" + p1 + "," + d1 + ") ")
    domain_file.write("OnTop(" + p2 + ",None) ")
    domain_file.write("OnTop(" + p1 + "," + d1 + ") ")
    domain_file.write("OnDisk(" + d1 + "," + d2 + ") \n")


def _move_not_last_to_not_empty(domain_file, d1, d2, d3, p1, p2):
    domain_file.write("Name: M" + d1 + p1 + p2 +
                      "-not-last-to-not-empty-" + d2 + d3 + "\n")
    # d1 on d3 on p1     d2 on p2
    domain_file.write("pre: OnPeg(" + p1 + "," + d1 + ") ")
    domain_file.write("OnPeg(" + p2 + "," + d2 + ") ")
    domain_file.write("OnPeg(" + p1 + "," + d3 + ") ")
    domain_file.write("OnDisk(" + d1 + "," + d3 + ") ")
    domain_file.write("OnTop(" + p1 + "," + d1 + ") ")
    domain_file.write("OnTop(" + p2 + "," + d2 + ") ")
    domain_file.write("Smaller(" + d1 + "," + d2 + ") \n")
    # now d3 on p1     d1 on d2 on p2
    domain_file.write("add: OnPeg(" + p2 + "," + d1 + ") ")
    domain_file.write("OnDisk(" + d1 + "," + d2 + ") ")
    domain_file.write("OnTop(" + p1 + "," + d3 + ") ")
    domain_file.write("OnTop(" + p2 + "," + d1 + ") \n")

    domain_file.write("del: OnPeg(" + p1 + "," + d1 + ") ")
    domain_file.write("OnDisk(" + d1 + "," + d3 + ") ")
    domain_file.write("OnTop(" + p1 + "," + d1 + ") ")
    domain_file.write("OnTop(" + p2 + "," + d2 + ") \n")


def _write_propositions(disks, pegs, domain_file):
    all_combs = ["OnPeg(" + p + "," + d + ")" for d in disks for p in pegs]
    smaller = ["Smaller(" + disks[i] + "," + disks[j] + ")" for i in range(len(disks)) for
               j in range(i + 1, len(disks))]
    disk_on_d = ["OnDisk(" + disks[i] + "," + disks[j] + ")" for i in range(len(disks)) for
                 j in range(i + 1, len(disks))]
    disk_on_d += ["OnDisk(" + d + ",None)" for d in disks]
    on_tops = ["OnTop(" + p + "," + d + ")" for d in disks + ['None'] for p in pegs]

    domain_file.write(" ".join(smaller + disk_on_d + all_combs + on_tops))
    domain_file.write("\n")


def _write_actions(disks, pegs, domain_file):
    for d1_ in range(len(disks)):
        for p1_ in range(len(pegs)):
            for p2_ in range(len(pegs)):
                if p1_ == p2_:
                    continue
                d1 = disks[d1_]
                p1 = pegs[p1_]
                p2 = pegs[p2_]
                # case 1: move last to empty
                _move_last_to_empty(domain_file, d1, p1, p2)
                # case 2: move last to not-empty
                for d2_ in range(d1_ + 1, len(disks)):
                    d2 = disks[d2_]
                    _move_last_to_not_empty(domain_file, d1, d2, p1, p2)
                    # case 3: move not last to empty
                    _move_not_last_to_empty(domain_file, d1, d2, p1, p2)
                    # case 4: move not last to not-empty
                    for d3_ in range(d1_ + 1, len(disks)):
                        if d1_ == d3_ or d2_ == d3_:
                            continue
                        d3 = disks[d3_]
                        _move_not_last_to_not_empty(domain_file, d1, d2, d3, p1, p2)


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    "*** YOUR CODE HERE ***"
    if n_ < 1 or m_ < 1:
        domain_file.close()
        return
    domain_file.write("Propositions:\n")
    _write_propositions(disks, pegs, domain_file)
    domain_file.write("Actions:\n")
    _write_actions(disks, pegs, domain_file)
    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_,
                        'w')  # use problem_file.write(str) to write to problem_file
    "*** YOUR CODE HERE ***"
    if n_ < 1 or m_ < 1:
        problem_file.close()
        return

    problem_file.write("Initial state: ")
    for d_ in range(len(disks)):
        if d_ == 0:
            problem_file.write("OnTop(" + pegs[0] + "," + disks[d_] + ") ")
        else:
            problem_file.write("OnDisk(" + disks[d_ - 1] + "," + disks[d_] + ") ")
        problem_file.write("OnPeg(" + pegs[0] + "," + disks[d_] + ") ")
    problem_file.write("OnDisk(" + disks[-1] + ",None) ")

    for i in range(len(disks)):
        for j in range(i):
            problem_file.write("Smaller(" + disks[j] + "," + disks[i] + ") ")

    for p_ in range(1, len(pegs)):
        problem_file.write("OnTop(" + pegs[p_] + ",None) ")
    problem_file.write("\n")

    problem_file.write("Goal state: ")
    for d_ in range(len(disks)):
        if d_ == 0:
            problem_file.write("OnTop(" + pegs[-1] + "," + disks[d_] + ") ")
        else:
            problem_file.write("OnDisk(" + disks[d_ - 1] + "," + disks[d_] + ") ")
        problem_file.write("OnPeg(" + pegs[-1] + "," + disks[d_] + ") ")

    problem_file.write("OnDisk(" + disks[-1] + ",None) ")
    problem_file.write("\n")

    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
