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


def __acyclic(G, s, M):
    M[s] = 1
    for y in G.adjlists[s]:
        if M[y] == None:
            if not __acyclic(G, y, M):
                return False
            else:
                if M[y] != 2:
                    return False
    M[s] = 2
    return True


def acyclic(G):
    """
    Return a boolean, false if a back edge was found
    """
    M = [None] * G.order
    for s in range(G.order):
        if M[s] == None:
            if not __acyclic(G, s, M):
                return False
    return True


def __is_cyclic(G, s):
    P = [None] * G.order
    q = queue.Queue()
    q.enqueue(s)
    while not q.isempty():
        x = q.dequeue()
        for y in G.adjlists[x]:
            if y == s and not x == s:
                return True
            elif P[y] == None:
                P[y] = 1
                q.enqueue(y)
    return False


def is_cyclic(G):
    """
    Return a boolean, true if a back edge was found //WARNING : THIS FUNCTION IS PROBABLY NOT WORKING IN EVERY CASES ! REVIEW NEDEED
    """
    M = [None] * G.order
    for s in range(G.order):
        if M[s] == None:
            M[s] = 1
            if __is_cyclic(G, s):
                return True
    return False
