# Advent of Code 2023

<img src="https://img.shields.io/badge/2023-40%20⭐-990000?style=flat-square"></img>

This repository contains my solution approaches for the [Advent of Code 2023](https://adventofcode.com/2023),
implemented in Python. It is structured as follows:

- `adventofcode`:
    - `framework`: This (probably slightly over-engineered) package mainly accommodates all the code related to
      automation.
    - `utils`: Currently, this package is empty, but it is planned to put all the functionalities, which are useful
      across different solutions, in there.
- `bin`: Scripts for automatically selecting and running today's solution,
  as well as for creating files and folders for the current day, can be found here.
- `solutions`: This folder contains all the solution approaches, some already refined, but most of them unoptimized.

**Running the solutions**

The solutions can be run with the following command:

```bash
python bin/run_solutions.py config.json [--day <day>] [--test]
```

If the `day` argument is omitted, the current date is used.
The `test` flag runs the solution with an example input, instead of the real puzzle input.
Additionally, in order for the above command to work, the puzzle input must be present in the
`input/day_<DD>.txt` (or `input/day_<DD>_example.txt` respectively) file and it might be necessary to
add the top-level directory to `$PYTHONPATH`.

Requirements:

- Python: `3.11.6`
- For some solutions the packages from the `requirements.txt` have to be installed.
