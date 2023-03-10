import requests
import random
import time
import os

website_ip = os.getenv('WEBSITE_IP', default="localhost")

endpoints_status = [
    "/code-2xx",
    "/code-4xx",
    "/code-5xx"
]

endpoints_delay = [
    "/ms-200",
    "/ms-500",
    "/ms-1000"
]

while True:
    num = random.randrange(0, 100)

    try:
        if num < 60:
            print(requests.get( f"http://{website_ip}:8000{endpoints_status[0]}"))  # 60% code 2xx
            print(requests.get( f"http://{website_ip}:8000{endpoints_delay[0]}"))
        elif 60 <= num < 80:
            print(requests.get( f"http://{website_ip}:8000{endpoints_status[1]}"))  # 20% code 4xx
            print(requests.get( f"http://{website_ip}:8000{endpoints_delay[1]}"))
        elif 80 <= num <= 100:
            print(requests.get( f"http://{website_ip}:8000{endpoints_status[2]}"))  # 20% code 500 
            print(requests.get( f"http://{website_ip}:8000{endpoints_delay[2]}"))

    except Exception as error:
        print(error)
        print("sleep 5 seconds...") 
        time.sleep(5)

    time.sleep(0.1)