# Development install

Install the package with its dependencies:

```shell
git clone https://github.com/FAIRmat-NFDI/pynxtools-xrd.git \\
    --branch main \\
    --recursive pynxtools_xrd
cd pynxtools_xrd
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install -e ".[dev]"
```

There is also a [pre-commit hook](https://pre-commit.com/#intro) available
which formats the code and checks the linting before actually committing.
It can be installed with
```shell
pre-commit install
```
from the root of this repository.

