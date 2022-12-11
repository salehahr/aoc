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