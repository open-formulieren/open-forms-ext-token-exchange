# Stage 1 - Build Token exchange extension environment
FROM python:3.10-slim-buster AS token-exchange-build-test

WORKDIR /app

RUN pip install pip -U
COPY . /app
RUN pip install -e .


# Stage 2 - Build the test image with the token exchange
FROM openformulieren/open-forms:test AS test-build

WORKDIR /app

COPY ./bin/docker_test.sh /test.sh

# Copy the dependencies of the token_exchange
COPY --from=token-exchange-build-test /usr/local/lib/python3.10 /usr/local/lib/python3.10

# Add token_exchange code to the image
COPY --chown=maykin:root ./token_exchange /app/src/token_exchange

USER maykin
