# 🛰️ Orion 7 Mars Rover Mission Control

A layered, fully tested Python mission-control application for planning and executing robotic rover missions on a rectangular Mars plateau.

The project began as a classic rover-navigation exercise and was developed into a more complete software system featuring input parsing, object-oriented domain modelling, validation, custom exceptions, structured logging, multiple rover types, JSON mission archiving, integration testing, and an interactive command-line interface.

---

## 🚀 Project Overview

Orion 7 is preparing its first uncrewed Mars rover mission.

Mission Control needs software capable of:

- Reading raw mission instructions
- Creating and controlling multiple rovers
- Rotating and moving rovers across a plateau
- Preventing movement outside mission boundaries
- Running rovers sequentially
- Handling invalid input safely
- Supporting different rover types
- Recording completed missions
- Providing an interactive terminal interface

The finished system is designed as a layered Python application rather than a single script.

---

## ✅ Features

- Parse raw Mars mission input
- Parse plateau coordinates
- Parse rover positions and headings
- Parse `L`, `R`, and `M` navigation instructions
- Rotate rovers left and right
- Move rovers in all four compass directions
- Enforce plateau boundaries
- Execute complete rover instruction sequences
- Run multiple rovers sequentially
- Support standard and Cargo Rovers
- Validate domain objects during construction
- Handle invalid input with custom exceptions
- Use structured Python logging
- Persist mission results as JSON archives
- Reload archived mission data
- Provide an interactive command-line interface
- Re-prompt users after invalid input
- Unit and integration test coverage with `pytest`
- Developed using Test Driven Development

---

## 🧭 Rover Navigation

A rover position contains:

```text
x-coordinate y-coordinate direction
```

Example:

```text
1 2 N
```

This means:

- `x = 1`
- `y = 2`
- Facing North

The four valid compass directions are:

```text
N
E
S
W
```

Rovers receive three possible instructions:

| Instruction | Meaning |
|---|---|
| `L` | Rotate 90° left |
| `R` | Rotate 90° right |
| `M` | Move forward |

Rotation changes the rover's heading without changing its coordinates.

Movement changes its coordinates while maintaining the same heading.

---

## 🗺️ Plateau Rules

The first mission line defines the upper-right plateau coordinates.

Example:

```text
5 5
```

The lower-left corner is always assumed to be:

```text
0 0
```

Therefore valid positions are:

```text
0 <= x <= 5
0 <= y <= 5
```

The upper-right coordinate itself is valid.

If a rover attempts to move beyond the plateau boundary, the move is refused and the rover remains in its current position.

---

## 🤖 Rover Types

### Standard Rover

A standard rover moves **one square** for every `M` instruction.

Example position:

```text
1 2 N
```

---

### Cargo Rover

The Cargo Rover is a specialised rover that moves **two squares** for every `M` instruction.

Cargo Rovers use an additional `C` marker:

```text
1 2 N C
```

If the full two-square movement would leave the plateau, the entire move is refused.

The Cargo Rover is implemented using inheritance from the standard `Rover` class.

Both rover types use the same mission execution interface, allowing the orchestrator to run a mixed fleet polymorphically.

---

## 🧪 Original Mission Example

### Input

```text
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

### Expected Output

```text
1 3 N
5 1 E
```

The application reproduces this result through the complete parsing and mission-execution pipeline.

---

## 🏗️ Architecture

The project separates responsibilities into different modules.

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

---

## 📥 Input Layer

Located in:

```text
src/input_layer.py
```

The input layer converts raw strings into structured Python data.

Main functions include:

```python
parse_plateau()
parse_position()
parse_instructions()
parse_mission()
```

For example:

```text
1 2 N
```

becomes:

```python
{
    "x": 1,
    "y": 2,
    "direction": "N"
}
```

The input layer is deliberately separated from rover logic so that changes to the input format do not require changes throughout the application.

---

## 🧠 Logic Layer

Located in:

```text
src/logic.py
```

The logic layer handles mission execution and orchestration.

The project initially implemented rover navigation using pure functions before later refactoring the domain into classes.

This allowed the navigation behaviour to be tested independently before introducing object-oriented modelling.

---

## 🧱 Domain Models

Located in:

```text
src/models.py
```

The main domain classes are:

```python
Position
Plateau
Rover
CargoRover
```

### Position

Represents:

```text
x
y
direction
```

### Plateau

Represents:

```text
max_x
max_y
```

and determines whether rover positions are within valid bounds.

### Rover

Owns a `Position` and provides behaviour including:

```text
rotate
move
execute_instructions
```

### CargoRover

Inherits standard Rover behaviour while overriding movement distance.

---

## 🔐 Validation

Domain objects validate their state using Python properties.

### Position Rules

- `x` must be a non-negative integer
- `y` must be a non-negative integer
- direction must be `N`, `E`, `S`, or `W`

### Plateau Rules

- `max_x` must be a positive integer
- `max_y` must be a positive integer

Invalid model construction raises project-specific exceptions.

This prevents invalid object state from spreading through the application.

---

## ⚠️ Custom Exceptions

Located in:

```text
src/exceptions.py
```

The project uses a custom exception hierarchy:

```text
MissionError
├── InvalidPlateauError
├── InvalidPositionError
├── InvalidInstructionError
└── InvalidMissionError
```

This makes expected mission failures distinguishable from unrelated programming errors.

For example, invalid input such as:

```text
1 2 Q
```

or:

```text
LMQR
```

produces a meaningful mission-specific error rather than an unclear generic exception.

---

## 📝 Logging

The application uses Python's built-in `logging` module.

Typical logging levels include:

- `INFO` — normal mission events
- `WARNING` — refused rover movements or recoverable problems
- `ERROR` — caught mission failures

User-facing output remains separate from diagnostic logging.

---

## 💾 Mission Archives

Located in:

```text
src/archive.py
```

Completed missions can be stored as JSON.

Each archive contains:

- Plateau specification
- Rover type
- Starting position
- Final position
- Timestamp

Example:

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

Archive functionality includes:

```python
build_archive()
save_archive()
load_archive()
```

Archive persistence is tested using a write/read round-trip to verify that stored data can be restored without loss.

Generated archives are ignored by Git.

---

## 💻 Interactive CLI

Run the application with:

```bash
python main.py
```

Example session:

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

The CLI validates input as it is entered.

If invalid data is supplied, the user receives a clear message and is prompted again rather than the program terminating unexpectedly.

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/jupiter5805/py-orion-rover-mission.git
```

