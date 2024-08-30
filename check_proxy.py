from queue import Queue
import threading 
import requests

FILENAME = "proxy_list.txt"
THREADS = 10

q = Queue()
valid_proxies = list()

with open(FILENAME, "r") as file:
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

            res = requests.get("http://ipinfo.io/json", proxies={
                "http": proxy,
                "https": proxy
            })

        except:

            continue

        if res.status_code == 200:

            valid_proxies.append(proxy)

    print("Thread", i, "is done.")
    q.put(None)

threads = list()
for i in range(THREADS):
    thread = threading.Thread(target=check_proxy, args=(i, ))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(valid_proxies)
