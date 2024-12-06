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

### Basic Example 1

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

## Advanced Usage

### Include files

#### Jinja2's include filter function

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

> ℹ️ **Note:** \
> Since [jinja2][]'s [`include`](https://jinja.palletsprojects.com/en/3.0.x/templates/#include) and [`indent`](https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.indent) do not work such nice with indention-sensitive languages like Python or YAML, it is not advised to use these features in complex cases.

#### pyyaml-include

[pyyaml-include][] provides a [pyyaml][] extension for including other YAML files.
Sometimes we use this extension instead of Jinja2's `include`/`indent` to help maintain the indentation of the YAML file.

1. install [pyyaml-include][]:

    ```bash
    pip install pyyaml-include
    ```

1. add both [pyyaml-include][] and `jinjyaml`'s constructor:

    ```python
    import yaml
    import jinjyaml as jy
    import pyyaml_include

    yaml.add_constructor("!j2", jy.Constructor)
    yaml.add_constructor("!inc", pyyaml_include.Constructor(base_dir="path_to_you_dir"))
    ```

1. Assume that we have YAML files same to previous example, the `main.yml` can be modified as below:

    ```yaml
    foo: !j2 |
      {% for i in range(n) %}
      - !inc sub-{{loop.index}}.yml
      {% endfor %}
    ```

1. include and load other YAML files:

    Assume that we have YAML files same to previous example:

    ```python
    with open("main.yml") as fp:
        doc = yaml.safe_load(fp)

    obj = jy.extract(doc, env)
    pprint(obj)
    ```

Then we'll get:

```json
{
  "foo": [
    {"1.1": "one", "1.2": "two" },
    {"2.1": {"2.1.1": "three", "2.1.2": "four"}}
  ]
}
```

In the situation, it's no necessary to use `jinja2.Environment` and `jinja2.FileSystemLoader` to render the template,
and also not necessary to use `filter indent` in the template.
Because [pyyaml-include] has parsed the file to object already.

> ❇️ **Conclusions:** \
> We can use [jinja2][]'s `include` and `indent` to include other YAML files **literally**, or to use [pyyaml-include][] to include other YAML files **as already-parsed objects**.

[jinja2]: https://jinja.palletsprojects.com/ "Jinja is a fast, expressive, extensible templating engine."
[pyyaml]: https://pyyaml.org/ "PyYAML is a full-featured YAML framework for the Python programming language."
[pyyaml-include]: https://github.com/tanbro/jinjyaml "An extending constructor of PyYAML: include other YAML files into current YAML document."
