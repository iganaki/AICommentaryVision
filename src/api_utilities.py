import datetime
from itertools import count
import os
import random
import requests
from dotenv import load_dotenv
import log

load_dotenv()

# 環境変数からAPIキーを取得
random_news_api_key = os.environ['NEWS_API_KEY']
random_word_api_key = os.environ['RANDOM_WORD_API_KEY']

# ニュースAPIからニュースを取得
def fetch_random_news():
    try:
        country = fetch_random_country()
        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey=" + random_news_api_key
        response = requests.get(url)
        if response.status_code == 200:
            news_data = response.json()
            titles = [article['title'] for article in news_data['articles']]
            return titles
        else:
            log.handle_api_error(response.status_code, "ニュースAPIからニュースを取得中にエラーが発生しました", status_code=response.status_code)
            raise Exception("異常なステータス")
    except Exception as e:
        log.handle_api_error(e, "ニュースAPIからニュースを取得中にエラーが発生しました", country=country)
        raise Exception("例外")

# ランダムな国名を取得
def fetch_random_country():
    countrys = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 'eg', 'fr',
                'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my',
                'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th',
                'tr', 'tw', 'ua', 'us', 've', 'za']
    
    return random.choice(countrys)

# API Ninjasからランダムな単語を取得
def fetch_random_word():
    try:
        url = "https://api.api-ninjas.com/v1/randomword"
        headers = {'X-Api-Key': random_word_api_key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            word_data = response.json()
            return word_data['word']
        else:
            error_data = response.json()
            log.handle_api_error(response.status_code, "API Ninjasからランダムな単語を取得中にエラーが発生しました", status_code=response.status_code, error_data=error_data["error"])
            raise Exception("異常なステータス")
    except Exception as e:
        log.handle_api_error(e, "API Ninjasからランダムな単語を取得中にエラーが発生しました")
        raise Exception("例外")

def fetch_random_wiki_word():
    S = requests.Session()

    URL = "https://ja.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnlimit": "5",
        "rnnamespace": "0",
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    RANDOMS = DATA["query"]["random"]
    titles = [random["title"] for random in RANDOMS]

    return titles
