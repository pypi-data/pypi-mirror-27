from brainiak.searchlight.searchlight import Searchlight
from brainiak.searchlight.searchlight import Diamond

from .Experiment import Experiment


class SearchlightExperiment(Experiment):
    def __init__(self, opts):
        super(SearchlightExperiment, self).__init__(opts)

    def process(self, filepath):
        pass
