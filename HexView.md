
# All bellow is written by AI

##  ```str.format``` 

The standard `str.format()` method uses replacement fields enclosed in curly braces `{}` to interpolate variables and control text alignment, numeric padding, and precision.

### Basic Field Syntax

Inside curly braces `{}`:


$$\text{\{ [field\_name] : [fill][align][width][.precision][type] \}}$$

---

### Alignment & Padding Specifiers

| Specifier | Purpose | Code Example | Output |
| --- | --- | --- | --- |
| **`:<`** | Left-align | `"{:<10}".format("Cat")` | `'Cat       '` |
| **`:>`** | Right-align | `"{:>10}".format("Cat")` | `'       Cat'` |
| **`:^`** | Center-align | `"{:^10}".format("Cat")` | `'   Cat    '` |
| **`fill`** | Custom fill char | `"{:*^10}".format("Cat")` | `'***Cat****'` |

---

### Data Type Specifiers (`type`)

| Specifier | Description | Code Example | Output |
| --- | --- | --- | --- |
| **`s`** | String | `"{:s}".format("Text")` | `'Text'` |
| **`d`** | Decimal Integer | `"{:d}".format(42)` | `'42'` |
| **`f`** | Fixed-point Float | `"{:.2f}".format(3.14159)` | `'3.14'` |
| **`%`** | Percentage | `"{:.1%}".format(0.75)` | `'75.0%'` |
| **`b` / `x**` | Binary / Hexadecimal | `"{:b}".format(10)` | `'1010'` |
| **`,`** | Thousands Separator | `"{:,}".format(1000000)` | `'1,000,000'` |

---

### Referencing Arguments

**1. Positional Alignment (Implicit vs. Explicit Index)**

```python
# Implicit order
print("{:<10} {:>5}".format("Item", 4))
# Output: 'Item           4'

# Explicit indexing (reuse or reorder)
print("{1} before {0}".format("B", "A"))
# Output: 'A before B'

```

**2. Named Keyword Arguments**

```python
print("{item:<12} {qty:>5} {price:>10.2f}".format(
    item="Laptop", 
    qty=2, 
    price=999.99
))
# Output: 'Laptop               2     999.99'

```

**3. Unpacking Dictionaries or Sequences**

```python
data = {"name": "Alice", "score": 95.5}
print("Player: {name} | Score: {score:.1f}".format(**data))

point = (10, 20)
print("X: {0[0]}, Y: {0[1]}".format(point))

```


## Flag Capture in Python

The recommended way to handle command-line flags in Python is using **`argparse`**, which is built into the standard library.

### Common Flag Types & Syntax

Here is a standard setup handling on/off switches, string flags, and integer values:

```python
import argparse

# 1. Initialize the parser
parser = argparse.ArgumentParser(description="Process command line flags.")

# 2. Add flags (prefix with - or --)

# Boolean Flag (On/Off Switch)
# If passed, sets to True; if omitted, defaults to False
parser.add_argument(
    "-v", "--verbose", action="store_true", help="Enable verbose mode"
)

# Flag taking a String argument (with a default value)
parser.add_argument(
    "-o", "--output", type=str, default="out.txt", help="Output file path"
)

# Flag taking an Integer argument
parser.add_argument(
    "-c", "--count", type=int, default=1, help="Number of repetitions"
)

# 3. Parse arguments from CLI
args = parser.parse_args()

# 4. Access flag values
print(f"Verbose: {args.verbose}")
print(f"Output:  {args.output}")
print(f"Count:   {args.count}")

```

---

### Executing from Command Line

Running this script from your terminal:

```bash
# Using short or long flags
python script.py -v --output report.csv --count 5

```

**Output:**

```text
Verbose: True
Output:  report.csv
Count:   5

```

---

### Key Flag Configuration Options

| Parameter | Purpose | Example |
| --- | --- | --- |
| **`action="store_true"`** | Creates a boolean switch defaulting to `False`. | `parser.add_argument("-v", action="store_true")` |
| **`type=`** | Automatically converts string input to `int`, `float`, etc. | `parser.add_argument("-c", type=int)` |
| **`default=`** | Value assigned if flag is omitted by the user. | `parser.add_argument("-o", default="out.txt")` |
| **`required=True`** | Forces user to provide an optional flag. | `parser.add_argument("-k", "--key", required=True)` |
| **`choices=[]`** | Restricts flag input to a specific list of values. | `parser.add_argument("--mode", choices=["fast", "slow"])` |

`argparse` also automatically generates a complete usage menu if users run `python script.py --help`.

If you want to quickly see how to create and manage CLI parsers step-by-step, check out [Lesson 60 on Python's Built-In CLI Parser](https://www.youtube.com/watch?v=VhIeKEzsWFY&vl=ml). This video breaks down `add_argument()` options like boolean flags, value types, and default settings in a clear visual format.