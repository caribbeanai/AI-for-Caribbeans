# Python in one weekend

Saturday morning, install Python from python.org or use Google Colab. By Sunday night you will know enough to read every script in this repo.

## Saturday

### 1. Variables

```python
name = "Shanice"
age = 16
island = "Saint Lucia"
print(f"{name} is {age} and lives in {island}.")
```

### 2. Lists

```python
islands = ["Jamaica", "Trinidad", "Barbados", "Saint Lucia"]
for island in islands:
    print(island)
```

### 3. If statements

```python
score = 78
if score >= 75:
    print("Grade I")
elif score >= 60:
    print("Grade II")
else:
    print("Try again")
```

### 4. Functions

```python
def jmd_to_usd(amount_jmd, rate=156):
    return round(amount_jmd / rate, 2)

print(jmd_to_usd(20000))
```

## Sunday

### 5. Dictionaries

```python
populations = {"Jamaica": 2_800_000, "Barbados": 281_000, "Grenada": 113_000}
print(populations["Barbados"])
```

### 6. Reading a file

```python
with open("notes.txt") as f:
    for line in f:
        print(line.strip())
```

### 7. Using a library

```python
import random
fruits = ["mango", "ackee", "soursop", "guinep", "june plum"]
print(random.choice(fruits))
```

That is enough. Now open `first_model.py` and run it.
