# course-prereq-team3

A basic FastAPI application.

## Setup

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Adding new dependencies

If you need to add new dependencies, you can do so by running:

```sh
pip install <package-name>
pip freeze > requirements.txt
```

Only run this with your virtual environment activated. Otherwise, you will modify your global Python environment's packages and incorrectly write to the requirements.txt file.

## Run Dev Instance

```sh
uv run fastapi dev main.py
```

Open http://127.0.0.1:8000/ to see the JSON response.

## Run Linting

Count should be 0 (no linting errors).

```sh
flake8 . --count --show-source --statistics --exclude=.venv
```

## Run Tests

```sh
pytest
```
See https://docs.pytest.org/en/stable/getting-started.html for more information on how to write and run tests with pytest.
