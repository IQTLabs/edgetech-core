## How to Contribute

In order to contribute to this module, you must pass the code checks below. Please integrate them into your workflow before submitting a pull request as they will run before being allowed to merge. 

```bash
black --diff --check *.py
pylint --disable=all --enable=unused-import *.py
mypy --allow-untyped-decorators --ignore-missing-imports --no-warn-return-any --strict *.py
```

You can install these checks using the command below.
```
pip install "black<23" pylint==v3.0.0a3 mypy==v0.991
```