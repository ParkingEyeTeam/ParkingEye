# The build-stage image:
FROM continuumio/miniconda3 AS build

RUN apt-get update && apt-get install -y build-essential

COPY ./server/environment.yml ./environment.yml
RUN ["conda", "env", "create", "-f", "environment.yml"]

# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n parking_eye -o /tmp/env.tar && \
	mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
	rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack

# The runtime-stage image; we can use Debian as the
# base image since the Conda env also includes Python
# for us.

FROM debian:buster AS runtime

# Copy /venv from the previous stage:
COPY --from=build /venv /venv

RUN apt-get update && apt-get install libgl1 -y

WORKDIR /app

COPY . ./

# When image is run, run the code with the environment
# activated:

COPY ./docker/start.sh /scripts/start.sh
ENTRYPOINT ["/bin/bash", "/scripts/start.sh"]
