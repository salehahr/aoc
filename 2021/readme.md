# 2022 Lessons Learnt

## Day 6
Modelling: model finite set of states instead of huge set of objects.

## Day 7
Sorting a list by frequency
```python
import collections
counts = collections.Counter(unsorted)
sorted = sorted(unsorted, key=counts.get, reverse=True)
```

Unique list with preserved order
```python
unique = list(dict.fromkeys(list_with_duplicate_elements))
```
