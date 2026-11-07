# Worked synthetic example

All people, figures and events below are invented teaching inputs. This is an authored expected response, not a live model trial.

Synthetic task: A pure function returns net delivery contribution from revenue and variable cost. It must reject negative or non-numeric values. Inputs are plain int or float, excluding bool. Currency units are consistent.

Proposed implementation:
```python
from math import isfinite

def contribution(revenue, cost):
    for value in (revenue, cost):
        if type(value) not in (int, float) or not isfinite(value) or value < 0:
            raise ValueError('Use finite, non-negative numbers')
    return revenue - cost
```

Acceptance cases: contribution(20, 8) → 12; contribution(8, 20) → -12 (a loss is valid); contribution(0, 0) → 0. Reject -1, True, '20', infinity and NaN as inputs. Float arithmetic may round; currency-ledger software should use a defined decimal/minor-unit policy instead.

Reversal: restore the single changed function and its added tests to the recorded baseline. This example is not an application deployment and does not establish tax or accounting compliance.
