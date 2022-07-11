import os
from rq import Queue
from redis import Redis


from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi_app import settings
from fastapi_app import simulation


app = FastAPI()

redis = Redis.from_url(settings.REDIS_URL)
q = Queue(connection=redis)

app.mount(
    "/static", StaticFiles(directory=os.path.join(settings.SERVER_ROOT, "static")), name="static"
)

templates = Jinja2Templates(directory=os.path.join(settings.SERVER_ROOT, "templates"))


# Test Driven Development --> https://fastapi.tiangolo.com/tutorial/testing/


@app.get("/")
def index(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/run_simulation")
def run_simulation(request: Request) -> Response:
    """Send a simulation task to a celery worker"""
    example_path = settings.DATAPACKAGES_DIR / "examples" / "dispatch" / "datapackage.json"
    job = q.enqueue(simulation.simulate_energysystem, path=str(example_path))
    return templates.TemplateResponse(
        "submitted_task.html", {"request": request, "job_id": job.id}
    )


@app.get("/check/{job_id}")
async def check_job(job_id: str) -> JSONResponse:
    job = q.fetch_job(job_id)
    if (status := job.get_status()) != "finished":
        return JSONResponse(content=status)
    return JSONResponse(content=job.result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
