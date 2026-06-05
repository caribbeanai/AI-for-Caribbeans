"""
First model. Predict if a Saturday at Hellshire Beach in Jamaica will be busy.
Inputs: temperature in Celsius, whether it is a holiday weekend.
Output: busy or not busy.

Author: Adrian Dunkley
"""

from sklearn.tree import DecisionTreeClassifier

X = [
    [28, 0],
    [30, 0],
    [32, 1],
    [29, 1],
    [25, 0],
    [27, 0],
    [33, 1],
    [31, 1],
    [26, 0],
    [30, 1],
]
y = [0, 1, 1, 1, 0, 0, 1, 1, 0, 1]

model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X, y)

print("Holiday weekend at 31C, busy?", bool(model.predict([[31, 1]])[0]))
print("Regular Saturday at 26C, busy?", bool(model.predict([[26, 0]])[0]))
