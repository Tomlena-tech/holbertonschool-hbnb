# Running Tests

This document provides instructions on how to run the tests for the project.

Run the tests using the following command:

```bash
make test
```
This will execute all test files located in the `test_models/` directory.

For running a specific test file, use the command:

```bash
make single file=<test_file_name>
```
Replace `<test_file_name>` with the name of the test file you want to run, for example: `test_base_model.py`

To clean up Python cache files, use the command:

```bash
make clean
```

To view the help message with all available commands, use:

```bash
make help
```

The help message will display the following options:

```
  make test          - Run all test files in test_models/
  make single file=... - Run a single test file (e.g. make single file=test_models/test_base_model.py)
  make clean         - Remove Python cache files
  make help          - Show this help message
```
