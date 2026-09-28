# Orion 7 Rover Mission Notes

## Project Overview

This project builds a complete Mars rover mission-control system for Orion 7.

The project begins with raw mission input and gradually develops into a layered Python application that can:

- Parse mission input
- Rotate and move rovers
- Execute complete rover missions
- Validate invalid input
- Handle errors with custom exceptions
- Use structured logging
- Model the domain with classes
- Support multiple rover types
- Save mission outcomes as JSON
- Run interactively through a command-line interface

The project uses Test Driven Development throughout.

The general development process is:

1. Write a failing test.
2. Write the minimum implementation needed to pass.
3. Run the test suite.
4. Refactor if needed.
5. Commit the completed change.


# Task 1: Project Setup

The project was created with the following basic structure:

```text
py-orion-rover-mission/
├── src/
│   └── input_layer.py
├── tests/
│   └── test_input_layer.py
├── NOTES.md
├── README.md
├── requirements.txt
└── .gitignore
```

A Python virtual environment was created and activated.

`pytest` was installed for testing.

Dependencies were frozen into:

```text
requirements.txt
```

A Git repository was initialised and connected to GitHub.

The virtual environment, cache files, and other generated files were excluded using `.gitignore`.

The project uses small meaningful commits rather than one large final commit.


# Task 2: Parse Plateau

The first parser is:

```python
parse_plateau(text)
```

Its job is to convert a raw plateau-size string into structured data.

Example input:

```text
5 5
```

Output:

```python
{
    "max_x": 5,
    "max_y": 5
}
```

The values represent the upper-right coordinates of the plateau.

The lower-left corner is assumed to be:

```text
0 0
```

Tests were written using multiple plateau sizes to make sure the values were actually parsed rather than hardcoded.


# Task 3: Parse Rover Position

The second parser is:

```python
parse_position(text)
```

Example input:

```text
1 2 N
```

Output:

```python
{
    "x": 1,
    "y": 2,
    "direction": "N"
}
```

The parser separates the position into:

- x coordinate
- y coordinate
- compass direction

All four compass directions were tested:

```text
N
E
S
W
```

Multiple coordinate values were also tested to ensure the implementation was not hardcoded.


# Task 4: Parse Instructions

The instruction parser is:

```python
parse_instructions(text)
```

Example input:

```text
LMLMLMLMM
```

Output:

```python
[
    "L",
    "M",
    "L",
    "M",
    "L",
    "M",
    "L",
    "M",
    "M"
]
```

The function returns a list of individual instruction characters.

Tests cover:

- The returned value is a list
- A single instruction
- Multiple instructions
- Correct instruction order

Python strings are directly iterable, so there is no need for complicated parsing logic.


# Task 5: Mission Parser

The full mission parser is:

```python
parse_mission(text)
```

Its job is to coordinate the previous parsers.

It does not duplicate parsing logic.

The mission format is:

```text
plateau
rover position
rover instructions
rover position
rover instructions
...
```

Example:

