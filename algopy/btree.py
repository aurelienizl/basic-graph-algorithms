# -*- coding: utf-8 -*-
"""BTree Module.

BTree class definition and standard methods and functions.

*Warning:*  Set ``BTree.degree`` before any tree instanciation.

"""

from . import queue
from .queue import Queue


class BTree:
    """BTree class.

    Attributes:
        degree (int): Degree for all existing trees.
        keys (list[Any]): List of node keys.
        children (list[BTree]): List of children.
    """
    
    degree = None

    def __init__(self, keys=None, children=None):
        """BTree instance constructor.

        Args:
            keys (list[Any]).
            children (list[BTree])

        """
        self.keys = keys if keys else []
        self.children = children if children else []

    @property
    def nbkeys(self):
        """Number of keys in node.

        Returns:
            int.
        """
        return len(self.keys)


def __tolinear(B):
    '''
    B is a nonempty tree
    '''
    s = "(<"
    for i in range(B.nbkeys-1):        # keys
        s += str(B.keys[i]) + ','
    s += str(B.keys[-1]) + ">"

    for child in B.children:           # children
        s += __tolinear(child)
    s += ')'
    return s

def tolinear(B):
    if B == None:
        return ""
    else:
        return __tolinear(B)

#to build examples: linear rep -> B-tree (int keys)
def __fromlinear(s, i=0): 
    if i < len(s) and s[i] == '(':   #useless if string well-formed
        i = i + 2 # to pass the '(<'
        B = BTree()
        while s[i] != '>':
            key = ""            
            while not(s[i] in ',>'):
                key += s[i]
                i += 1
            B.keys.append(int(key))
            if s[i] == ',':
                i += 1 
        i += 1  # to pass the '>'
        B.children = []
        while s[i] != ')':
            (C, i) = __fromlinear(s, i)
            B.children.append(C)
        i = i + 1   # to pass the ')'
        return (B, i)
    else:
        return None

def from_linear(s, d):
    """Build a new tree from its _linear representation_.

    Args:
        s (str): the linear representation
        d (int): the degree

    Returns:
        BTree: New tree.
    """                
    BTree.degree = d
    (B, _) = __fromlinear(s)
    return B


# display version 1 : creation of the dot -> use graphviz.Source

def __node_dot(ref):
    """Gets node into dot proper shape.

    Args:
        ref (BTree).

    """

    s = str(id(ref)) + '[label="'
    for i in range(ref.nbkeys-1):
        s += str(ref.keys[i]) + ' | '
    s += str(ref.keys[ref.nbkeys-1])
    s +=  '"];\n'
    return s


def __link_dot(ref_a, ref_b):
    """Writes down link between two BTree nodes in dot format.

    Args:
        ref_A (BTree).
        ref_B (BTree).

    """

    return "   " + str(id(ref_a)) + " -- " + str(id(ref_b)) + ";\n"


def dot(ref):
    """Writes down dot format of tree.

    Args:
        ref (BTree).

    Returns:
        str: String storing dot format of BTree.

    """

    s = "graph " + str(ref.degree) + " {\n"
    s += "node [shape = record, height=.1];\n"
    q = Queue()
    q.enqueue(ref)
    s += __node_dot(ref)
    while not q.isempty():
        ref = q.dequeue()
        for child in ref.children:
            s += __node_dot(child)
            s += __link_dot(ref, child)
            q.enqueue(child)
    s += "}"
    return s

def display(ref, *args, **kwargs):
    """Render a BinTree to for in-browser display.

    *Warning:* Made for use within IPython/Jupyter only.

    Extra non-documented arguments are passed to the ``dot`` function and
    complyt with its documentation.

    Args:
        ref (BinTree).

    Returns:
        Source: Graphviz wrapper object for BinTree rendering.

    """

    # Ensure all modules are available
    try:
        from graphviz import Source
        from IPython.display import display
    except:
        raise Exception("Missing module: graphviz.")
    # Generate dot and return display object
    dot_source = dot(ref, *args, **kwargs)
    display(Source(dot_source))

# display version 2 : creation of a graphviz.Graph object
    
def displaySVG(ref, filename='temp'):
    """Render a BTree to SVG format.

    *Warning:* Made for use within IPython/Jupyter only.

    Args:
        ref (BTree).
        filename (str): Temporary filename to store SVG output.

    Returns:
        SVG: IPython SVG wrapper object for BTree.

    """

    # Ensure all modules are available
    try:
        from graphviz import Graph, Source
        from IPython.display import SVG
    except:
        raise Exception("Missing module: graphviz and/or IPython.")
    # Traverse Btree and generate temporary Graph object
    output_format = 'svg'
    graph = Graph(filename, format=output_format)
    q = Queue()
    if ref is not None:
        q.enqueue(ref)
    while not q.isempty():
        ref = q.dequeue()

        node_label = ''
        for i in range(ref.nbkeys-1):
            node_label += str(ref.keys[i]) + ' | '
        node_label += str(ref.keys[ref.nbkeys - 1])
        graph.node(str(id(ref)), label=node_label,
                   style="rounded", shape="record")

        for child in ref.children:
            graph.edge(str(id(ref)), str(id(child)))
            q.enqueue(child)
    # Render to temporary file and SVG object
    graph.render(filename=filename, cleanup=True)
    return SVG(filename + '.' + output_format)



