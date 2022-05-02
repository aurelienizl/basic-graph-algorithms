# -*- coding: utf-8 -*-
"""General Tree module: first child - right sibling representation.

*Warning:* All the functions defined in this module are assumed to receive a non-None
value for their ``ref/B`` parameter.

"""

from . import queue
from .queue import Queue

class TreeAsBin:
    """
    Simple class for (General) Trees 
    represented as Binary Trees (first child - right sibling)
    """

    def __init__(self, key, child=None, sibling=None):
        """
        Init Tree
        """
        self.key = key
        self.child = child
        self.sibling = sibling


###############################################################################
# Display

def dot(B):
    """Simple dot format of tree.

    Args:
        B (TreeAsBin).

    Returns:
        str: String storing dot format of tree.

    """

    s = "graph {\n"
    q = Queue()
    q.enqueue(B)
    s += str(id(B)) + '[label = "' + str(B.key) + '"]\n'
    while not q.isempty():
        B = q.dequeue()
        child = B.child
        while child:
            s += str(id(child)) + '[label = "' + str(child.key) + '"]\n'
            s = s + "   " + str(id(B)) + " -- " + str(id(child)) + "\n"
            q.enqueue(child)
            child = child.sibling
    s += "}"
    return s

def display(B):
    """Render a Tree for in-browser display.

    *Warning:* Made for use within IPython/Jupyter only.

    Args:
        T (Tree).

    Returns:
        Source: Graphviz wrapper object for tree rendering.

    """    
    try:
        from IPython.display import display
        from graphviz import Source
    except:
        raise Exception("Missing module: graphviz and/or IPython.")
    display(Source(dot(B)))
    

###############################################################################
# load and save
# use the "list" representation: (o A1 A2 ... AN).

def to_linear(B):
    """Build the _linear representation_ of a tree.

    Args:
        B (TreeAsBin)

    Returns:
        str: the linear representation of B

    """            
    s = '(' + str(B.key)
    C = B.child
    while C != None:
        s += to_linear(C)
        C = C.sibling
    s += ')'
    return s

def save(B, filename):
    """save the linear representation of a tree in a text file.

    Args:
        B (TreeAsBin): the tree to save.
        filename (str): the new file

    """        
    fout = open(filename, mode='w')
    fout.write(to_linear(B))
    fout.close()
    
    
def __from_linear(s, i=0): 
    if i < len(s) and s[i] == '(':   
        i = i + 1 # to pass the '('
        key = ""
        while not (s[i] in "()"):
            key = key + s[i]
            i += 1
        B = treeasbin.TreeAsBin(int(key))
        (B.child, i) = __from_linear(s, i)
        i = i + 1   # to pass the ')'
        (B.sibling, i) = __from_linear(s, i)
        return (B, i)
    else:
        return (None, i)

def from_linear(s):
    """Build a new tree from its _linear representation_.

    Args:
        str: the linear representation

    Returns:
        TreeAsBin: New tree.
    """            
    return __from_linear(s)[0]


def load(filename):
    """Build a new tree from a text file containing the _linear representation_.

    Args:
        filename (str): File to load.

    Returns:
        TreeAsBin: New tree.

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


