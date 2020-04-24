class JinjaTemplateGenerateStreamReader:
    def __init__(self, iterable):
        self._iterable = iter(iterable)

    def read(self, _):
        try:
            return next(self._iterable)
        except StopIteration:
            return ''