```text
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

The parser produces:

```python
{
    "plateau": {
        "max_x": 5,
        "max_y": 5
    },
    "rovers": [
        {
            "position": {
                "x": 1,
                "y": 2,
                "direction": "N"
            },
            "instructions": [
                "L",
                "M",
                "L",
                "M",
                "L",
                "M",
                "L",
                "M",
                "M"
            ]
        },
        {
            "position": {
                "x": 3,
                "y": 3,
                "direction": "E"
            },
            "instructions": [
                "M",
                "M",
                "R",
                "M",
                "M",
                "R",
                "M",
                "R",
                "R",
                "M"
            ]
        }
    ]
}
```

The first line always represents the plateau.

After that, rover data comes in pairs:

```text
position line
instruction line
```

Tests cover:

- Plateau with no rovers
- One rover
- Two rovers
- The exact mission from the original brief

This task demonstrates composition because the larger parser is built from smaller focused parsing functions.


# Task 6: Logic Layer Planning

The input layer is responsible for turning raw mission strings into clean Python dictionaries and lists.

The logic layer should not care where the data came from.

It should only work with the structured mission data produced by the parser.

The logic layer needs to do four main things:

1. Rotate a rover left or right.
2. Move a rover forward.
3. Execute a list of instructions for one rover.
4. Run a complete mission and collect final rover positions.


## Position Representation

At this stage, a rover position remains a dictionary:

```python
{
    "x": 1,
    "y": 2,
    "direction": "N"
}
```

This keeps the first logic implementation simple.

Later the project refactors positions into classes.


## Rotation Design

Rotation should take:

```python
position
instruction
```

and return a new position.

Example:

```python
rotate(
    {"x": 0, "y": 0, "direction": "N"},
    "L"
)
```

returns:

```python
{
    "x": 0,
    "y": 0,
    "direction": "W"
}
```

The original dictionary should not be mutated.

Instead of a long `if/elif` chain, compass directions are treated as a cycle:

```python
[
    "N",
    "E",
    "S",
    "W"
]
```

Rotating right moves forward through the cycle.

Rotating left moves backwards through the cycle.


## Movement Design

Each direction corresponds to a coordinate change:

```text
N -> x stays same, y + 1
E -> x + 1, y stays same
S -> x stays same, y - 1
W -> x - 1, y stays same
```

The plateau boundaries are inclusive.

For:

```python
{
    "max_x": 5,
    "max_y": 5
}
```

the valid range is:

```python
0 <= x <= 5
0 <= y <= 5
```

If a rover attempts to move outside the plateau, it should stay where it is.


## Instruction Execution Design

The instruction execution function takes:

```python
starting_position
instructions
plateau
```

It processes each instruction in order.

For:

```text
L
R
```

it calls rotation logic.

For:

```text
M
```

it calls movement logic.

It should not duplicate compass or bounds logic.


## Mission Execution Design

A separate function runs the whole mission.

It takes the parsed mission dictionary and runs every rover sequentially.

The expected final positions from the original mission are:

```python
[
    {
        "x": 1,
        "y": 3,
        "direction": "N"
    },
    {
        "x": 5,
        "y": 1,
        "direction": "E"
    }
]
```


## Layer Separation

The input layer should not import the logic layer.

The logic layer should not import the input layer.

They only meet in:

```text
main.py
```

or integration tests.

This separation makes both layers easier to test and change independently.


# Task 7: Rotate

The rover rotation function was implemented using the compass cycle:

```python
[
    "N",
    "E",
    "S",
    "W"
]
```

Left rotation produces:

```text
N -> W
W -> S
S -> E
E -> N
```

Right rotation produces:

```text
N -> E
E -> S
S -> W
W -> N
```

The implementation returns a new position rather than modifying the original position dictionary.

Tests cover:

- Left rotation from all four directions
- Right rotation from all four directions
- Original position is unchanged
- Returned position is a new object

Using a direction cycle removes the need for repetitive branching logic.


# Task 8: Move

Movement uses a direction-to-coordinate lookup.

Conceptually:

```python
MOVEMENTS = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0)
}
```

A move applies the matching x and y changes.

The rover keeps the same compass direction while moving.


## Plateau Boundaries

The maximum plateau coordinates are valid positions.

For a:

```text
5 5
```

plateau:

```text
5 5
```

is valid.

But:

```text
5 6
```

or:

```text
6 5
```

are outside the plateau.

Moves outside the plateau are refused.

Tests cover all four edges:

- North
- East
- South
- West

Corners are also tested because they can expose off-by-one errors.


# Task 9: Execute Instruction Sequence

The function:

```python
execute_instructions(
    position,
    instructions,
    plateau
)
```

executes a complete rover instruction sequence.

It delegates to:

```python
rotate()
```

and:

```python
move()
```

rather than implementing rotation and movement rules itself.

An empty instruction list leaves the rover at its starting position.

A single instruction behaves correctly.

The original mission sequence:

```text
LMLMLMLMM
```

starting from:

```text
1 2 N
```

ends at:

```text
1 3 N
```

The original starting dictionary remains unchanged.


# Task 10: Main Program and Integration Testing

A mission-running function was added to process every rover sequentially.

The original input:

```text
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

