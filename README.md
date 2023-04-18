
# Basic Graph Algorithms

  
  

Basic Graph Algorithms is a graph manipulation project. This project brings together a set of methods and structure allowing graph creation and manipulation. This project is an example of homework requested in the EPITA engineering school in the 3rd semester.

  

## Installation

  

For APT package manager :


```bash

sudo apt  install  python3  -y && pip install  graphviz  IPython

```

## Usage

  

Clone the project

  

```bash

git clone  https://github.com/Darkvgold/Basic-Graph-Algorithms

```

  

Go to the project directory

  

```bash

cd Basic-Graph-Algorithms

```

  

Install dependencies

  

```bash

sudo apt  install  python3  -y && pip install  graphviz  IPython

```

  

Run the example file

  

```bash

python3 main.py

```

  
  

## Documentation

  
## Functions

### `__buildgraph(str1, str2, k)`

A helper function that computes the number of differing characters between two strings, `str1` and `str2`, up to a given length `k`. The function returns the difference between the two strings.

#### Parameters

-   `str1`: The first string to compare.
-   `str2`: The second string to compare.
-   `k`: The length to compare the strings up to.

#### Returns

-   `diff`: The number of differing characters between the two strings.

### `buildgraph(filename, k)`

This function reads a lexicon from a given file, builds an undirected graph connecting words of length `k` that differ by exactly one character, and returns the graph.

#### Parameters

-   `filename`: The name of the file containing the lexicon.
-   `k`: The desired word length for constructing the graph.

#### Returns

-   `G`: The constructed graph with words of length `k` and edges between words differing by exactly one character.


### `mostconnected(G)`

This function returns a list of words that are directly connected to the largest number of other words in the input graph `G`.

#### Parameters

-   `G`: The input graph.

#### Returns

-   `res`: A list of words that are directly connected to the largest number of other words in the input graph.

### `__alldoublets(G, x, M, L)`

A helper function that recursively finds all words that can form a doublet with the word at index `x` in the graph `G`. The function updates the list `L` with the doublet words.

#### Parameters

-   `G`: The input graph.
-   `x`: The index of the starting word in the graph.
-   `M`: A list of booleans indicating whether a word has been visited.
-   `L`: A list to store the doublet words.

### `alldoublets(G, start)`

This function returns a list of all words that can form a _doublet_ with the word `start` in the lexicon in the graph `G`.

#### Parameters

-   `G`: The input graph.
-   `start`: The starting word for finding doublets.

#### Returns

-   `L`: A list of words that can form a doublet with the starting word.

### `__nosolution(G, x, P)`

A helper function that recursively explores the graph `G`, updating the list `P` with boolean values indicating whether a node has been visited.

#### Parameters

-   `G`: The input graph.
-   `x`: The index of the starting word in the graph.
-   `P`: A list of booleans indicating whether a word has been visited.

### `nosolution(G)`

This function returns a pair of words that form a "doublet" without a solution in the input graph `G`, or `(None, None)` if there is no such pair.

#### Parameters

-   `G`: The input graph.

#### Returns

-   A tuple containing a pair of words that form a "doublet" without a solution in the input graph, or `(None, None)` if there is no such pair.

### `__ladder_v1(G, start, end, p)`

A helper function that finds a ladder of words that connect the doublet (start, end) in the input graph `G` using a breadth-first search algorithm.

#### Parameters

-   `G`: The input graph.
-   `start`: The starting word for the ladder.
-   `end`: The ending word for the ladder.
-   `p`: A list to store the parents of visited nodes during the search.

### `ladder_v1(G, start, end)`

This function returns a "ladder" of words that connect the "doublet" (start, end) in the input graph `G`, where a "ladder" is a sequence of words where each adjacent pair differs by only one character.

#### Parameters

-   `G`: The input graph.
-   `start`: The starting word for the ladder.
-   `end`: The ending word for the ladder.

#### Returns

-   `L`: A list of words forming a ladder between the start and end words in the input graph.

