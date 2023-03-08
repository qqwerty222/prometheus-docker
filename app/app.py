from prometheus_client import start_http_server, Summary
from prometheus_client import Counter
import random
import time

# Status code counter metric
HTTP_REQUESTS   = Counter('http_requests', 'Status codes returned by request', ['status'] )

def code2xx():
    HTTP_REQUESTS.labels(status='200').inc(1)
    # HTTP_REQUESTS.inc(1)

def code4xx():
    HTTP_REQUESTS.labels(status='400').inc(1)
    # HTTP_REQUESTS.inc(1)

def code5xx():
    HTTP_REQUESTS.labels(status='500').inc(1)
    # HTTP_REQUESTS.inc(1)

def status_code_generator():
    num = random.randrange(0, 100)

    if num < 60:            # 60% code 200
        code2xx()
    elif 60 >= num < 80:    # 20% code 400
        code4xx()
    elif num >= 80:         # 20% code 500
        code5xx()

    time.sleep(1)

# Request time metric
REQUEST_TIME = Summary('http_request_processing_time', 'Time spent processing request in seconds')

@REQUEST_TIME.time()
def process_time(t):
    time.sleep(t)

def process_time_generator():
    num = random.randrange(0, 100)

    if num < 60:
        process_time(random.uniform(0, 0.2))    # 60% responce time less than 200ms
    elif 60 >= num < 80:
        process_time(random.uniform(0.2, 0.5))  # 20% responce time from 200ms to 500ms
    elif num >= 80:
        process_time(random.uniform(0.5, 1))    # 20% responce time from 500ms to 1s
    
    time.sleep(1)


if __name__ == '__main__':
    # start up server to expose metrics
    start_http_server(8000)

    # Generate some requests.
    while True:
        status_code_generator()
        process_time_generator()

        

