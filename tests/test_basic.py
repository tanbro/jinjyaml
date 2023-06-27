import pickle
import string
import unittest
from random import randint

import yaml

import jinjyaml as jy

from .loaders import LOADERS

TAG = "j2"

YAML = string.Template(
    """
    data: !${TAG} |
        {% for n in range(3) %}
        - attr_{{ n }}: {{ loop.index }}
        {% endfor %}
    """
).substitute(TAG=TAG)

DATA = {
    "data": [
        {"attr_0": 1},
        {"attr_1": 2},
        {"attr_2": 3},
    ]
}


class BasicTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctor = jy.Constructor()
        for Loader in LOADERS:
            yaml.add_constructor(f"!{TAG}", ctor, Loader)
        rprt = jy.Representer(TAG)
        yaml.add_representer(jy.Data, rprt)

    def test_construct(self):
        for Loader in LOADERS:
            obj = yaml.load(YAML, Loader)
            result = jy.extract(obj)
            self.assertListEqual(result["data"], DATA["data"], f"{Loader}")

    def test_inplace_extract(self):
        for Loader in LOADERS:
            obj = yaml.load(YAML, Loader)
            jy.extract(obj, inplace=True)
            self.assertListEqual(obj["data"], DATA["data"])

    def test_inplace_extract_list(self):
        s = string.Template(
            """
            - !${TAG} |
                {% for _ in range(n) %}
                - {{ loop.index }}
                {% endfor %}
            """
        ).substitute(TAG=TAG)
        for Loader in LOADERS:
            n = randint(1, 100)
            obj = yaml.load(s, Loader)
            jy.extract(obj, inplace=True, context={"n": n})
            self.assertListEqual(obj[0], [x + 1 for x in range(n)])

    def test_load_from_represent(self):
        for Loader in LOADERS:
            obj1 = yaml.load(YAML, Loader)
            txt = yaml.dump(obj1)
            obj2 = yaml.load(txt, Loader)
            data2 = jy.extract(obj2)
            self.assertListEqual(DATA["data"], data2["data"])

    def test_reload_extracted(self):
        for Loader in LOADERS:
            obj1 = yaml.load(YAML, Loader)
            data1 = jy.extract(obj1)
            txt = yaml.dump(data1)
            obj2 = yaml.load(txt, Loader)
            data2 = jy.extract(obj2)
            self.assertListEqual(data1["data"], data2["data"])

    def test_tag_type_complex(self):
        s = """
        x: !j2 [1,2,3]
        """
        for Loader in LOADERS:
            with self.assertRaises(TypeError):
                yaml.load(s, Loader)


class SerializationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctor = jy.Constructor()
        for Loader in LOADERS:
            yaml.add_constructor(f"!{TAG}", ctor, Loader)

    def test_pickle(self):
        for Loader in LOADERS:
            obj1 = yaml.load(YAML, Loader)
            data = pickle.dumps(obj1)
            obj2 = pickle.loads(data)
            obj2 = jy.extract(obj2)
            self.assertListEqual(obj2["data"], DATA["data"])


if __name__ == "__main__":
    unittest.main()
