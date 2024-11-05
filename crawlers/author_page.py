from bs4 import BeautifulSoup
from urllib import parse
import requests

URL = "https://scholar.google.com/citations"

def load_html(html):

    soup = BeautifulSoup(html, "html.parser")
    return soup

def load_rows(soup):

    rows = soup.select("tr.gsc_a_tr")
    data = list()
    
    for row in rows:
        article_data = load_data(row)
        data.append(article_data)
    
    return data

def load_data(row):

    article_data = row.select_one("td.gsc_a_t")

    article_title_and_url = article_data.select_one("a")
    
    # article_title = article_title_and_link.text
    article_url = article_title_and_url.get("href")

    url_params = parse.parse_qs(parse.urlparse(article_url).query)
    
    citation_for_view = url_params["citation_for_view"][0]

    return citation_for_view

    # article_authors = article_data.select_one("div.gs_gray").text.split(", ")

    # print(article_title)
    # print(article_link)
    # print(article_authors)

    # citation_data = row.select_one("td.gsc_a_c")

    # citation_count_and_link = citation_data.select_one("a")

    # citation_count = citation_count_and_link.text
    # citation_link = citation_count_and_link.get("href")

    # print(citation_count)
    # print(citation_link)

    # publication_data = row.select_one("td.gsc_a_y")

    # publication_date = publication_data.select_one("span").text

    # print(publication_date)

def scrape(user, headers, proxies):

    params = {
        "hl": "en",
        "user": user,
        "cstart": "0",
        "pagesize": "12"
    }

    data = {
        "json": "1"
    }

    for header, proxy in zip(headers, proxies):

        try:

            response = requests.post(URL, params=params, data=data, headers=header, proxies=proxy, timeout=5)
            html = response.json().get("B")

            soup = load_html(html)
            data = load_rows(soup) # Will return a list of citation_for_view 

            return data

        except:

            pass