# -*- coding: utf-8 -*-
__license__ = 'Junior (c) EPITA'
__docformat__ = 'reStructuredText'
__revision__ = '$Id: doublets.py 2022-04-11'

"""
Doublet homework
2022-04
@author: aurelien.izoulet
"""

from algopy import graph, queue


def str_diff(str1, str2, k):
    diff = 0
    for i in range(k):
        if str1[i] != str2[i]:
            diff += 1
        if diff > 1:
            return diff
    return diff


def buildgraph(filename, k):
    """Build and return a graph with words of length k from the lexicon in filename

    """
    with open(filename) as file_in:
        res = []
        for line in file_in:
            if (len(line) - 1) == k:
                line = line[:-1]
                res.append(line)
    G = graph.Graph(len(res), False, res)
    for i in range(len(res)):
        for j in range(i + 1, len(res)):
            if str_diff(res[i], res[j], k) == 1:
                G.addedge(i, j)
    return G


def mostconnected(G):
    """ Return the list of words that are directly linked to the most other words in G

    """
    (res, maxi) = ([], 0)
    for i in range(G.order):
        if maxi < len(G.adjlists[i]):
            res = []
            maxi = len(G.adjlists[i])
        if len(G.adjlists[i]) == maxi:
            res.append(G.labels[i])
    return res


def ischain(G, L):
    """ Test if L (word list) is a valid elementary *chain* in the graph G

    """
    for i in range(len(L)):
        if L[i] not in G.labels:
            return False
        for j in range(i+1, len(L)):
            if L[i] == L[j]:
                return False
    is_chain = True
    for i in range(len(L) - 1):
        if is_chain:
            one = G.labels.index(L[i])
            two = G.labels.index(L[i+1])
            chain = two in G.adjlists[one]
        else:
            return False
    return True


def __alldoublets(G, x, M, L):
    M[x] = True
    for y in G.adjlists[x]:
        if not M[y]:
            __alldoublets(G, y, M, L)
            L.append(G.labels[y])


def alldoublets(G, start):
    """ Return the list of all words that can form a *doublet* with the word start in the lexicon in G

    """
    L = []
    M = [False] * G.order
    __alldoublets(G, G.labels.index(start), M, L)
    return L


def __nosolution(G, x, P):
    P[x] = True
    for i in G.adjlists[x]:
        if not P[i]:
            __nosolution(G, i, P)


def nosolution(G):
    """ Return a *doublet* without solution in G, (None, None) if none

    """
    P = [False] * G.order
    __nosolution(G, 0, P)
    index = -1
    index2 = -1
    for i in range(G.order):
        if not P[i] and index == -1:
            index = i
            if index2 != -1:
                return (G.labels[index], G.labels[index2])
        elif index2 == -1:
            index2 = i
            if index != -1:
                return (G.labels[index], G.labels[index2])
    return (None, None)


def __ladder(G, start, end, p):
    q = queue.Queue()
    q.enqueue(G.labels.index(start))
    p[G.labels.index(start)] = -1
    while not q.isempty():
        x = q.dequeue()
        if G.labels[x] == end:
            return
        for y in G.adjlists[x]:
            if p[y] == None:
                p[y] = x
                q.enqueue(y)


def ladder(G, start, end):
    """ Return a *ladder* to the *doublet* (start, end) in G

    """
    (p, L) = ([None] * G.order, [])
    __ladder(G, start, end, p)
    if p[G.labels.index(end)] == None:
        return []
    else:
        i = p[G.labels.index(end)]
        while i != -1:
            L.append(G.labels[i])
            i = p[i]
        L.reverse()
        L.append(end)
        return L


"""def __BFS_forest(G, s, p, start, end, max):
    q = queue.Queue()
    start = G.labels[s]
    q.enqueue(s)
    p[s] = 1   # root
    while not q.isempty():
        x = q.dequeue()
        for y in G.adjlists[x]:
            if p[y] == None:
                q.enqueue(y)  # tree edge x -> y
                p[y] = p[x] + 1
                end = G.labels[y]
    return (start, end)

def longestdoublet(G):
    (start, end, max) = ("", "", 0)
    for s in range(G.order):
        p = [None] * G.order
        (val1, val2) = __BFS_forest(G, s, p, start, end, max)
        for el in p:
            if el is not None and el > max:
                (start, end, max) = (val2, val1, el)
    return (start, end, max)    # represents the spanning forest"""


def __longestdoublet(G, val):
    (M, q, M[G.labels.index(val)]) = ([-1] * G.order, queue.Queue(), 1)
    q.enqueue(G.labels.index(val))
    while not q.isempty():
        x = q.dequeue()
        for el in G.adjlists[x]:
            if M[el] == -1:
                M[el] = M[x] + 1
                q.enqueue(el)
    return (val, M[x], G.labels[x])


def longestdoublet(G):
    """ Find in G one of the most difficult *d hj oublets* (that has the longest *ladder*)

    """
    local_max = 0
    for i in range(G.order):
        (first, dst, last) = __longestdoublet(G, G.labels[i])
        local_max2 = max(dst, local_max)
        if local_max2 > local_max:
            (start, maxi, end, local_max) = (first, dst, last, local_max2)
    return (start, end, maxi)