produces:

```text
1 3 N
5 1 E
```


## Integration Test

An integration test runs the complete pipeline:

```text
raw mission string
        ↓
parse_mission()
        ↓
structured mission
        ↓
run_mission()
        ↓
final rover positions
```

The original mission is tested end-to-end.

A second custom mission is also tested so integration coverage does not rely on only one example.

The integration tests become the safety net for later refactoring.


# Task 11: Custom Exceptions

A custom exception hierarchy was created:

```text
MissionError
├── InvalidPlateauError
├── InvalidPositionError
├── InvalidInstructionError
└── InvalidMissionError
```

`MissionError` is the base class.


## Why Custom Exceptions

Custom exceptions allow calling code to distinguish expected mission failures from unrelated programming errors.

Examples include:

- Invalid plateau syntax
- Invalid rover position syntax
- Invalid direction
- Invalid rover instruction
- Invalid mission structure

The application can catch:

```python
MissionError
```

when it wants to handle all expected mission failures.

More specific callers can catch individual subclasses when necessary.


## Useful Error Messages

Error messages should explain the actual problem.

For example:

```text
Unknown instruction: 'Q' in 'LMQR'
```

is more useful than only:

```text
InvalidInstructionError
```


## Parser Validation

The parsers were updated to reject malformed input.

Examples include:

```text
5
```

instead of two plateau coordinates,

```text
1 2 Q
```

with an invalid compass direction,

and:

```text
LMQR
```

with an unknown rover instruction.


# Task 12: Try/Except in main.py

The program should not crash when users provide invalid mission input.

`main.py` catches:

```python
MissionError
```

specifically.

It does not use:

```python
except Exception:
```

because catching every possible Python error could hide programming bugs.

Expected mission errors are handled gracefully.

Unexpected errors remain visible to developers.

When mission parsing fails, the program displays a clear error message and stops that mission safely.


# Task 13: Logging

Python's built-in:

```python
logging
```

module was introduced for diagnostic information.

Logging is configured centrally in the application entry point.


## Logging Levels

The application uses:

```text
INFO
```

for normal mission events.

Examples:

```text
Mission starting
Mission completed
```

It uses:

```text
WARNING
```

for recoverable events.

For example:

```text
Move refused because rover would leave plateau
```

It uses:

```text
ERROR
```

for caught mission exceptions.


## Print vs Logging

`print()` is reserved for user-facing output in the interface layer.

Internal diagnostic information uses logging.

This separates application output from developer and operational information.


# Task 14: Refactor Logic into Classes

The original dictionary-based logic was refactored into domain classes.

The main classes are:

```python
Position
Plateau
Rover
```

The integration test remained unchanged during the refactor.

This ensures that although the internal design changed, the external mission behaviour stayed the same.


## Position Class

A `Position` contains:

```text
x
y
direction
```

Example:

```python
Position(
    1,
    2,
    "N"
)
```


## Plateau Class

A `Plateau` contains:

```text
max_x
max_y
```

It is responsible for understanding its own valid bounds.


## Rover Class

A `Rover` contains a:

```python
Position
```

and provides behaviour including:

```text
rotate
move
execute_instructions
```


## Mutation vs Replacement Decision

I chose to make the `Rover` object mutable.

This fits the domain because a rover represents a physical entity whose state changes while it moves.

For example:

```python
rover.move(plateau)
```

updates the rover's current position.


## Plateau Bounds Decision

The plateau owns the rules describing valid coordinates.

The rover calculates a potential destination.

The move is accepted only when that destination is within the plateau.

This separates:

```text
movement behaviour
```

from:

```text
plateau boundary knowledge
```


# Task 15: Validation at Construction

The model classes initially trusted their inputs.

Validation was added using:

```python
@property
```

setters.


## Position Validation

A position's:

```text
x
y
```

must be non-negative integers.

