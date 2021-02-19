import unittest
from contextlib import ExitStack
from os import path
from textwrap import dedent

import jinja2
import yaml
from jinjyaml import JinjyamlConstructor, jinjyaml_render

TAG = 'j2'
SEARCH_PATH = 'tests'


class IncludeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        j2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(SEARCH_PATH)
        )
        constructor = JinjyamlConstructor(
            env=j2_env
        )
        yaml.add_constructor('!{}'.format(TAG), constructor)

    def test_include_mapping(self):
        doc = yaml.load(
            dedent('''
            foo: !j2 |
                {% include "child-1.yml" %}
                {% include "child-2.yml" %}
            '''),
            yaml.Loader
        )

        data = jinjyaml_render(doc, yaml.Loader)

        foo = dict()
        with ExitStack() as stack:
            files = [
                stack.enter_context(open(path.join(SEARCH_PATH, fname)))
                for fname in ("child-1.yml", "child-2.yml")
            ]
            for file in files:
                foo.update(yaml.load(file, yaml.Loader))
        self.assertDictEqual(data, {"foo": foo})


if __name__ == '__main__':
    unittest.main()
