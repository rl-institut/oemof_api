"""Simulation module"""

# pylint: disable=W0611
import oemof.tabular.datapackage  # noqa
from oemof import solph
from oemof.network.energy_system import EnergySystem
from oemof.tabular.facades import TYPEMAP
from sqlalchemy.orm import Session

from fastapi_app import database, settings


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

    input_data = solph.processing.parameter_as_dict(
        energysystem,
        exclude_attrs=["bus", "from_bus", "to_bus", "from_node", "to_node"],
    )
    results_data = solph.processing.results(model)

    with Session(settings.engine) as session:
        simulation_id = database.store_results(session, input_data, results_data)
    return simulation_id


def restore_results(simulation_id):
    """
    Restore results from DB and JSON-encode it

    Parameters
    ----------
    simulation_id: int
        Simulation ID to restore results from

    Returns
    -------
    results: dict
        JSON-encoded results from database
    """
    with Session(settings.engine) as session:
        _, results = database.restore_results(session, simulation_id)
    # Result contains tuples as keys and pandas.Series in sequences:
    results = {
        str(key): {
            "scalars": data["scalars"],
            "sequences": {
                key: series.to_dict() for key, series in data["sequences"].items()
            },
        }
        for key, data in results.items()
    }
    return results


if __name__ == "__main__":
    dispatch_example_path = (
        settings.DATAPACKAGES_DIR / "examples" / "dispatch" / "datapackage.json"
    )
    print(simulate_energysystem(str(dispatch_example_path)))
