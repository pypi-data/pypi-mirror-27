#
# (C) 2014-2017 Seiji Matsuoka
# Licensed under the MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import itertools
from flashflood.core.node import SyncNode


class IteratorInput(SyncNode):
    def __init__(self, iter_input, fields=None, params=None):
        super().__init__(params=params)
        self.iter_input = iter_input
        if fields is not None:
            self.fields.merge(fields)

    def on_submitted(self):
        main, counter = itertools.tee(self.iter_input)
        self._out_edge.records = main
        if self.fields:
            self._out_edge.fields.merge(self.fields)
        self._out_edge.params.update(self.params)
