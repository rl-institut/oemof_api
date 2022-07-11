# Manuals from
# https://pythonspeed.com/articles/conda-docker-image-size/
# https://pythonspeed.com/articles/activate-conda-dockerfile/
# https://jcristharif.com/conda-docker-tips.html
FROM continuumio/miniconda3 AS build

ENV PYTHONDONTWRITEBYTECODE=true

# Install the package as normal:
COPY environment.yml .
RUN conda env create -f environment.yml

# Install conda-pack:
RUN conda install --freeze-installed -c conda-forge conda-pack

# Use conda-pack to create a standalone environment
# in /venv:
RUN conda-pack -n oemof_api -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# Clean conda and remove unnecessary files
RUN \
  conda clean -afy \
  && find /opt/conda/ -follow -type f -name '*.a' -delete \
  && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
  && find /opt/conda/ -follow -type f -name '*.js.map' -delete

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack

# The runtime-stage image; we can use Debian as the
# base image since the Conda env also includes Python
# for us.
FROM debian:buster-slim AS runtime

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  && apt-get install -y git \
  # Remove unnecessary apt files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system api_user \
    && adduser --system --ingroup api_user api_user

# Copy /venv from the previous stage:
COPY --from=build /venv /venv

# install requirements
WORKDIR /tmp
SHELL ["/bin/bash", "-c"]
COPY ./pyproject.toml ./poetry.lock ./
RUN source /venv/bin/activate && python -m pip install --upgrade pip && pip install --no-cache-dir poetry && poetry install --no-root

ENV BASH_ENV "/home/api_user/.bashrc"
RUN echo "source /venv/bin/activate" > /home/api_user/.bashrc

COPY ./fastapi_app /fastapi_app
RUN chown -R api_user /fastapi_app

USER api_user

WORKDIR /fastapi_app

EXPOSE 5001

ENTRYPOINT ["/entrypoint"]

# run the app server, the last argument match the app variable in the webapp.py file
CMD ["uvicorn", "webapp:app", "--host", "0.0.0.0", "--port", "5001"]
