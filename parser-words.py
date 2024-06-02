import aiohttp
import asyncio
from bs4 import BeautifulSoup
import db

letters = ['а']
result = set()
max_tasks = 1

async def fetch_words(session, letter, addung):
    url = f'https://ru.wiktionary.org/w/index.php?title=Категория:Русские_существительные&from={letter}' + (addung or '')
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36'
    }
    async with session.get(url, headers=headers) as response:
        text = await response.text()
        soup = BeautifulSoup(text, 'lxml')
        words_div = soup.find_all('div', class_='mw-category mw-category-columns')
        if not words_div or len(words_div) < 2:
            return [], None
        words = [x.lower() for x in words_div[1].text.split('\n') if '-' not in x and len(x) > 2]
        #print(f"URL: {url} -> Found words: {words[:5]}...")  # Отладочная информация
        new_addung = f'&subcatfrom=а&pagefrom={words[-1]}#mw-pages'
        return words, new_addung

async def worker(session, task_queue):
    global result
    while True:
        letter, addung = await task_queue.get()
        words, new_addung = await fetch_words(session, letter, addung)
        if words:
            unique_words = set(words) - result
            if unique_words:
                result.update(unique_words)
            else: break
        task_queue.task_done()
        if new_addung:
            await task_queue.put((letter, new_addung))
        if len(result) > 160_000: break

async def main():
    global result
    task_queue = asyncio.Queue()
    task_queue.put_nowait((letters[0], ''))

    async with aiohttp.ClientSession() as session:
        workers = [asyncio.create_task(worker(session, task_queue)) for _ in range(max_tasks)]
        await task_queue.join()
        for _ in range(max_tasks):
            await task_queue.put((None, None))
        await asyncio.gather(*workers)

    print(f"Total unique words fetched: {len(result)}")
    try:
        for word in result:
            db.add_word(word,0,False)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    asyncio.run(main())
