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

def __buildgraph(str1, str2, k):
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
            if __buildgraph(res[i], res[j], k) == 1:
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


def __ladder_v1(G, start, end, p):
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


def ladder_v1(G, start, end):
    """ Return a *ladder* to the *doublet* (start, end) in G

    """
    (p, L) = ([None] * G.order, [])
    __ladder_v1(G, start, end, p)
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


def ladder_v2(G, start, end):
    """

    """
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


def __longestdoublet_v1(G, s, p, start, end, max):
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


def longestdoublet_v1(G):
    """
    Find in G one of the most difficult *d hj oublets* (that has the longest *ladder*)

    """
    (start, end, max) = ("", "", 0)
    for s in range(G.order):
        p = [None] * G.order
        (val1, val2) = __longestdoublet_v1(G, s, p, start, end, max)
        for el in p:
            if el is not None and el > max:
                (start, end, max) = (val2, val1, el)
    return (start, end, max)


def __longestdoublet_v2(G, val):
    (M, q, M[G.labels.index(val)]) = ([-1] * G.order, queue.Queue(), 1)
    q.enqueue(G.labels.index(val))
    while not q.isempty():
        x = q.dequeue()
        for el in G.adjlists[x]:
            if M[el] == -1:
                M[el] = M[x] + 1
                q.enqueue(el)
    return (val, M[x], G.labels[x])


def longestdoublet_v2(G):
    """ Find in G one of the most difficult *d hj oublets* (that has the longest *ladder*)

    """
    local_max = 0
    for i in range(G.order):
        (first, dst, last) = __longestdoublet_v2(G, G.labels[i])
        local_max2 = max(dst, local_max)
        if local_max2 > local_max:
            (start, maxi, end, local_max) = (first, dst, last, local_max2)
    return (start, end, maxi)


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


def more_than_dist(G, src, dist):
    """
    This function returns all nodes away from *dist* from the cource
    """
    M = [None] * G.order
    L = []
    M[src] = 0
    q = queue.Queue()
    q.enqueue(src)
    while not q.isempty():
        x = q.dequeue()
        for y in G.adjlists[x]:
            if M[y] == None:
                M[y] = M[x] + 1
                q.enqueue(y)
                if M[y] > dist:
                    L.append(y)
    return L


def just_than_dist(G, src, dist):
    """
    This function return all nodes away from dist to source
    """
    M = [None] * G.order
    L = []
    q = queue.Queue()
    q.enqueue(src)
    M[src] = 0
    while not q.isempty():
        x = q.dequeue()
        for y in G.adjlists[x]:
            if M[y] == None:
                M[y] = M[x] + 1
                if M[y] == dist:
                    L.append(y)
                elif M[y] > dist:
                    return L
                q.enqueue(y)
    return L


def interval(G, src, min, max):
    """
    This function returns all nodes that are at a distance between min and max from src
    """
    M = [None] * G.order
    M[src] = 0
    L = []
    q = queue.Queue()
    q.enqueue(src)
    while not q.isempty():
        x = q.dequeue()
        for y in G.adjlists[x]:
            if M[y] == None:
                M[y] = M[x] + 1
                if M[y] >= min and M[y] <= max:
                    L.append(y)
                elif M[y] > max:
                    return L
                q.enqueue(y)
    return L


def levels(G, src):
    M = [None] * G.order
    M[src] = 0
    LEVELS = []
    DIST = 0
    L = []
    q = queue.Queue()
    q.enqueue(src)
    while not q.isempty():
        x = q.dequeue()
        if M[x] > DIST:
            L.append(LEVELS)
            LEVELS = [x]
            DIST += 1
        else:
            LEVELS.append(x)
        for y in G.adjlists[x]:
            if M[y] == None:
                M[y] = M[x] + 1
                q.enqueue(y)
    return L
