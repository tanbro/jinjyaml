import pickle
import string
import unittest

import yaml

import jinjyaml

TAG = 'j2'

YAML = string.Template('''
data: !${TAG} |
  {% for n in range(3) %}
  - attr_{{ n }}: {{ loop.index }}
  {% endfor %}
''').substitute(TAG=TAG)

DATA = {
    'data': [
        {'attr_0': 1},
        {'attr_1': 2},
        {'attr_2': 3},
    ]
}


class BasicTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        constructor = jinjyaml.Constructor()
        yaml.add_constructor('!{}'.format(TAG), constructor)
        representer = jinjyaml.Representer(TAG)
        yaml.add_representer(jinjyaml.Data, representer)

    def test_construct(self):
        obj = yaml.load(YAML, yaml.Loader)
        result = jinjyaml.extract(obj)
        self.assertListEqual(result['data'], DATA['data'])

    def test_inplace_extract(self):
        obj = yaml.load(YAML, yaml.Loader)
        jinjyaml.extract(obj, inplace=True)
        self.assertListEqual(obj['data'], DATA['data'])

    def test_represent_construct(self):
        obj1 = yaml.load(YAML, yaml.Loader)
        data1 = jinjyaml.extract(obj1)
        txt = yaml.dump(data1)
        obj2 = yaml.load(txt, yaml.Loader)
        data2 = jinjyaml.extract(obj2)
        self.assertListEqual(data1['data'], data2['data'])


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
        self.assertListEqual(obj2['data'], DATA['data'])


if __name__ == '__main__':
    unittest.main()
