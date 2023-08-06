from ..utils import Logger


class Experiment:
    def __init__(self, opts):
        self.opts = opts
        self.logger = Logger()
        self.experimentClass = self.__class__.__name__

    def process(self, filepath):
        raise NotImplementedError(
            "Experiment class requires a `process` method.")
