
from oemof.network.energy_system import EnergySystem

from oemof import solph
import oemof.tabular.datapackage  # noqa
from oemof.tabular.facades import TYPEMAP
from fastapi_app.settings import DATAPACKAGES_DIR


def simulate_energysystem(path):
    es = EnergySystem.from_datapackage(path, typemap=TYPEMAP)
    model = solph.Model(es)
    model.solve(solver="cbc")
    return solph.processing.results(model)


if __name__ == "__main__":
    dispatch_example_path = DATAPACKAGES_DIR / "examples" / "dispatch" / "datapackage.json"
    results = simulate_energysystem(str(dispatch_example_path))
    print(results)
