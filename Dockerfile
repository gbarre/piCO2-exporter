FROM python:3.8-slim AS build

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

WORKDIR /uptime

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY collector.py .
COPY piCO2-exporter.py .

FROM python:3.8-slim AS run

RUN set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y; \
    rm -rf /var/lib/apt/lists/*; \
    apt-get clean

WORKDIR /uptime

COPY --from=build /opt/venv /opt/venv
COPY --from=build /uptime .

ENV TZ="Europe/Paris"
ENV PATH="/opt/venv/bin:$PATH"

CMD [ "piCO2-exporter.py" ]
ENTRYPOINT [ "python" ]
