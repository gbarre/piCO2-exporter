# piCO2-exporter

Python exporter for SCD30 sensor on Raspberry pi

## Build

```sh
git clone https://github.com/gbarre/piCO2-exporter.git
cd piCOE-exporter/
# sudo apt install docker.io
# sudo usermod -aG docker ${USER}
# logout / login
docker build -t pico2-exporter .
```

## Run

```sh
docker run -d -p9983:9983 --restart=unless-stopped --device /dev/i2c-1 --name pico2-exporter pico2-exporter
# You might need to adapt /dev/i2c-1 port...
```

## Test

```sh
docker logs pico2-exporter
2022-01-11 18:41:58,578 - __main__ - INFO - CO2: 650.04ppm, temp: 23.59°C, rh: 34.89%

curl http://localhost:9983
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 377.0
python_gc_objects_collected_total{generation="1"} 0.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 40.0
python_gc_collections_total{generation="1"} 3.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="8",patchlevel="12",version="3.8.12"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 3.852288e+07
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 1.4790656e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.64192305474e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 2.5900000000000003
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 7.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06
# HELP probe_co2 Show CO2 ppm metric
# TYPE probe_co2 gauge
probe_co2{firmware_version="834"} 650.8117065429688
# HELP probe_temp Show temp metric
# TYPE probe_temp gauge
probe_temp{firmware_version="834"} 23.39246368408203
# HELP probe_humidity Show humidity metric
# TYPE probe_humidity gauge
probe_humidity{firmware_version="834"} 35.06622314453125
```

## Prometheus

```yaml
---
global:
  scrape_interval:     15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: node
    # If prometheus-node-exporter is installed, grab stats about the local
    # machine by default.
    static_configs:
      - targets: ['localhost:9100']

  - job_name: piCO2
    scrape_interval: 3s
    scrape_timeout: 2s
    static_configs:
      - targets: ['localhost:9983']

```

## Grafana

[See here](./grafana.json) for dashboard example.

![grafana dashboard capture](./doc/grafana.png)
