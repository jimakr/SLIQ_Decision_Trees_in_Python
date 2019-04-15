def algorithm_u(ns, m):
    def visit(n, a):
        ps = [[] for i in range(m)]
        for j in range(n):
            ps[a[j + 1]].append(ns[j])
        return ps

    def f(mu, nu, sigma, n, a):
        if mu == 2:
            yield visit(n, a)
        else:
            for v in f(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v
        if nu == mu + 1:
            a[mu] = mu - 1
            yield visit(n, a)
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                yield visit(n, a)
        elif nu > mu + 1:
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = mu - 1
            else:
                a[mu] = mu - 1
            if (a[nu] + sigma) % 2 == 1:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v

    def b(mu, nu, sigma, n, a):
        if nu == mu + 1:
            while a[nu] < mu - 1:
                yield visit(n, a)
                a[nu] = a[nu] + 1
            yield visit(n, a)
            a[mu] = 0
        elif nu > mu + 1:
            if (a[nu] + sigma) % 2 == 1:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] < mu - 1:
                a[nu] = a[nu] + 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = 0
            else:
                a[mu] = 0
        if mu == 2:
            yield visit(n, a)
        else:
            for v in b(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v

    n = len(ns)
    a = [0] * (n + 1)
    for j in range(1, m + 1):
        a[n - m + j] = j - 1
    return f(m, n, 0, n, a)


listed_data = [[20, 1],
               [20, 3],
               [20, 10],
               [25, 6],
               [25, 8],
               [30, 2],
               [30, 4],
               [30, 7],
               [40, 5],
               [40, 9]]

family_data = [['eggamos', 3],
               ['eggamos', 6],
               ['agamos', 4],
               ['agamos', 5],
               ['agamos', 10],
               ['diazeumenos', 1],
               ['diazeumenos', 2],
               ['diazeumenos', 7],
               ['diazeumenos', 8],
               ['diazeumenos', 9]]

dictrid = {1: 1,
           2: 1,
           3: 0,
           4: 1,
           5: 1,
           6: 0,
           7: 1,
           8: 1,
           9: 1,
           10: 0, }


def gini_list(list_a, list_b, classlist):
    n1 = len(list_a)
    n2 = len(list_b)

    if n1 == 0 or n2 == 0:
        return 2

    n = n1 + n2
    pos_a = 0.0
    pos_b = 0.0

    for item in list_a:
        if classlist[item[1]] == 1:
            pos_a += 1

    for item in list_b:
        if classlist[item[1]] == 1:
            pos_b += 1

    neg_a = n1 - pos_a
    neg_b = n2 - pos_b
    gini_a = 1 - float((pos_a*pos_a + neg_a*neg_a)/(n1*n1))
    gini_b = 1 - float((pos_b*pos_b + neg_b*neg_b)/(n2*n2))
    return (n1/n)*gini_a + (n2/n)*gini_b


def split_list(index, list_a):
    #leafset = {5, 3, 4, 10, 6, 8, 1}
    right = list_a[index:]
    left = list_a[0:index]
    #left = [item for item in list_a[0:index] if leafset.__contains__(item[1])]
    return left, right


def split_atribute(list_a):
    last = list_a[0][0]
    index = -1
    best_gini = 2
    for item in list_a:
        index += 1
        if item[0] != last:
            last = item[0]
            left, right = split_list(index, list_a)
            gini = gini_list(left, right, dictrid)
            if best_gini > gini:
                best_gini = gini

    return best_gini


def split_list_descrete(list_a, split):
    #split = [[1,2],[3,4]]
    left = []
    right = []
    for item in list_a:
        if split[0].__contains__(item[0]):
            left.append(item)
        else:
            right.append(item)

    return left, right


def split_atribute_descrete(list_a):
    last = list_a[0][0]
    uniques = [last]
    best_gini = 2
    for item in list_a:
        if item[0] != last:
            last = item[0]
            uniques.append(item[0])

    sets = list(algorithm_u(uniques, 2))

    for split in sets:
        a, b = split_list_descrete(list_a, split)
        gini = gini_list(a, b, dictrid)
        if best_gini > gini:
            best_gini = gini

    return best_gini


print(split_atribute_descrete(family_data))
print(split_atribute(listed_data))
