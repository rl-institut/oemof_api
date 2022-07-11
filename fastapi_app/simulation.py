"""Simulation module"""

import json

# pylint: disable=W0611
import oemof.tabular.datapackage  # noqa
from oemof import solph
from oemof.network.energy_system import EnergySystem
from oemof.tabular.facades import TYPEMAP

from fastapi_app.settings import DATAPACKAGES_DIR


def simulate_energysystem(path):
    """
    Simulates ES, stores results to DB and returns simulation ID

    Parameters
    ----------
    path : str
        Path to oemof.tabular energysystem datapackage

    Returns
    -------
    simulation_id : int
        Simulation ID to restore results from
    """
    energysystem = EnergySystem.from_datapackage(path, typemap=TYPEMAP)
    model = solph.Model(energysystem)
    model.solve(solver="cbc")
    results = solph.processing.results(model)
    results = solph.processing.convert_keys_to_strings(results)
    results = {str(key): value for key, value in results.items()}
    return json.dumps(results)


if __name__ == "__main__":
    dispatch_example_path = (
        DATAPACKAGES_DIR / "examples" / "dispatch" / "datapackage.json"
    )
    print(simulate_energysystem(str(dispatch_example_path)))
