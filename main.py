import db
import re


def main():
    while True:
        words = db.get_words_sorted()
        alp = list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        pattern = r'.{0,}'
        n = int(input('Введите длину слова: '))
        letters_true = set()
        failed_words = []
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
            inp = input('Какие буквы есть в слове? (запишите +, если угадано) ')
            if len(inp) == n or inp == '+':
                if inp != '+':print(inp.title() + ' - ваше загаданное слово!')
                else: print(word.title() + ' - ваше загаданное слово!')
                db.update_encountered(pattern)
                db.increment_usage_count(word)
                break
            if not inp.isalpha() and inp != '':
                print('Некорректно!')
                inp = input('Какие буквы есть в слове? ')
            letters_true |= set(inp)
            r = input('Введите шаблон правильных букв (ок_а_) или enter, если шаблон не изменился: ')
            if len(r) != n and len(r) != 0:
                print('Некорректно!')
                r = input('Введите шаблон правильных букв (ок_а_) или enter, если шаблон не изменился: ')
            if r:
                pattern = r.replace(' ','').replace('_','.')
                if '.' in pattern:
                    failed_words.append(word)
            alp = [x for x in alp if x not in set(word)-set(letters_true)]
        else:
            word = input('Не удалось угадать слово. Введите загаданное: ')
            db.add_word(word,1,1)

if __name__ == '__main__':
    t = int(input('Введите кол-во попыток: '))
    main()
