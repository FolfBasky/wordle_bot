import db
import re

def main():
    while True:
        words = db.get_words_sorted()
        alp = list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        pattern = r'.{0,}'
        n = int(input('Введите длину слова: '))
        t = int(input('Введите кол-во попыток: '))
        letters_true = set()
        failed_words = set()
        for _ in range(t):
            word = sorted([x for x in words if len(x[0])==n and all(True if i in alp else False for i in x[0]) \
                        and re.match(pattern,x[0]) \
                        and x[0] not in failed_words \
                        and all(True if i in x[0] else False for i in letters_true)], key=lambda x: (n-len(set(x[0])),-int(x[2])))
            if len(word) > 0: word = word[0][0]
            else:
                wv = input('Нет подходящих слов, введите загаданное: ')
                db.add_word(wv,1,1)
                break
            print('Попробуйте: '+word)
            inp = input('Какие буквы в слове оказались? ')
            letters_true |= set(inp)
            if len(inp) == n:
                print(inp.title() + ' - ваше загаданное слово!')
                db.update_encountered(pattern)
                break
            r = input('Введите шаблон правильных букв (ок_а_) или enter, если шаблон не изменился: ')
            if r:
                pattern = r.replace(' ','').replace('_','.')
                if '.' in pattern:
                    failed_words.add(word)
            alp = [x for x in alp if x not in set(word)-set(letters_true)]
        else:
            word = input('Не удалось угадать слово. Введите загаданное: ')
            db.add_word(word,1,1)

if __name__ == '__main__':
    main()
