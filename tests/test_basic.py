import pickle
import string
import unittest

import yaml

from jinjyaml import JinjyamlConstructor, jinjyaml_render, JinjyamlRepresenter, JinjyamlObject

TAG = 'jinja'

YAML = string.Template('''
!${TAG} |
  {% for n in range(3) %}
  - attr_{{ n }}: {{ loop.index }}
  {% endfor %}
''').substitute(TAG=TAG)

DATA = [
    {'attr_0': 1},
    {'attr_1': 2},
    {'attr_2': 3},
]


class BasicTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        constructor = JinjyamlConstructor()
        yaml.add_constructor('!{}'.format(TAG), constructor)
        representer = JinjyamlRepresenter(TAG)
        yaml.add_representer(JinjyamlObject, representer)

    def test_construct(self):
        data = yaml.load(YAML, yaml.Loader)
        data = jinjyaml_render(data, yaml.Loader)
        self.assertListEqual(data, DATA)

    def test_represent_construct(self):
        data1 = yaml.load(YAML, yaml.Loader)
        data1 = jinjyaml_render(data1, yaml.Loader)
        txt = yaml.dump(data1)
        data2 = yaml.load(txt, yaml.Loader)
        data2 = jinjyaml_render(data2, yaml.Loader)
        self.assertListEqual(data1, data2)


class AutoRenderTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        constructor = JinjyamlConstructor(auto_render=True)
        yaml.add_constructor('!{}'.format(TAG), constructor)

    def test_auto_render(self):
        data = yaml.load(YAML, yaml.Loader)
        self.assertListEqual(data, DATA)


class SerializationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        constructor = JinjyamlConstructor()
        yaml.add_constructor('!{}'.format(TAG), constructor)
        representer = JinjyamlRepresenter(TAG)
        yaml.add_representer(JinjyamlObject, representer)

    def test_pickle(self):
        obj1 = yaml.load(YAML, yaml.Loader)
        data = pickle.dumps(obj1)
        obj2 = pickle.loads(data)
        obj2 = jinjyaml_render(obj2, yaml.Loader)
        self.assertListEqual(obj2, DATA)


if __name__ == '__main__':
    unittest.main()
