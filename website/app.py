from flask import Response, Flask
import prometheus_client 
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge

import random
import time

app = Flask(__name__)

# infinitive value
_INF = float("inf")

# Define metrics to send to /metrics
metrics = {}
metrics['request']                  = Counter('http_request', 'Total number of requests', ['endpoint', 'status'])
metrics['request_latency_bucket']   = Histogram('http_request_duration_seconds', 'Histogram for the duration in seconds', ['endpoint', 'status'], buckets=(0.1, 0.2, 0.25, 0.5, 1, _INF))

metrics['request_inflight_max']     = Gauge('http_request_inflight_max', 'Gauge for max count of request that can be operated')
metrics['request_inflight_max'].set(10)

# Page that return one of 2xx status codes
@app.route("/code-2xx")
def code2xx():

    # randomly generate status 2xx response
    index = random.randint(0, 5)
    codes = [ 200, 202, 203, 204, 205, 206 ] 
    metrics['request'].labels(endpoint='/code-2xx', status=f'{codes[index]}').inc()

    return Response(status=codes[index])

@app.route("/code-4xx")
def code4xx():

    # randomly generate status 4xx response
    index = random.randint(0, 2)
    codes = [ 400, 401, 404 ] 
    metrics['request'].labels(endpoint='/code-4xx', status=f'{codes[index]}').inc()

    return Response(status=codes[index])

@app.route("/code-5xx")
def code5xx():

    # randomly generate status 5xx response
    index = random.randint(0, 2)
    codes = [ 500, 501, 503 ] 
    metrics['request'].labels(endpoint='/code-5xx', status=f'{codes[index]}').inc()

    return Response(status=codes[index])

# Make endpoints to simulate latency
@app.route("/ms-200")
def ms200():

    metrics['request'].labels(endpoint='/ms-200', status=200).inc()
    
    start = time.time()
    time.sleep(random.uniform(0, 0.2))
    end = time.time()

    metrics['request_latency_bucket'].labels(endpoint='/ms-200', status=200).observe(end - start)

    return Response(status=200)

@app.route("/ms-500")
def ms500():

    metrics['request'].labels(endpoint='/ms-500', status=200).inc()
    
    start = time.time()
    time.sleep(random.uniform(0.2, 0.5))
    end = time.time()

    metrics['request_latency_bucket'].labels(endpoint='/ms-500', status=200).observe(end - start)

    return Response(status=200)

@app.route("/ms-1000")
def ms1000():

    metrics['request'].labels(endpoint='/ms-1000', status=200).inc()
    
    start = time.time()
    time.sleep(random.uniform(0.5, 1))
    end = time.time()

    metrics['request_latency_bucket'].labels(endpoint='/ms-1000', status=200).observe(end - start)

    return Response(status=200)

# Collect metrics and their values 
@app.route("/metrics")
def requests_count():
    metrics['request'].labels(endpoint='/metrics', status=200).inc()
    res = []
    for key, value in metrics.items():
        res.append(prometheus_client.generate_latest(value))

    return Response(res, mimetype="text/plain")