class JinjayamlRepresenters:
    def __init__(self, tag):
        self._tag = tag

    def __call__(self, dumper, data):
        return dumper.represent_scalar(f'!{self._tag}', data.source)
