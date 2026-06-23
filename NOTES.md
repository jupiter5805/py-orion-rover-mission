# Orion 7 Rover Mission Notes

## Task 6: Logic Layer Planning

The input layer is now responsible for turning raw mission strings into clean Python dictionaries and lists. The logic layer should not care where the data came from. It should only work with the structured mission data produced by the parser.

The logic layer needs to do four main things:

1. Rotate a rover left or right.
2. Move a rover forward by one square.
3. Execute a list of instructions for one rover.
4. Run a full mission and collect the final positions of all rovers.

### Position shape

For now, a rover position will continue to be represented as a dictionary:

```python
{"x": 1, "y": 2, "direction": "N"}
```

This keeps the logic simple at this stage. Later in the project this may be refactored into a class.

### Rotation design

Rotation will be a pure function. It will take a position and an instruction, then return a new position dictionary.

Example:

```python
rotate({"x": 0, "y": 0, "direction": "N"}, "L")
```

returns:

```python
{"x": 0, "y": 0, "direction": "W"}
```

The original position should not be changed.

Instead of using lots of `if` statements, I will use a direction cycle:

```python
["N", "E", "S", "W"]
```

Rotating right moves one step forward in the list. Rotating left moves one step backward.

### Movement design

Movement will also be a pure function. It will take a position and plateau bounds, then return a new position.

Direction changes:

```python
N = y + 1
E = x + 1
S = y - 1
W = x - 1
```

The plateau bounds are inclusive, so if the plateau is:

```python
{"max_x": 5, "max_y": 5}
```

then `(5, 5)` is still a valid position.

A move is valid only if:

```python
0 <= x <= max_x
0 <= y <= max_y
```

If a move would go off the plateau, the rover should stay in the same position.

### Instruction execution

The `execute_instructions` function will take:

```python
starting_position
instructions
plateau
```

It will go through each instruction one by one.

* If the instruction is `"L"` or `"R"`, it will call `rotate`.
* If the instruction is `"M"`, it will call `move`.

It should return the final position.

### Mission execution

A separate function will run the full mission. It will take the parsed mission dictionary and run each rover sequentially.

Each rover starts from its parsed starting position and follows its own instructions.

The output should be a list of final positions, for example:

```python
[
    {"x": 1, "y": 3, "direction": "N"},
    {"x": 5, "y": 1, "direction": "E"}
]
```

### Layer separation

The input layer should not import the logic layer.

The logic layer should not import the input layer.

The only place where parsing and mission running should meet is `main.py` or an integration test.

This keeps the project easier to test and easier to change later.
