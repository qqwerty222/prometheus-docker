from flask import Response, Flask, request
import prometheus_client 
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge

import random
import time

app = Flask(__name__)

_INF = float("inf")

metrics = {}
metrics['http_requests']  = Counter('http_requests', 'Total number of requests', ['status'])
metrics['request_latency'] = Histogram('http_request_duration_seconds', 'Histogram for the duration in seconds', buckets=(0.1, 0.2, 0.25, 0.5, 1, _INF))

@app.route("/code-2xx")
def code2xx():

    # randomly generate status 2xx response
    index = random.randint(0, 5)
    codes = [ 200, 202, 203, 204, 205, 206 ] 
    metrics['http_requests'].labels(status=f'{codes[index]}').inc()

    # simulate request process delay
    start = time.time()
    delay()
    end = time.time()

    metrics['request_latency'].observe(end - start)

    return Response(status=codes[index])

@app.route("/code-4xx")
def code4xx():

    # randomly generate status 4xx response
    index = random.randint(0, 20)
    codes = [ 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 428, 429, 431 ] 
    metrics['http_requests'].labels(status=f'{codes[index]}').inc()

    # simulate request process delay
    start = time.time()
    delay()
    end = time.time()

    metrics['request_latency'].observe(end - start)

    return Response(status=codes[index])

@app.route("/code-5xx")
def code5xx():

    # randomly generate status 5xx response
    index = random.randint(0, 6)
    codes = [ 500, 501, 502, 503, 504, 505, 511 ] 
    metrics['http_requests'].labels(status=f'{codes[index]}').inc()

    # simulate request process delay
    start = time.time()
    delay()
    end = time.time()
    metrics['request_latency'].observe(end - start)

    return Response(status=codes[index])

def delay():
    num = random.randrange(0, 100)

    if num <= 5:                                
        delay = random.uniform(0, 0.1)            # 5%  delay below  100ms
    elif 5 < num <= 20:                         
        delay = random.uniform(0.1, 0.2)          # 15% delay below  200ms 
    elif 20 < num <= 60:                       
        delay = random.uniform(0.2, 0.25)         # 40% delay below  250ms
    elif 60 < num <= 85:                        
        delay = random.uniform(0.25, 0.5)         # 25% delay below  500ms
    elif 85 < num <= 95:                        
        delay = random.uniform(0.5, 1)            # 10% delay below  1000ms
    elif num > 95:                              
        delay = random.uniform(1, 1.25)           # 5%  delay above  1250ms
        
    print(f"#------------------------------------------------------------------------------ # {num} - {delay}")
   
    time.sleep(delay)
    return None

@app.route("/metrics")
def requests_count():
    res = []
    for key, value in metrics.items():
        res.append(prometheus_client.generate_latest(value))

    return Response(res, mimetype="text/plain")