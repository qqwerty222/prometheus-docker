import requests
import random
import time
import os

website_ip = os.getenv('WEBSITE_IP', default="localhost")

endpoints = [
    "/code-2xx",
    "/code-4xx",
    "/code-5xx"
]

# if __name__ == '__main__':

while True:
    num = random.randrange(0, 100)

    try:
        if num < 60:
            print(requests.get( f"http://{website_ip}:8000{endpoints[0]}"))  # 60% code 2xx
        elif 60 <= num < 80:
            print(requests.get( f"http://{website_ip}:8000{endpoints[1]}"))  # 20% code 4xx
        elif 80 <= num <= 100:
            print(requests.get( f"http://{website_ip}:8000{endpoints[2]}"))  # 20% code 500 

    except Exception as error:
        print(error)
        print("sleep 5 seconds...") 
        time.sleep(5)

    time.sleep(0.1)