import unittest
from contextlib import ExitStack
from pathlib import Path
from secrets import token_hex

import jinja2
import yaml

import jinjyaml as jy

from .loaders import LOADERS

TAG = "j2"
SEARCH_PATH = "tests"


class IncludeTestCase(unittest.TestCase):
    j2_env = None

    @classmethod
    def setUpClass(cls):
        cls.j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(SEARCH_PATH))
        ctor = jy.Constructor()
        for Loader in LOADERS:
            yaml.add_constructor(f"!{TAG}", ctor, Loader)

    def test_simple_include(self):
        files = "child-1.yml", "child-2.yml"
        string = """
        foo: !j2 |
            {% for fname in files %}
            {% filter indent %}
            {% include fname %}
            {% endfilter %}
            {% endfor %}
        """
        for Loader in LOADERS:
            doc = yaml.load(string, Loader)
            data = jy.extract(doc, Loader, env=self.j2_env, context={"files": files})
            foo = dict()
            with ExitStack() as stack:
                for fp in (stack.enter_context(Path(SEARCH_PATH, fname).open()) for fname in files):
                    foo.update(yaml.load(fp, Loader))
            self.assertDictEqual(data, {"foo": foo}, f"{Loader}")

    def test_cascade_include(self):
        string = """
        foo: !j2 |
            {% filter indent %}
            {% include "child-x.yml.j2" %}
            {% endfilter %}
        """
        for Loader in LOADERS:
            doc = yaml.load(string, Loader)
            value = token_hex()
            data = jy.extract(doc, Loader, env=self.j2_env, context={"value": value})
            o = jy.extract(data, Loader, env=self.j2_env)
            foo = o["foo"]
            x = foo["x"]
            y = x["y"]
            self.assertEqual(y.strip(), value)


if __name__ == "__main__":
    unittest.main()
