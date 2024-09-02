import requests

FILENAME = "valid_proxy_list.txt"

with open(FILENAME, "r") as file:
    proxies = file.read().split("\n")[:-1]

sites_to_check = ["https://www.amazon.com/?tag=amazusnavi-20&hvadid=675149237887&hvpos=&hvnetw=g&hvrand=16573818752733055329&hvpone=&hvptwo=&hvqmt=e&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9022196&hvtargid=kwd-10573980&ref=pd_sl_7j18redljs_e&hydadcr=28883_14649097&gad_source=1"]

counter = 0
for site in sites_to_check:

    flag = True

    while flag and len(proxies):

        try:
            
            res = requests.get(site, 
                            proxies={
                                    "http": "101.255.134.100:8080",
                                    "https": "101.255.134.100:8080"
                                },
                                timeout=5
                    )
            
            print(res.status_code)

            exit()

            if res.status_code == 200:
                flag = False
            
            counter += 1
        
        except:

            print(res.status_code)

            exit()

            print("failed")

            proxies.pop(counter)    

print(proxies)       
