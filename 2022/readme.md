# Notes

## Day 1
Typing
```python
from typing import Callable, Generator

Callable[[args], ReturnType]
Generator[YieldType, SendType, ReturnType]
```

## Day 3
Dict concatenation
```python
dict3 = dict1 | dict2
```

Unicode <-> integer conversion
```python
ord("a") == 97
ord("b") == 98
...
chr(97) == "a"
chr(98) == "b"
```

Function generator
```python
def outer_func(a):
    def inner_func(b):
        result_ = ...
        return result_
    return inner_func

A, B = ...
callback = outer_func(A)
result = callback(B)
```

## Day 6
[Sets](https://docs.python.org/3/tutorial/datastructures.html#sets) = unique lists.


## Day 11
1. Evals in lambda.  
    The following (doesn't work properly)
    ```python
    match = "x + 1"
    operation = lambda x: eval(match)
    ```
    is not the same as
    ```python
    match = "x + 1"
    operation = lambda x, match=match: eval(match)
    ```
2. [Modular arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic)  
    * Congruence
        ```
        x % N == x (mod N)
        ```
    
    * Corollary
        ```
        x % N == (x % N) % N
        ```
   * [Chinese Remainder Theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem) -
      Given that `N` and `M` are coprime:  
      ```
      x % N == (x % (N * M)) % N
      x % M == (x % (N * M)) % M
      ```
   * Example  
       ```
       # Divisibility test with big number
       91238 % 5 = 3
       91238 % 7 = 0
       
       # Reduce the big number
       91238 % (5 * 7) = 28
       
       # Divisibility test with the smaller number
       28 % 5 = 3
       28 % 7 = 0
       ```
 

## Day 12
[Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode) to find the shortest path between nodes in a graph.

## Day 13
Exclusive OR (XOR)
```python
True ^ False == True
True ^ True == False
False ^ False == False
```

List sorting with double arguments
```python
from functools import cmp_to_key

def compare(elem1, elem2):
    """
    Returns a number: (negative/zero/positive)
    which corresponds to (less than/equals/greater than)
    """
    if elem1 < elem2:
        return -1
    elif elem1 == elem2:
        return 0
    elif elem1 > elem2:
        return 1

unsorted_list.sort(key=cmp_to_key(compare))
```

## Day 14
[Memoisation](https://en.wikipedia.org/wiki/Memoization) can really speed things up...

## Day 24
[BFS (breadth-first search)](https://en.wikipedia.org/wiki/Breadth-first_search) uses a FIFO queue,
whereas a depth-first search uses LIFO. 
