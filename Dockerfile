# Stage 1 - Build token exchange environment
FROM python:3.8-slim-buster AS token-exchange-build

WORKDIR /app

RUN pip install pip -U
COPY . /app
RUN pip install .


# Stage 2 - Build the production image with the token exchange
FROM openformulieren/open-forms:latest AS production-build

WORKDIR /app

# Copy the dependencies of the token_exchange
COPY --from=token-exchange-build /usr/local/lib/python3.8 /usr/local/lib/python3.8

# Add token_exchange code to the image
COPY --chown=maykin:root ./token_exchange /app/src/token_exchange

USER maykin
