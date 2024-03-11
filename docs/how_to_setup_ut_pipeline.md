## Target:
Full unit test pipeline with full fledged script or code for Python using makefile, Poetry and Pytest to allow use running the whole process using command like "make format", "make lint", "make test", the folder hierarchy was like:

```plaintext
.
├── Makefile
├── README.md
├── langchain_community
│ ├── init.py
│ ├── pycache
│ ├── adapters
│ ├── agent_toolkits
│ ├── cache.py
│ ├── callbacks
│ ├── chat_loaders
│ ├── chat_message_histories
│ ├── chat_models
│ ├── docstore
│ ├── document_compressors
│ ├── document_loaders
│ ├── document_transformers
│ ├── embeddings
│ ├── example_selectors
│ ├── graphs
│ ├── indexes
│ ├── llms
│ ├── output_parsers
│ ├── py.typed
│ ├── retrievers
│ ├── storage
│ ├── tools
│ ├── utilities
│ ├── utils
│ └── vectorstores
├── poetry.lock
├── pyproject.toml
├── scripts
│ ├── check_imports.py
│ ├── check_pydantic.sh
│ └── lint_imports.sh
└── tests
├── init.py
├── pycache
├── data.py
├── examples
├── integration_tests
└── unit_tests
```

To create a full unit test pipeline for your Python project using Makefile, Poetry, and Pytest, follow these steps:

1. **Poetry Setup**: Ensure `poetry` is installed on the system. It is used for dependency management and packaging in Python projects. The `pyproject.toml` file will hold all the necessary configurations.

2. **Makefile**: The `Makefile` will define commands to run formatting, linting, and testing. It should be placed in the root directory.

3. **Pytest Configuration**: Configure `pytest` to recognize your tests directory and any additional configuration settings you might need.

Here's an example setup for your project:

### pyproject.toml

```toml
[tool.poetry]
name = "langchain_community"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"

[tool.poetry.dev-dependencies]
pytest = "^6.0"

[tool.pytest.ini_options]
minversion = "6.0"
testpaths = [
    "tests/unit_tests",
    "tests/integration_tests",
]
addopts = "-ra -q"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### Makefile

```makefile
.PHONY: format lint test

format:
	@echo "Formatting code"
	poetry run black langchain_community tests

lint:
	@echo "Linting code"
	poetry run flake8 langchain_community tests
	poetry run mypy langchain_community tests
	@echo "Checking for proper imports"
	./scripts/check_imports.py
	./scripts/lint_imports.sh
	./scripts/check_pydantic.sh

test:
	@echo "Running unit tests"
	poetry run pytest

# Additional targets for setting up the environment, cleaning build artifacts, etc.
```

### Installing Dependencies

Before you can run the `Makefile` commands, you need to install the project dependencies and dev dependencies. You can do this by running:

```bash
poetry install
```

### Running the Commands

To format your code, you can run:

```bash
make format
```

To lint your code, you can run:

```bash
make lint
```

To run your tests, you can run:

```bash
make test
```

### Scripts

Ensure that the scripts in the `scripts` directory are executable. You can make them executable by running:

```bash
chmod +x scripts/*.py
chmod +x scripts/*.sh
```

### Pytest

Write your unit tests in the `tests/unit_tests` directory. Pytest is configured to automatically discover tests in the directories specified in the `pyproject.toml` file.

### Additional Notes

- The `@echo` command in the `Makefile` is used to print a message before each command is run.
- Ensure that `black`, `flake8`, and `mypy` are listed in the `poetry` dev dependencies if you're using them for formatting and linting.
- You may need to adjust the scripts in the `scripts` directory to match the linting and import checks you require.
- The `.PHONY` target in the `Makefile` is used to declare that the following targets are not files.

This setup provides a robust starting point for a unit test pipeline in an AWS environment. You can expand and modify this setup according to the specific needs of your project.

## Tutorial to start 
