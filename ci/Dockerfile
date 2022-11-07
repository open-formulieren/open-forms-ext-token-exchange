# Stage 1 - Build Token exchange extension environment
FROM python:3.8-slim-buster AS token-exchange-build-test

WORKDIR /app

RUN pip install pip -U
COPY . /app
RUN pip install -e .


# Stage 2 - Build the production image with the demo extension
FROM openformulieren/open-forms:test AS test-build

WORKDIR /app

COPY ./bin/docker_test.sh /test.sh

# Copy the dependencies of the demo-extension
COPY --from=token-exchange-build-test /usr/local/lib/python3.8 /usr/local/lib/python3.8

# Add demo_extension code to the image
COPY --chown=maykin:root ./token_exchange /app/src/token_exchange

USER maykin
