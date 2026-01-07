## Dev Setup (Windows)

```bat
py -3.12 -m pip install --upgrade uv
uv sync
uvx pre-commit install

## Dev Setup (Windows)

```bat
py -3.12 -m pip install --upgrade uv
uvx pre-commit install
```

## Checks (wie CI)

```bat
uvx ruff format --check .
uvx ruff check .
```
