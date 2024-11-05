from bs4 import BeautifulSoup
from datetime import datetime
import threading 
import requests

URL = "https://scholar.google.com/citations"

# Field Helper Functions

def f_authors(text):
    return text.split(", ")

def f_publication_date(text):
    
    formats = ["%Y/%m/%d", "%Y/%m"]
    
    for format in formats:
        
        try:
            
            return datetime.strptime(text, format)
        
        except Exception as e:
            
            # print(e)
            pass

FIELD_NAMES = { 
    "Authors": f_authors,
    "Publication date": f_publication_date, 
    "Publisher": None, 
    "Description": None, 
}

TIMEOUT = 5
THREADS = 6

mutex = threading.Lock()

q = None

headers = None
proxies = None

articles = list()

# Crawler

def load_html(html):
    
    soup = BeautifulSoup(html, "html.parser")
    return soup

def parse_html(soup):

    article = dict()

    article_title_and_url = soup.select_one("a.gsc_oci_title_link")
    
    article_title = article_title_and_url.text
    article_url = article_title_and_url.get("href")

    article["Title"] = article_title
    article["Link"] = article_url

    fields = soup.select("div.gs_scl")
    for field in fields:

        field_name = field.select_one("div.gsc_oci_field").text

        if field_name in FIELD_NAMES:

            field_value = field.select_one("div.gsc_oci_value").text
            
            if FIELD_NAMES[field_name] is not None:
                article[field_name] = FIELD_NAMES[field_name](field_value)
            else:
                article[field_name] = field_value

    return article

def scrape_articles():

    global q

    global headers
    global proxies

    while True:

        data = q.get()

        if data is None:
            break

        user, citation_for_view = data

        params = {
            "view_op": "view_citation",
            "hl": "en",
            "user": user,
            "citation_for_view": citation_for_view
        }

        while True:

            try:

                with mutex:
                
                    headers_ = next(headers)
                    proxies_ = next(proxies)

                response = requests.get(URL, params=params, headers=headers_, proxies=proxies_, timeout=TIMEOUT)
                
                soup = load_html(response.text)
                article = parse_html(soup)

                with mutex:
                    articles.append(article)

                break

            except Exception as e:

                # print(e)
                pass
    
    q.put(None)

def scrape(q_, headers_, proxies_):

    global q

    global headers
    global proxies
    
    q = q_ 

    headers = headers_
    proxies = proxies_

    threads = list()
    for i in range(THREADS):
        thread = threading.Thread(target=scrape_articles)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    for article in articles:
        print(article)
    