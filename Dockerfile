# Stage 1 - Build token exchange environment
FROM python:3.12-slim-bookworm AS token-exchange-build

WORKDIR /app

# Use uv to install dependencies
RUN pip install uv -U
COPY . /app
RUN uv pip install --system .


# Stage 2 - Build the production image with the token exchange
FROM openformulieren/open-forms:latest AS production-build

WORKDIR /app

# Copy the dependencies of the token_exchange
COPY --from=token-exchange-build /usr/local/lib/python3.12 /usr/local/lib/python3.12

# Add token_exchange code to the image
COPY --chown=maykin:root ./token_exchange /app/src/token_exchange

USER maykin