Valid examples include:

```text
0
1
5
```

Invalid examples include:

```text
-1
"5"
```

The direction must be:

```text
N
E
S
W
```

Invalid values raise:

```python
InvalidPositionError
```


## Plateau Validation

The plateau's:

```text
max_x
max_y
```

must be positive integers.

Values such as:

```text
5
10
```

are valid.

Values such as:

```text
0
-1
"5"
```

are invalid.

Invalid values raise:

```python
InvalidPlateauError
```


## Rover Position Validation

A rover's position must be a:

```python
Position
```

instance.

Passing a raw dictionary directly to the Rover is rejected.


## Why Validate During Construction

Invalid state should be prevented as early as possible.

If an invalid `Position` cannot be constructed, later parts of the application do not need to repeatedly check whether the position is valid.

Property setters also mean later assignments receive the same validation as initial construction.


# Task 16: Specialised Rover

A new specialised rover type was introduced:

```python
CargoRover
```

A normal rover moves one square for every:

```text
M
```

instruction.

A Cargo Rover moves two squares.


## Cargo Rover Bounds Behaviour

A Cargo Rover only performs the movement if the full two-square move is legal.

For example, if it is at:

```text
4 2 E
```

on a:

```text
5 5
```

plateau, moving two squares would end at:

```text
6 2
```

which is outside the plateau.

The move is therefore completely refused.

The Cargo Rover stays at:

```text
4 2 E
```


## Inheritance vs Composition

Two designs were considered.

### Inheritance

```text
Rover
  ↓
CargoRover
```

The Cargo Rover inherits normal rover behaviour and overrides only its movement distance.


### Composition

Another option would be to give one Rover class a movement strategy object.

Different strategies could move different distances.


## Decision

I chose inheritance.

The Cargo Rover shares nearly everything with the normal Rover:

- Position
- Rotation
- Plateau interaction
- Instruction processing
- Mission execution interface

The meaningful difference is only movement distance.

Inheritance therefore gives a clear and small specialisation.


## Abstract Base Class Decision

I did not make Rover abstract.

The normal Rover itself is a valid concrete rover.

There is therefore no need to force all rover objects to be subclasses of an abstract-only parent.


## Rover Type Input

A standard rover is still represented as:

```text
1 2 N
```

A Cargo Rover uses:

```text
1 2 N C
```

The additional:

```text
C
```

marks the rover as cargo.


## Polymorphism

The mission runner chooses the correct rover class during construction.

After construction, both rover types are used through the same interface:

```python
rover.execute_instructions(...)
```

The orchestrator does not need separate instruction-running logic for Cargo Rovers.


# Task 17: Dunder Methods

Dunder methods were added to make model objects easier to display, debug, and compare.


## __repr__

`Position`, `Plateau`, and `Rover` implement useful developer-facing representations.

Example:

```python
Position(
    x=1,
    y=3,
    direction="N"
)
```

has a representation equivalent to:

```text
Position(x=1, y=3, direction='N')
```

A Rover representation includes its current Position.

Cargo Rovers automatically use the Cargo Rover class name in their representation.


## __str__

`Position.__str__()` returns the human-readable mission format.

Example:

```text
1 3 N
```

This matches the required rover output from the original mission specification.


## __eq__

Two `Position` objects compare equal when:

```text
x matches
y matches
direction matches
```

Two Rovers compare equal when:

- They are the same rover type
- Their positions are equal

This means:

```text
Rover at 1 2 N
```

does not compare equal to:

```text
CargoRover at 1 2 N
```

because the rover types have different behaviour.


## __hash__ Decision

I chose not to implement:

```python
__hash__
```

The model objects are mutable.

A rover's position changes during a mission.

Using mutable objects as dictionary keys or set members could produce confusing behaviour if their state changed after being hashed.

Leaving these objects unhashable is safer.


# Task 18: Mission Archive

Mission outcomes are persisted to JSON files.

The archive contains:

- Original plateau specification
- Rover type
- Rover starting position
- Rover final position
- Timestamp


