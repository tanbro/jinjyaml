# jinjyaml

[![GitHub tag](https://img.shields.io/github/tag/tanbro/jinjyaml.svg)](https://github.com/tanbro/jinjyaml)
[![Test Python Package](https://github.com/tanbro/jinjyaml/actions/workflows/python-package.yml/badge.svg)](https://github.com/tanbro/jinjyaml/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/jinjyaml/badge/?version=latest)](https://jinjyaml.readthedocs.io/en/latest/?badge=latest)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=tanbro_jinjyaml&metric=alert_status)](https://sonarcloud.io/dashboard?id=tanbro_jinjyaml)
[![PyPI](https://img.shields.io/pypi/v/jinjyaml.svg)](https://pypi.org/project/jinjyaml/)

Application specific tag of [Jinja2][] template in [PyYAML][].

It may be useful if you only want to render special tag nodes in the document,
instead of whole YAML string as a template.

## Usage

```python
>>> import yaml
>>> import jinjyaml
>>>
>>> yaml.add_constructor('!j2', jinjyaml.Constructor())
>>>
>>> s = '''
... array:
...   !j2 |
...     {% for i in range(n) %}
...     - sub{{i}}: {{loop.index}}
...     {% endfor %}
... '''
>>>
>>> obj = yaml.load(s)
>>>
>>> data = jinjyaml.extract(obj, context={'n': 3})
>>> print(data)
{'array': [{'sub0': 1}, {'sub1': 2}, {'sub2': 3}]}
```

[Jinja2]: https://jinja.palletsprojects.com/ "Jinja is a modern and designer-friendly templating language for Python"
[PyYAML]: https://pyyaml.org/ "PyYAML is a full-featured YAML framework for the Python programming language."