def isomorphic(G1, G2):
    """Test if G1 and G2 (graphs of same length words) are isomorphic

    """
    for i in range(G1.order):
        if G1.labels[i] not in G2.labels:
            return False
        else:
            if len(G1.adjlists[i]) != len(G2.adjlists[G2.labels.index(G1.labels[i])]):
                return False
            for j in G1.adjlists[i]:
                if G1.labels[j] not in G2.labels:
                    return False
                else:
                    if G2.labels.index(G1.labels[j]) not in G2.adjlists[G2.labels.index(G1.labels[i])]:
                        return False
    return True


def __components(G, M, S):
    q = queue.Queue()
    q.enqueue(S)
    while not q.isempty():
        x = q.dequeue()
        for y in G.adjlists[x]:
            if M[y] == None:
                M[y] = M[x]
                q.enqueue(y)


def components(G):
    """
    The function returns the pair:

    Number of connected components,
    The component vector: for each vertex the number of the component it belongs to.

    """
    M = [None] * G.order
    i = 0
    for s in range(G.order):
        if M[s] == None:
            i += 1
            M[s] = i
            __components(G, M, s)
    return [[i], [M]]


def __bipartite(G, s, M):
    q = queue.Queue()
    q.enqueue(s)
    while not q.isempty():
        x = q.dequeue()
        for y in G.adjlists[x]:
            if M[y] == None:
                M[y] = -M[x]
                q.enqueue(y)
            if M[y] == M[x]:
                return False
    return True


def bipartite(G):
    """
    A bipartite graph is an undirected graph (multigraphe), 
    where S can be partitioned into two sets S1 and S2:

    Such that:
        ∀{u,v}∈A
        either u∈S1 and v∈S2
        or u∈S2 and v∈S1.

    This function return true if a graph is bipartite or false if it's not. 
    """
    M = [None] * G.order
    for s in range(G.order):
        if M[s] == None:
            M[s] = 1
            if not __bipartite(G, s, M):
                return False
    return True


def path_bfs(G, start, end):
    M = [None] * G.order
    M[start] = -1
    q = queue.Queue()
    q.enqueue(start)
    while not q.isempty():
        x = q.dequeue()
        for y in G.adjlists[x]:
            if M[y] == None:
                M[y] = x
                q.enqueue(y)
    if M[start] == None or M[end] == None:
        return []
    else:
        L = []
        while end != -1:
            L.append(end)
            end = M[end]
        L.reverse()
        return L


def test():
    
    print("###############################################################################")
    print("###                              PYTHON TESTS                               ###")
    print("###############################################################################")
    import time




    print("###############################################################################")
    start = time.time()

    G3 = buildgraph("lexicons/lex_some.txt", 3)
    G4 = buildgraph("lexicons/lex_some.txt", 4)

    print("Most connected : ")

    if mostconnected(G4) == ['ford', 'fork'] and mostconnected(G3) == ['oat', 'sat']:
        print("ok")
    else:
        print("error !")
    print()

    end = time.time()
    print("The time of execution of above function is :", end-start)
    print()
    print("###############################################################################")
    start = time.time()

    print("Is chain : ")

    if ischain(G3, ['ape', 'apt', 'opt', 'oat', 'mat', 'man']) and \
        not ischain(G3, ['man', 'mat', 'sat', 'sit', 'pit', 'pig']) and\
        not ischain(G3, ['ape', 'apt', 'opt', 'oat', 'mat', 'oat', 'mat', 'man']):
        print("ok")
    else:
        print("error !")
    print()

    end = time.time()
    print("The time of execution of above function is :", end-start)
    print()
    print("###############################################################################")
    start = time.time()

    print("All doublets :")

    if all(item in alldoublets(G3, "pen") for item in 
        ['eel', 'een', 'ell', 'ilk', 'ill', 'ink', 'pie', 'pig', 'pin', 'pit']):
        print("ok")
    else:
        print("error !")
    print()

    end = time.time()
    print("The time of execution of above function is :", end-start)
    print()
    print("###############################################################################")
    start = time.time()

    print("No solution : ")

    if all(item in nosolution(G3) for item in ('ape', 'eel')) and nosolution(G4) == (None, None):
        print("ok")
    else:
        print("error !")
    print()

    end = time.time()
    print("The time of execution of above function is :", end-start)
    print()
    print("###############################################################################")
    start = time.time()

    print("Ladder : ")

    if all(item in ladder(G3, "ape", "man") for item in ['ape', 'apt', 'opt', 'oat', 'mat', 'man']) \
        and ladder(G3, "man", "pig") == []\
        and all(item in ladder(G4, "work", "food") for item in ['work', 'fork', 'ford', 'food']):
        print("ok")
    else:
        print("error !")
    print()

    end = time.time()
    print("The time of execution of above function is :", end-start)
    print()
    print("###############################################################################")
    start = time.time()

    print("Longest Doublet : ")

    if (all(item in longestdoublet(G3) for item in ('ape', 'one', 10)) or\
        all(item in longestdoublet(G3) for item in ('one', 'tea', 10)))\
            and all(item in longestdoublet(G4) for item in ('tree', 'five', 13)):
        print("ok")
    else:
        print("error !")
    print()

    end = time.time()
    print("The time of execution of above function is :", end-start)

