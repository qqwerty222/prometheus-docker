# Monitor website endpoints with Prometheus and Graphana

There is 3 services in this project:
- traffic_generator, infinitely send requests to website endpoints
- website, receive requests and answer with random delay and status code
- prometheus, collect metrics from website 
- grafana, get and visualize prometheus metrics

## How to deploy

To deploy this project use: 
```bash
docker compose up -d
```

Output:
```bash
[+] Running 5/5
 ✔ Network prometheus-docker_monitoring    Created     0.1s
 ✔ Container exporter                      Started     1.3s
 ✔ Container grafana                       Started     1.3s
 ✔ Container traffic_generator             Started     0.9s
 ✔ Container prometheus                    Started     1.4s
```

After you will see 7 containers
```bash
CONTAINER ID   IMAGE                                CREATED         STATUS         PORTS                                       NAMES
2bbba533fd7d   prometheus-docker-website            7 seconds ago   Up 6 seconds   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   exporter
16b9227e4cd7   prometheus-docker-grafana            7 seconds ago   Up 6 seconds   0.0.0.0:3000->3000/tcp, :::3000->3000/tcp   grafana
9530b5771a68   prometheus-docker-traffic_generator  7 seconds ago   Up 6 seconds                                               traffic_generator
aa26c5f193ba   prom/prometheus:latest               7 seconds ago   Up 6 seconds   0.0.0.0:9090->9090/tcp, :::9090->9090/tcp   prometheus
```

## Project description
  
This project implement 4-golden-signals monitoring. The four golden signals of monitoring are latency, traffic, errors, and saturation.

Latency - time that takes to serve a request. Website have 4 endpoints to simulate latency: /ms-200, /ms-500, /ms-1000  
Traffic - number of requests per second, sended to website  
Errors  - number of errors that occured while serving requests. There is /code-2xx, /code-3xx, /code-5xx endpoints to simulate errors  
Saturation - how much your system is loaded compare to maximum possible load

## Endpoints 

localhost:9090/ - Prometheus  
localhost:3000/ - Grafana

localhost:8000/metrics - Metrics exporter  

Website error endpoints:  
localhost:8000/code-2xx  
localhost:8000/code-4xx  
localhost:8000/code-5xx  

Website delay endpoints:  
localhost:8000/ms-200  
localhost:8000/ms-500  
localhost:8000/ms-1000  