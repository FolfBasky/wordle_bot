import requests
import db

def fetch_words(url):
    words = set()
    response = session.get(url)
    words = response.text.strip().replace('"','').replace(']','').replace('\ufeff[','').split(',')
    return words

def main():
    url = "https://wordleplay.com/dic/ru/len5.json?v=1.2.1"
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