Move into the project:

```bash
cd py-orion-rover-mission
```

---

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

With the virtual environment activated:

```bash
python main.py
```

Follow the prompts to:

1. Enter the plateau size
2. Add a rover
3. Enter navigation instructions
4. Add additional rovers if required
5. Execute the mission

The final rover positions will be displayed and the mission will be archived automatically.

---

## 🧪 Running the Tests

Run the full test suite:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_models.py -v
```

or:

```bash
pytest tests/test_integration.py -v
```

The project contains both unit and integration tests.

---

## 🔬 Testing Strategy

Unit tests cover:

- Plateau parsing
- Rover-position parsing
- Instruction parsing
- Full mission parsing
- Rover rotation
- Rover movement
- Plateau boundary handling
- Instruction execution
- Mission execution
- Custom exceptions
- Logging behaviour
- Position model
- Plateau model
- Rover model
- Cargo Rover
- Property validation
- Dunder methods
- JSON archive persistence
- CLI input handling

Integration tests verify that multiple layers work together correctly.

The original Mars Rover mission acts as the main end-to-end regression test.

---

## 🔴🟢 Test Driven Development

The project was developed using a TDD workflow:

```text
RED
Write a failing test

GREEN
Write the minimum code required to pass

REFACTOR
Improve the implementation while keeping tests green

COMMIT
Commit the completed change
```

This approach was especially valuable during the transition from functional dictionary-based logic to object-oriented models.

Existing tests acted as a safety net throughout the refactor.

---

## 🐍 Python Concepts Demonstrated

This project demonstrates practical use of:

- Python functions
- Dictionaries and lists
- Loops
- Pure functions
- Lookup tables
- Modular architecture
- Object-Oriented Programming
- Inheritance
- Polymorphism
- Properties and setters
- Custom exceptions
- Exception handling
- Logging
- JSON serialization
- File handling
- Dunder methods
- Fixtures
- TDD
- Unit testing
- Integration testing
- CLI development
- Git version control

---

## 🧰 Technologies

- Python
- pytest
- JSON
- Python Logging
- Object-Oriented Programming
- Test Driven Development
- Git
- GitHub

---

## 🌐 Design Decisions

Detailed engineering decisions are documented in:

```text
NOTES.md
```

This includes reasoning around:

- Logic-layer design
- Functional purity
- Plateau boundary ownership
- Mutation vs replacement
- Class modelling
- Constructor validation
- Exception hierarchy
- Logging
- Inheritance vs composition
- Cargo Rover design
- Dunder methods
- Hashability
- Archive persistence
- CLI separation

---

## 📈 Development Approach

The repository was developed through small, meaningful commits rather than a single large implementation.

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

This provides a readable development history and demonstrates incremental software development.

---

## 🎯 Key Learning Outcomes

This project demonstrates several software-engineering principles:

### Separation of concerns

Input parsing, domain behaviour, persistence, and the interface are separated into dedicated modules.

### Composition

Larger operations are built by coordinating smaller focused functions and objects.

### Validation close to the data

Model objects prevent invalid states from being created.

### Custom error handling

Expected domain failures are represented explicitly through custom exceptions.

### Refactoring with tests

The project was refactored from a functional approach to an object-oriented design while preserving behaviour through integration tests.

### Polymorphism

Standard and Cargo Rovers can be executed through the same mission-control interface.

### Persistence

Mission results can be saved and restored using JSON archives.

### Interface isolation

The CLI coordinates existing components rather than implementing navigation rules itself.

---

## 🔮 Possible Future Extensions

The core project is complete, but possible extensions include:

- Plateau obstacles
- Mission replay
- ASCII plateau visualisation
- Additional rover types
- State-machine driven CLI
- Async mission coordination using `asyncio`
