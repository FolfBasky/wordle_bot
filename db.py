import sqlite3

# Функция для создания таблицы, если её не существует
def create_table():
    try:
        conn = sqlite3.connect('words.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS words
                     (word TEXT PRIMARY KEY,
                     usage_count INTEGER,
                     encountered BOOLEAN)''')
        conn.commit()
    except sqlite3.Error as e:
        print("Ошибка при создании таблицы:", e)
    finally:
        conn.close()

# Функция для добавления результата в базу данных
def add_word(word, usage_count, encountered):
    try:
        conn = sqlite3.connect('words.db')
        c = conn.cursor()
        c.execute('''INSERT INTO words (word, usage_count, encountered)
                     VALUES (?, ?, ?)''', (word, usage_count, encountered))
        conn.commit()
    except sqlite3.Error as e:
        print("Ошибка при добавлении слова:", e)
    finally:
        conn.close()

# Функция для извлечения всех результатов из базы данных, отсортированных по частоте использования и алфавиту
def get_words_sorted():
    try:
        conn = sqlite3.connect('words.db')
        c = conn.cursor()
        c.execute("SELECT * FROM words ORDER BY encountered DESC, usage_count DESC")
        rows = c.fetchall()
        return rows
    except sqlite3.Error as e:
        print("Ошибка при получении слов:", e)
    finally:
        conn.close()

# Функция для увеличения количества использований слова
def increment_usage_count(word, increment_by=1):
    try:
        conn = sqlite3.connect('words.db')
        c = conn.cursor()
        c.execute('''UPDATE words
                     SET usage_count = usage_count + ?
                     WHERE word = ?''', (increment_by, word))
        conn.commit()
    except sqlite3.Error as e:
        print("Ошибка при увеличении количества использований слова:", e)
    finally:
        conn.close()

# Функция для установки encountered в True, если слово уже существует
def update_encountered(word):
    try:
        conn = sqlite3.connect('words.db')
        c = conn.cursor()
        c.execute('''UPDATE words
                     SET encountered = 1
                     WHERE word = ?''', (word,))
        conn.commit()
    except sqlite3.Error as e:
        print("Ошибка при обновлении encountered:", e)
    finally:
        conn.close()

# Функция для удаления слова из базы данных
def delete_word(word):
    try:
        conn = sqlite3.connect('words.db')
        c = conn.cursor()
        c.execute("DELETE FROM words WHERE word=?", (word,))
        conn.commit()
    except sqlite3.Error as e:
        print("Ошибка при удалении слова:", e)
    finally:
        conn.close()

# Пример использования функций
if __name__ == "__main__":
    create_table()
    print(get_words_sorted())
