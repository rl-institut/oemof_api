# Oemof API

API to simulate energysystems using energy datapackages from [oemof_tabular](https://github.com/oemof/oemof-tabular).

## Get started

Run `sudo docker-compose up -d --build` to run the task queue and the webapp simulaneously.

Now the webapp is available at `127.0.0.1:5001`

Run `sudo docker-compose down` to shut the services down.

## Develop while services are running

### Using [redis](https://redis.io/documentation)

You have to start redis-server
`service redis-server start`
(to stop it use `service redis-server stop`)
Move to `task_queue` and run `. setup_redis.sh` to start the celery queue with redis a message
 broker.
We cannot use celery, as there is a dependency conflict (click versions differ) with oemof_tabular.
Instead, we are going for [RQ](https://github.com/rq/rq) (Redis Queue)
(from docs: "RQ (Redis Queue) is a simple Python library for queueing jobs and processing them in the background with workers.
It is backed by Redis and it is designed to have a low barrier to entry. It should be integrated in your web stack easily.")

### Using [RQ](https://python-rq.org/docs/)

Start RQ task queue via `rq worker`.

### Using [fastapi](https://fastapi.tiangolo.com/)

In another terminal go the the root of the repo and run `. fastapi_run.sh`

Now the fastapi app is available at `127.0.0.1:5001`


## Docs

To build the docs simply go to the `docs` folder

    cd docs

Install the requirements

    pip install -r docs_requirements.txt

and run

    make html

The output will then be located in `docs/_build/html` and can be opened with your favorite browser

## Code linting

Please install pre-commit via `pre-commit install`. This will enanble all lintings from `.pre-commit-config.yaml`.
