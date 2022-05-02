# `algopy` directory

Will contain all "modules" (.py) needed for algo classes

## Utilisation

To import the module `xxx.py`

    from algopy import xxx


- either the file containing the import is in the same directory as `algopy`
- either `algopy` has been added to the "Python path" (recommended)

## Graphviz to display trees (and later graphs)
To use the `display` functions in `tree.py` and `treeasbin.py` (to test your `dot` function):

- under IPython, if you managed to install [Graphviz](https://pypi.org/project/graphviz/)
    
    - try `tree.display(T)` 
- console mode:
    - you just need graphviz (not the Python module)
    - save the result of your `dot` function in a file (`tree.dot`in the example below)
    - run `dot`:
        - for instance under Ubuntu
            ```bash
            dot tree.dot -Tpng > tree.png
            ```
            creates `tree.png`: ![`tree.png`](tree.png) 
- Online: copy the result of `print(tree.dot(T))` here: [https://dreampuf.github.io/GraphvizOnline](https://dreampuf.github.io/GraphvizOnline)