# jinjyaml

[![CircleCI](https://circleci.com/gh/tanbro/jinjyaml.svg?style=svg)](https://circleci.com/gh/tanbro/jinjyaml)
[![Documentation Status](https://readthedocs.org/projects/jinjyaml/badge/?version=latest)](https://jinjyaml.readthedocs.io/en/latest/?badge=latest)
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
