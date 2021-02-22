import pickle
import string
import unittest

import jinjyaml
import yaml

TAG = 'j2'

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
        constructor = jinjyaml.Constructor()
        yaml.add_constructor('!{}'.format(TAG), constructor)
        representer = jinjyaml.Representer(TAG)
        yaml.add_representer(jinjyaml.Data, representer)

    def test_construct(self):
        obj = yaml.load(YAML, yaml.Loader)
        data = jinjyaml.extract(obj)
        self.assertListEqual(data, DATA)

    def test_represent_construct(self):
        obj1 = yaml.load(YAML, yaml.Loader)
        data1 = jinjyaml.extract(obj1)
        txt = yaml.dump(data1)
        obj2 = yaml.load(txt, yaml.Loader)
        data2 = jinjyaml.extract(obj2)
        self.assertListEqual(data1, data2)


class SerializationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        constructor = jinjyaml.Constructor()
        yaml.add_constructor('!{}'.format(TAG), constructor)
        representer = jinjyaml.Representer(TAG)
        yaml.add_representer(jinjyaml.Data, representer)

    def test_pickle(self):
        obj1 = yaml.load(YAML, yaml.Loader)
        data = pickle.dumps(obj1)
        obj2 = pickle.loads(data)
        obj2 = jinjyaml.extract(obj2)
        self.assertListEqual(obj2, DATA)


if __name__ == '__main__':
    unittest.main()
