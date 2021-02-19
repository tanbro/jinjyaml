# jinjyaml

[![GitHub tag](https://img.shields.io/github/tag/tanbro/jinjyaml.svg)](https://github.com/tanbro/jinjyaml)
[![Python Package](https://github.com/tanbro/jinjyaml/workflows/Python%20package/badge.svg)](https://github.com/tanbro/jinjyaml/actions?query=workflow%3A%22Python+package%22)
[![Documentation Status](https://readthedocs.org/projects/jinjyaml/badge/?version=stable)](https://jinjyaml.readthedocs.io/en/latest/?badge=latest)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=tanbro_jinjyaml&metric=alert_status)](https://sonarcloud.io/dashboard?id=tanbro_jinjyaml)
[![PyPI](https://img.shields.io/pypi/v/jinjyaml.svg)](https://pypi.org/project/jinjyaml/)

Application specific YAML tag of Jinja2 template

## Usage

```python
>>> from pprint import pprint
>>> import yaml
>>> from jinjyaml import JinjyamlConstructor, jinjyaml_render
>>> 
>>> txt = '''
... array:
...   !jinja2 |
...     {% for n in range(3) %}
...     - sub{{n}}: {{loop.index}}
...     {% endfor %}
... '''
>>> 
>>> loader_class = yaml.FullLoader
>>> constructor = JinjyamlConstructor()
>>> loader_class.add_constructor('!jinja2', constructor)
>>> obj = yaml.load(txt, loader_class)
>>> rendered = jinjyaml_render(obj, loader_class)
>>> pprint(rendered)
{'array': [{'sub0': 1}, {'sub1': 2}, {'sub2': 3}]}
```