### `ladder_v2(G, start, end)`

This function returns a "ladder" of words that connect the "doublet" (start, end) in the input graph `G`, where a "ladder" is a sequence of words where each adjacent pair differs by only one character. This function uses a breadth-first search algorithm to find the shortest path between the two input words.

#### Parameters

-   `G`: The input graph.
-   `start`: The starting word for the ladder.
-   `end`: The ending word for the ladder.

#### Returns

-   `L`: A list of words forming a ladder between the start and end words in the input graph.

### `__longestdoublet_v1(G, s, p, start, end, max)`

A helper function that finds the longest ladder in the input graph `G` starting at node `s`.

#### Parameters

-   `G`: The input graph.
-   `s`: The starting node for the ladder.
-   `p`: A list to store the lengths of ladders.
-   `start`: The starting word of the longest ladder.
-   `end`: The ending word of the longest ladder.
-   `max`: The length of the longest ladder found so far.

#### Returns

-   A tuple containing the starting and ending words of the longest ladder found from the current node.

### `longestdoublet_v1(G)`

This function finds one of the most difficult doublets (that has the longest ladder) in the input graph `G`.

#### Parameters

-   `G`: The input graph.

#### Returns

-   A tuple containing the starting and ending words of the longest ladder and the ladder's length.

### `__longestdoublet_v2(G, val)`

A helper function that finds the longest ladder in the input graph `G` starting at the word `val`.

#### Parameters

-   `G`: The input graph.
-   `val`: The starting word for the ladder.

#### Returns

-   A tuple containing the starting word, the length of the longest ladder, and the ending word of the longest ladder found from the current word.

### `longestdoublet_v2(G)`

This function finds one of the most difficult doublets (that has the longest ladder) in the input graph `G`.

#### Parameters

-   `G`: The input graph.

#### Returns

-   A tuple containing the starting and ending words
  
  ### `components(G)`

This function returns the number of connected components in the input graph `G` and the component vector, which indicates the component each vertex belongs to.

#### Parameters

-   `G`: The input graph.

#### Returns

-   A pair containing the number of connected components and the component vector.

### `more_than_dist(G, src, dist)`

This function returns all nodes in the input graph `G` that are further than a specified distance `dist` from the source node `src`.

#### Parameters

-   `G`: The input graph.
-   `src`: The source node.
-   `dist`: The distance threshold.

#### Returns

-   `L`: A list of nodes that are further than the specified distance from the source node.

### `just_than_dist(G, src, dist)`

This function returns all nodes in the input graph `G` that are exactly at a specified distance `dist` from the source node `src`.

#### Parameters

-   `G`: The input graph.
-   `src`: The source node.
-   `dist`: The desired distance.

#### Returns

-   `L`: A list of nodes that are exactly at the specified distance from the source node.

### `interval(G, src, min, max)`

This function returns all nodes in the input graph `G` that are at a distance between `min` and `max` (inclusive) from the source node `src`.

#### Parameters

-   `G`: The input graph.
-   `src`: The source node.
-   `min`: The minimum distance.
-   `max`: The maximum distance.

#### Returns

-   `L`: A list of nodes that are at a distance between `min` and `max` from the source node.

### `levels(G, src)`

This function returns the levels of the input graph `G` starting from the source node `src`. Each level contains nodes at the same distance from the source node.

#### Parameters

-   `G`: The input graph.
-   `src`: The source node.

#### Returns

-   `L`: A list of lists, where each inner list represents a level of nodes at the same distance from the source node.

## Authors

  

— Izoulet Aurélien, [@Darkvgold](https://github.com/Darkvgold)

— Nathalie Bouquet, [@nathalieEpita](https://github.com/nathalieEpita)

  
  

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

  
  

[![CodeFactor](https://www.codefactor.io/repository/github/aurelienizl/basic-graph-algorithms/badge)](https://www.codefactor.io/repository/github/aurelienizl/basic-graph-algorithms)
