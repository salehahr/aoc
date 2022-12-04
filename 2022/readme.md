# 2022 Lessons Learnt

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

## Day 4