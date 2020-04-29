class JinjayamlRepresenter:
    """Representer for Jinja2 template tags

    When dumping YAML into string, the class Represents template object into YAML tag text
    """

    def __init__(self, tag):
        self._tag = tag

    def __call__(self, dumper, data):
        return dumper.represent_scalar(f'!{self._tag}', data.source)
