Pre-commit/Pre-push
--------------------
This section sets up pre-commit and pre-push hooks in order to
ensure code style and code formatting and ensure security and testing is in place.


Installation [ Note that this step is already done in docker entry point ]
```bash
pre-commit install
pre-commit install --hook-type pre-push
```

Run all
```bash
pre-commit run --all-files
```

Clean up incase something goes wrong

```bash
pre-commit clean
```

Once this is done when you commit
    isort ( Sort imports )
    -> black ( Code formatting a.k.a gofmt )
    -> flake8 ( Code linting )
    -> mypy ( Static type checking )
    -> bandit ( Security checks )
In that order.

Before you git push the pytest with coverage gets run.
