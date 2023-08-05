#
# (C) 2014-2017 Seiji Matsuoka
# Licensed under the MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import functools
import json
import traceback

from chorus import rdkit
from chorus.model.graphmol import Compound

from flashflood.node.function.filter import MPFilter
from flashflood.node.chem.molecule import AsyncMolecule
from flashflood.node.function.number import AsyncNumber
from flashflood.node.reader.sqlite import SQLiteReader
from flashflood.node.writer.container import AsyncContainerWriter
from flashflood.sqlitehelper import SQLITE_HELPER as sq
from flashflood.workflow.responseworkflow import ResponseWorkflow


def rdmorgan_filter(qmol, params, row):
    mol = Compound(json.loads(row["__molobj"]))
    try:
        score = rdkit.morgan_sim(mol, qmol, radius=2)  # ECFP4 equivalent
    except:
        print(traceback.format_exc())
        return
    thld = float(params["threshold"])
    if score >= thld:
        row["morgan_sim"] = score
        return row


class RDKitMorgan(ResponseWorkflow):
    def __init__(self, query, **kwargs):
        super().__init__(query, **kwargs)
        qmol = sq.query_mol(query["queryMol"])
        func = functools.partial(rdmorgan_filter, qmol, query["params"])
        sq_in = SQLiteReader(query)
        mpf = MPFilter(
            func, fields=[
                {"key": "morgan_sim", "name": "Fingerprint similarity",
                 "d3_format": ".2f"}
            ]
        )
        molecule = AsyncMolecule()
        number = AsyncNumber()
        writer = AsyncContainerWriter(self.results)
        self.connect(sq_in, mpf)
        self.connect(mpf, molecule)
        self.connect(molecule, number)
        self.connect(number, writer)
