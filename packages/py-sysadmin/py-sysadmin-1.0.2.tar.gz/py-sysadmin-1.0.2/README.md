## Install

### PyPI

```sh
pip install sysadmin
```

### Local

```sh
pip install -r requirements.txt
python setup.py build
pip install .
```

### Development

```sh
pip install -r dev-requirements.txt
python setup.py build
pip install -e .
nosetests
pre-commit run -a
```
