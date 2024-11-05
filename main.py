from util import generate_headers, generate_proxies
import crawlers.article_page as article
import crawlers.author_page as author
from queue import Queue

headers = generate_headers()
proxies = generate_proxies()

users = ["Kv9AbjMAAAAJ"]

THREADS = 6

if __name__ == "__main__":

    q = Queue()

    for user in users:
        
        data = author.scrape(user, headers, proxies)
        
        for citation_for_view in data:
            q.put([user, citation_for_view])

    q.put(None)

    article.scrape(q, headers, proxies)

