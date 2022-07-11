"""FastAPI web services"""

import os

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from redis import Redis
from rq import Queue

from fastapi_app import settings, simulation

app = FastAPI()

redis = Redis.from_url(settings.REDIS_URL)
q = Queue(connection=redis)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(settings.SERVER_ROOT, "static")),
    name="static",
)

templates = Jinja2Templates(directory=os.path.join(settings.SERVER_ROOT, "templates"))


# Test Driven Development --> https://fastapi.tiangolo.com/tutorial/testing/


@app.get("/")
def index(request: Request) -> Response:
    """Homepage"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/run_simulation")
def run_simulation(request: Request) -> Response:
    """
    Send a simulation task to rq queue

    Parameters
    ----------
    request: Request
        Simulation request

    Returns
    -------
    Response:
        Job id
    """
    example_path = (
        settings.DATAPACKAGES_DIR / "examples" / "dispatch" / "datapackage.json"
    )
    job = q.enqueue(simulation.simulate_energysystem, path=str(example_path))
    return templates.TemplateResponse(
        "submitted_task.html", {"request": request, "job_id": job.id}
    )


@app.get("/check/{job_id}")
async def check_job(job_id: str) -> JSONResponse:
    """Check status of job"""
    job = q.fetch_job(job_id)
    if (status := job.get_status()) != "finished":
        return JSONResponse(content=status)
    results = simulation.restore_results(simulation_id=job.result)
    return JSONResponse(content=results)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