## Example Archive

```json
{
    "plateau": {
        "max_x": 5,
        "max_y": 5
    },
    "rovers": [
        {
            "type": "standard",
            "starting_position": {
                "x": 1,
                "y": 2,
                "direction": "N"
            },
            "final_position": {
                "x": 1,
                "y": 3,
                "direction": "N"
            }
        }
    ],
    "timestamp": "..."
}
```


## Archive Functions

The archive module provides:

```python
build_archive()
save_archive()
load_archive()
```

`build_archive()` creates the archive data structure.

`save_archive()` writes the archive as JSON.

`load_archive()` reads the JSON file back into Python data.


## Round-Trip Testing

Archive behaviour is tested using a round trip:

```text
Python data
    ↓
save JSON
    ↓
load JSON
    ↓
Python data
```

The loaded value should equal the original archive structure.

This confirms that archive persistence is lossless.


## Archive Directory

Generated mission archive files are runtime data rather than source code.

The:

```text
archives/
```

folder is excluded from Git using `.gitignore`.


# Task 19: Interactive CLI

The final interface is an interactive command-line application.

Running:

```bash
python main.py
```

starts Orion 7 Mission Control.


## CLI Flow

The application asks the user for:

1. Plateau size.
2. Rover starting position.
3. Rover instructions.
4. Whether another rover should be added.

After all rovers have been entered, the mission runs.

The program then:

1. Displays final rover positions.
2. Saves the mission archive.
3. Prints the location of the archive file.


## Example Session

```text
=== ORION 7 MISSION CONTROL ===

Enter plateau size (e.g. 5 5): 5 5

Rover 1
Enter rover position: 1 2 N
Enter rover instructions: LMLMLMLMM
Add another rover? y

Rover 2
Enter rover position: 3 3 E
Enter rover instructions: MMRMMRMRRM
Add another rover? n

Mission complete.
Rover 1: 1 3 N
Rover 2: 5 1 E

Archive written to: archives/mission_....json
```


## Invalid Input

Invalid input should never crash the CLI.

Instead, the application displays a useful error and prompts the user again.

This applies to:

- Invalid plateau sizes
- Invalid rover positions
- Invalid compass directions
- Invalid rover types
- Invalid rover instructions
- Invalid yes/no responses


## Interface Separation

The CLI coordinates other parts of the system.

It does not implement rover movement rules.

The interface calls:

```text
input parsers
model classes
mission runner
archive functions
```

This keeps presentation logic separate from domain logic.


# Testing Strategy

The project uses:

```text
pytest
```

throughout.


## Unit Tests

Unit tests cover:

- Plateau parsing
- Position parsing
- Instruction parsing
- Mission parsing
- Rotation
- Movement
- Plateau boundaries
- Instruction execution
- Custom exceptions
- Logging behaviour
- Position model
- Plateau model
- Rover model
- Constructor validation
- Cargo Rover
- Dunder methods
- Archive persistence
- CLI input handling


## Integration Tests

Integration tests verify multiple layers working together.

The main regression test is the original Orion 7 mission:

```text
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

Expected result:

```text
1 3 N
5 1 E
```

This test was kept green while the project was refactored from dictionaries and pure functions into classes.


# TDD Workflow

The project followed Test Driven Development.

The normal cycle was:

```text
RED
Write a failing test

GREEN
Write enough implementation to pass

REFACTOR
Improve the implementation while keeping tests green

