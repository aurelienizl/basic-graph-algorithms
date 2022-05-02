# -*- coding: utf-8 -*-
"""General Tree module.


*Warning:* All the functions defined in this module are assumed to receive a non-None
value for their ``ref/T`` parameter.

"""

from . import queue
from .queue import Queue


class Tree:
    """Simple class for general tree.

    Attributes:
        key (Any): Node key.
        children (List[Tree]): Node children.

    """
    def __init__(self, key, children=None):
        """Init general tree, ensure children are properly set.

        Args:
            key (Any).
            children (List[Tree]).

        """
        self.key = key
        if children == None:
            self.children = []
        else:
            self.children = children

    @property
    def nbchildren(self):
        """Number of children of node."""

        return len(self.children)

###############################################################################
# Display

def dot(T):
    """Simple dot format of tree.

    Args:
        T (Tree).

    Returns:
        str: String storing dot format of tree.

    """

    s = "graph {\n"
    q = Queue()
    q.enqueue(T)
    s += str(id(T)) + '[label = "' + str(T.key) + '"]\n'
    while not q.isempty():
        T = q.dequeue()
        for child in T.children:
            s += str(id(child)) + '[label = "' + str(child.key) + '"]\n'
            s = s + "   " + str(id(T)) + " -- " + str(id(child)) + "\n"
            q.enqueue(child)
    s += "}"
    return s
    

def display(T):
    """Render a Tree for in-browser display.

    *Warning:* Made for use within IPython/Jupyter only.

    Args:
        T (Tree).

    Returns:
        Source: Graphviz wrapper object for tree rendering.

    """

    # Ensure all modules are available
    try:
        from graphviz import Source
        from IPython.display import display
    except:
        raise Exception("Missing module: graphviz.")
    # Generate dot and return display object
    dot_source = dot(T)
    display(Source(dot_source))
    
###############################################################################
# load and save
# use the linear representation: (o A1 A2 ... AN).

def to_linear(T):
    """Build the _linear representation_ of a tree.

    Args:
        T (Tree)

    Returns:
        str: the linear representation of T

    """        
    s = '(' + str(T.key)
    for child in T.children:
        s += to_linear(child)
    s += ')'
    return s

def save(T, filename):
    """save the linear representation of a tree in a text file.

    Args:
        T (Tree): the tree to save.
        filename (str): the new file

    """            
    fout = open(filename, mode='w')
    fout.write(to_linear(T))
    fout.close()
    
    
def __from_linear(s, i=0): 
        i += 1 # to skip the '('
        key = ""
        while s[i] != '(' and s[i] != ')':  # s[i] not in "()"
            key += s[i]
            i += 1
        T = tree.Tree(int(key), [])
        while s[i] != ')':  # s[i] == '('
            (C, i) = __from_linear(s, i)
            T.children.append(C)
        i += 1 # to skip the ')'
        return (T, i)

def from_linear(s):
    """Build a new tree from its _linear representation_.

    Args:
        str: the linear representation

    Returns:
        Tree: New tree.
    """            
    return __from_linear(s)[0]

def load(filename):
    """Build a new tree from a text file containing the _linear representation_.

    Args:
        filename (str): File to load.

    Returns:
        Tree: New tree.

    Raises:
        FileNotFoundError: If file does not exist. 

    """        
    # Open file and get full content
    file = open(filename, 'r')
    content = file.read()
    # Remove all whitespace characters for easier parsing
    content = content.replace('\n', '').replace('\r', '') \
                     .replace('\t', '').replace(' ', '')
    file.close()
    # Parse content and return tree
    return from_linear(content)

    

