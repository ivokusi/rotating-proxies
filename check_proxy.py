from queue import Queue
import threading 
import requests

INPUT = "proxy_list.txt"
OUTPUT = "valid_proxy_list.txt"
SITE_TO_TEST = "https://scholar.google.com/citations?user=Kv9AbjMAAAAJ&hl=en&oi=sra"
THREADS = 6

CWHITE  = '\33[37m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'

q = Queue()
valid_proxies = list()

with open(INPUT, "r") as file:
    proxies = file.read().split("\n")
    for proxy in proxies[:-1]:
        q.put(proxy)

q.put(None)

def check_proxy(i):

    global q

    while True:

        proxy = q.get()

        if proxy is None:
            break
        
        try:

            res = requests.get(SITE_TO_TEST, 
                               proxies={
                                    "http": proxy,
                                    "https": proxy
                                }, 
                                timeout=5
                            )

        except:
            
            print(f"{CRED}Thread {i} found invalid proxy {proxy}{CWHITE}")
            continue

        if res.status_code == 200:

            print(f"{CGREEN}Thread {i} found valid proxy {proxy}{CWHITE}")
            valid_proxies.append(proxy)

        else:
            
            print(f"{CRED}Thread {i} found invalid proxy {proxy}{CWHITE}")

    print("Thread", i, "is done.")
    q.put(None)

threads = list()
for i in range(THREADS):
    thread = threading.Thread(target=check_proxy, args=(i, ))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

with open(OUTPUT, "w") as file:
    for proxy in valid_proxies:
        file.write(proxy)
        file.write("\n")
