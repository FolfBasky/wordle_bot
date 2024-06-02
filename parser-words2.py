import requests
import db


def fetch_words(url, sp = 301):
    words = set()
    if sp >= 30_000: return set()
    headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
               'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
               'Accept-Encoding':'gzip, deflate, br',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
                'Accept-Language':'ru,en;q=0.9',
                }
    data = {
    "modul": "lists",
    "method": "get_position_page",
    "start": sp,
    "step": 300,
    "id": 3251,
    "mode": 0,
    "alphabet": 1,
    "lang": 0,
    "columns": 3,
    "json_object": 1
    }
    try:
        response = session.get('https://kupidonia.ru/spisok/spisok-suschestvitelnyh-russkogo-jazyka')
        cookies = response.cookies.get_dict()
        response = session.post(url, data=data, headers=headers, cookies=cookies).json()
        for x in range(len(response['reply'])):
            word = response['reply'][str(x)]['title']
            if word in words: return set()
            words.add(word)
    except requests.RequestException as e:
        print("Ошибка при запросе:", e)
    return words|fetch_words(url,sp+300)

def main():
    url = "https://kupidonia.ru/ajax.php"
    words = fetch_words(url)
    print(f"Найдено {len(words)} слов")
    ww = [x[0] for x in db.get_words_sorted()]
    for word in words:
        if word in ww:
            db.increment_usage_count(word)
        else:
            db.add_word(word, 1, False)

if __name__ == '__main__':
    session = requests.Session()
    main()
