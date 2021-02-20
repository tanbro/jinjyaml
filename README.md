# jinjyaml

[![GitHub tag](https://img.shields.io/github/tag/tanbro/jinjyaml.svg)](https://github.com/tanbro/jinjyaml)
[![Test Python Package](https://github.com/tanbro/jinjyaml/actions/workflows/python-package.yml/badge.svg)](https://github.com/tanbro/jinjyaml/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/jinjyaml/badge/?version=latest)](https://jinjyaml.readthedocs.io/en/latest/?badge=latest)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=tanbro_jinjyaml&metric=alert_status)](https://sonarcloud.io/dashboard?id=tanbro_jinjyaml)
[![PyPI](https://img.shields.io/pypi/v/jinjyaml.svg)](https://pypi.org/project/jinjyaml/)

Application specific YAML tag of Jinja2 template

## Usage

```python
>>> import jinjyaml
>>> import yaml
>>>
>>> txt = '''
... array:
...   !j2 |
...     {% for n in range(3) %}
...     - sub{{n}}: {{loop.index}}
...     {% endfor %}
... '''
>>>
>>> constructor = jinjyaml.Constructor()
>>> yaml.add_constructor('!j2', constructor)
>>> obj = yaml.load(txt, yaml.Loader)
>>> jinjyaml.extract(obj, yaml.Loader)
{'array': [{'sub0': 1}, {'sub1': 2}, {'sub2': 3}]}
```