COMMIT
Save the completed development step
```

This made later refactoring safer because existing tests protected previously working behaviour.


# Git Commit Strategy

The project was developed using small meaningful commits.

Examples include:

```text
feat: add left rover rotation
feat: add right rover rotation and immutability
feat: add rover movement in all directions
feat: prevent rover movement beyond plateau bounds
feat: execute basic rover instructions
feat: execute complete rover instruction sequences
feat: add full mission runner
test: add end-to-end mission integration tests
feat: add mission exception hierarchy
feat: validate malformed mission input
feat: handle mission errors gracefully in main
feat: add structured mission logging
refactor: introduce Position model
refactor: introduce Plateau model
refactor: introduce Rover model and class orchestrator
feat: validate model construction
feat: add Cargo Rover and mixed fleet support
feat: add rover model dunder methods
feat: add JSON mission archive
feat: add interactive mission control CLI
```

This produces a readable project history where each commit represents an actual development step.


# Final Project Structure

The finished project structure is approximately:

```text
py-orion-rover-mission/
│
├── src/
│   ├── input_layer.py
│   ├── logic.py
│   ├── models.py
│   ├── exceptions.py
│   └── archive.py
│
├── tests/
│   ├── test_input_layer.py
│   ├── test_logic.py
│   ├── test_models.py
│   ├── test_exceptions.py
│   ├── test_integration.py
│   ├── test_main.py
│   ├── test_archive.py
│   └── test_cli.py
│
├── main.py
├── README.md
├── NOTES.md
├── requirements.txt
├── .gitignore
└── archives/
```


# Module Responsibilities

## src/input_layer.py

Responsible for converting raw mission input into structured Python data.

Contains functions such as:

```python
parse_plateau()
parse_position()
parse_instructions()
parse_mission()
```


## src/logic.py

Responsible for mission execution and orchestration.

Earlier functional rover logic was also developed here before the object-oriented refactor.


## src/models.py

Contains the main domain classes:

```python
Position
Plateau
Rover
CargoRover
```

This module contains most rover behaviour and model validation.


## src/exceptions.py

Contains the custom mission exception hierarchy:

```python
MissionError
InvalidPlateauError
InvalidPositionError
InvalidInstructionError
InvalidMissionError
```


## src/archive.py

Responsible for JSON mission persistence.

Contains:

```python
build_archive()
save_archive()
load_archive()
```


## main.py

Acts as the interface and application entry point.

It is responsible for:

- Configuring logging
- Prompting users
- Parsing user input
- Running missions
- Displaying final positions
- Handling expected errors
- Saving archives

It does not implement rover navigation logic itself.


# Original Mars Rover Mission

Original input:

```text
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

Expected and produced output:

```text
1 3 N
5 1 E
```


# Final Capabilities

The completed system can:

- Parse plateau input
- Parse rover positions
- Parse rover instructions
- Parse complete missions
- Validate malformed input
- Rotate rovers left
- Rotate rovers right
- Move rovers forward
- Respect plateau boundaries
- Execute full instruction sequences
- Execute multiple rovers sequentially
- Run complete missions
- Raise custom exceptions
- Handle expected errors gracefully
- Produce structured logs
- Model positions using classes
- Model plateaus using classes
- Model rovers using classes
- Validate model construction
- Support a standard rover
- Support a Cargo Rover
- Execute mixed rover fleets
- Provide useful object representations
- Compare model objects
- Save mission outcomes as JSON
- Reload mission archives
- Run interactively through a CLI
- Re-prompt after invalid user input
- Maintain unit and integration tests


# Optional Extensions

The core project is complete without the optional extensions.

Possible future extensions include:

- State-machine CLI
- Async coordination
- ASCII plateau visualisation
- Additional rover types
- Plateau obstacles
- Mission replay

These are optional and should only be added if the core project remains complete and well tested.


# Final Reflection

The project began as a simple Mars Rover parsing and navigation exercise but developed into a layered Python application.

The most important lessons from the project were:

- Separate raw input parsing from domain logic.
- Build complex behaviour from smaller focused functions.
- Use TDD to protect existing behaviour.
- Keep integration tests during major refactors.
- Prevent invalid state as early as possible.
- Use custom exceptions for domain failures.
- Keep diagnostic logging separate from user output.
- Put behaviour on the objects that own the relevant state.
- Use polymorphism so orchestration code does not depend heavily on rover type.
- Keep persistence logic separate from mission logic.
- Keep interface code separate from domain rules.
- Use small Git commits so the development story is easy to follow.

The result is a complete Orion 7 rover mission-control application rather than only a solution to the original Mars Rover kata.