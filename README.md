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

### Example 1

```python
>>> import yaml
>>> import jinjyaml as jy
>>>
>>> ctor = jy.Constructor()
>>> yaml.add_constructor('!j2', ctor, yaml.FullLoader)
>>>
>>> s = '''
... array:
...   !j2 |
...     {% for i in range(n) %}
...     - sub{{i}}: {{loop.index}}
...     {% endfor %}
... '''
>>>
>>> obj = yaml.full_load(s)
>>>
>>> data = jy.extract(obj, context={'n': 3})
>>> print(data)
{'array': [{'sub0': 1}, {'sub1': 2}, {'sub2': 3}]}
```

### Example 2

We have such YAML files:

- `child-1.yml`:

  ```yaml
  "1.1": one
  "1.2": two
  ```

- `child-2.yml`:

  ```yaml
  "2.1":
    "2.1.1": three
    "2.1.2": four
  ```

- `main.yml`:

  ```yaml
  children: !j2 |

    {% include "child-1.yml" %}
    {% include "child-2.yml" %}
  ```

execute python code:

```python
from pprint import pprint

import jinjyaml as jy
import yaml

env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))

ctor = jy.Constructor()
yaml.add_constructor('!j2', ctor, yaml.FullLoader)

with open('main.yml') as fp:
    doc = yaml.full_load(fp)

obj = jy.extract(doc, env)
pprint(obj)
```

We'll get:

```python
{'foo': {'1.1': 'one',
         '1.2': 'two',
         '2.1': {'2.1.1': 'three', '2.1.2': 'four'}}}
```

[jinja2]: https://jinja.palletsprojects.com/ "Jinja is a modern and designer-friendly templating language for Python"
[pyyaml]: https://pyyaml.org/ "PyYAML is a full-featured YAML framework for the Python programming language."
