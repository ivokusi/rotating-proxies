import random

# Headers

def generate_random_user_agent():
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:116.0) Gecko/20100101 Firefox/116.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0',
    ]

    return random.choice(user_agents)

def generate_random_accept_language():
    
    languages = ['en-US', 'en-GB', 'fr-FR', 'de-DE', 'es-ES', 'it-IT', 'ja-JP', 'zh-CN', 'ru-RU', 'pt-BR']
    language_weights = [1.0, 0.9, 0.8, 0.7, 0.6]
    selected_languages = random.sample(languages, k=random.randint(1, 3))
    return ','.join([f"{lang};q={random.choice(language_weights)}" for lang in selected_languages])
    
def generate_random_accept_encoding():
   
    encodings = ['gzip', 'deflate', 'br', 'identity']
    selected_encodings = random.sample(encodings, k=random.randint(1, 3))
    return', '.join(selected_encodings)

def generate_random_connection():
    
    connections = ['keep-alive', 'close', 'upgrade']
    return random.choice(connections)

def generate_headers():

    while True:
        yield {
            'User-Agent': generate_random_user_agent(),
            'Accept-Language': generate_random_accept_language(),
            'Accept-Encoding': generate_random_accept_encoding(),
            'Connection': generate_random_connection()
        }

# Proxy

VALID_PROXIES = "proxy_list/valid_proxy_list.txt"

def generate_proxies():

    with open(VALID_PROXIES, "r") as file:
        proxies = file.read().split("\n")[:-1]
    
    while True:
        for proxy in proxies:
            yield {
                "http": proxy,
                "https": proxy
            }