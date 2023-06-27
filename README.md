# jinjyaml

[![GitHub tag](https://img.shields.io/github/tag/tanbro/jinjyaml.svg)](https://github.com/tanbro/jinjyaml)
[![Python Package](https://github.com/tanbro/jinjyaml/actions/workflows/python-package.yml/badge.svg)](https://github.com/tanbro/jinjyaml/actions/workflows/python-package.yml)
[![PyPI](https://img.shields.io/pypi/v/jinjyaml.svg)](https://pypi.org/project/jinjyaml/)
[![Documentation Status](https://readthedocs.org/projects/jinjyaml/badge/?version=latest)](https://jinjyaml.readthedocs.io/en/latest/?badge=latest)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=tanbro_jinjyaml&metric=alert_status)](https://sonarcloud.io/dashboard?id=tanbro_jinjyaml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=tanbro_jinjyaml&metric=coverage)](https://sonarcloud.io/summary/new_code?id=tanbro_jinjyaml)

Application specific tag of [Jinja2][] template in [PyYAML][].

It may be useful if you only want to render special tag nodes in the document,
instead of whole YAML string as a template.

## Usage

### Example 1

1. Add `Jinja2` template constructor for tag `"!j2"`

   ```python
   import yaml
   import jinjyaml as jy

   ctor = jy.Constructor()
   yaml.add_constructor("!j2", ctor, yaml.SafeLoader)
   ```

1. create `YAML` file `1.yml`, with such contents:

   ```yaml
   array: !j2 |
     {% for i in range(n) %}
     - sub{{i}}: {{loop.index}}
     {% endfor %}
   ```

1. load and render the `YAML` file

   ```python
   with open("1.yml") as fp:
       data = yaml.load(fp, Loader=yaml.SafeLoader)
       # or for the short:
       # data = yaml.safe_load(fp)

   jy.extract(data, context={"n": 3}, inplace=True)

   print(data)
   ```

We'll get:

```json
{"array": [{"sub0": 1}, {"sub1": 2}, {"sub2": 3}]}
```

### Example 2

We have such YAML files:

- `sub-1.yml`:

  ```yaml

  "1.1": one
  "1.2": two
  ```

- `sub-2.yml`:

  ```yaml

  "2.1":
    "2.1.1": three
    "2.1.2": four
  ```

- `main.yml`:

  ```yaml
  foo: !j2 |

    {% filter indent %}
    {% include "sub-1.yml" %}
    {% endfilter %}

    {% filter indent %}
    {% include "sub-2.yml" %}
    {% endfilter %}
  ```

execute python code:

```python
from pprint import pprint

import jinja2
import jinjyaml as jy
import yaml

env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))

ctor = jy.Constructor()
yaml.add_constructor("!j2", ctor, yaml.SafeLoader)

with open("main.yml") as fp:
    doc = yaml.safe_load(fp)

obj = jy.extract(doc, env)
pprint(obj)
```

We'll get:

```json
{"foo": {"1.1": "one",
         "1.2": "two",
         "2.1": {"2.1.1": "three", "2.1.2": "four"}}}
```

> **NOTE:**
>
> Since [Jinja2][]'s [`include`](https://jinja.palletsprojects.com/en/3.0.x/templates/#include) and [`indent`](https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.indent) do not work very nice with indention languages like Python or YAML, it's not advised to use the feature in a complex case.

[jinja2]: https://jinja.palletsprojects.com/ "Jinja is a fast, expressive, extensible templating engine."
[pyyaml]: https://pyyaml.org/ "PyYAML is a full-featured YAML framework for the Python programming language."
