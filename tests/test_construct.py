import unittest

import yaml
from jinjyaml import JinjaConstructor, render_object, JinjayamlRepresenters, JinjyamlObject

TAG = 'jinja'

YAML = '''
!jinja |
  {% for n in range(3) %}
  - {{ loop.index }}: value is {{ n }}
  {% endfor %}
'''


class MyTestCase(unittest.TestCase):
    def test_something(self):
        constructor = JinjaConstructor()
        yaml.add_constructor(f'!{TAG}', constructor)
        representer = JinjayamlRepresenters(TAG)
        yaml.add_representer(JinjyamlObject, representer)

        o1 = yaml.load(YAML, yaml.Loader)
        s = yaml.dump(o1)
        o2 = yaml.load(s, yaml.Loader)
        self.assertListEqual(
            render_object(o1),
            render_object(o2)
        )


if __name__ == '__main__':
    unittest.main()
