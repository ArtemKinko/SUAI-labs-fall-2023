# Вариант №8
import io
import math
import string
from functools import reduce
import operator

spam_table = dict()


def create_spam_table(path):
    with io.open(path, encoding='utf-8') as file:
        for line in file:
            line = line.split(',', 1)
            spam_class = line[0]
            message = [word.lower().strip(string.punctuation) for word in line[1].rsplit()]
            print(message)
            for word in message:
                if word == '':
                    continue
                else:
                    if word not in spam_table.keys():
                        if spam_class == '"ham"':
                            spam_table.update({word: [0, 1]})
                        else:
                            spam_table.update({word: [1, 0]})
                    else:
                        spam_num, ham_num = spam_table.get(word)[0], spam_table.get(word)[1]
                        if spam_class == '"ham"':
                            spam_table.update({word: [spam_num, ham_num + 1]})
                        else:
                            spam_table.update({word: [spam_num + 1, ham_num]})
        print(spam_table)
        all_words = 0
        spam_words = 0
        ham_words = 0
        for key in spam_table.keys():
            all_words += 1
            if spam_table.get(key)[0] > 0:
                spam_words += 1
            if spam_table.get(key)[1] > 0:
                ham_words += 1
        print("all words:", all_words)
        print("spam words:", spam_words)
        print("ham words:", ham_words)
        return all_words, spam_words, ham_words


def check_spam(message, all_words, spam_words, ham_words, alpha):
    words = message.split(' ')
    words = [word.lower().strip(string.punctuation) for word in words]
    probabilities_spam = []
    probabilities_ham = []
    print(words)

    for word in words:
        if word in spam_table.keys():
            probabilities_spam.append(math.log(spam_table.get(word)[0] + alpha / (alpha * all_words + spam_words)))
            probabilities_ham.append(math.log(spam_table.get(word)[1] + alpha / (alpha * all_words + ham_words)))
        else:
            probabilities_spam.append(alpha / (alpha * all_words + spam_words))
            probabilities_ham.append(alpha / (alpha * all_words + ham_words))

    print("Оценка категории 'спам':", sum(probabilities_spam))
    print("Оценка категории 'не спам':", sum(probabilities_ham))
    if sum(probabilities_spam) > sum(probabilities_ham):
        print("Сообщение '", message, "' спам!\n")
    else:
        print("Сообщение '", message, "' не спам!\n")


all_words, spam_words, ham_words = create_spam_table("spam-data.csv")
# check_spam("Магазине гора яблок. Купи семь килограмм шоколадку", all_words, spam_words, ham_words, 1)
check_spam("Thanks for your subscription to mobile app", all_words, spam_words, ham_words, 2)
check_spam("You are winner! You won 1000 cash prize", all_words, spam_words, ham_words, 2)
check_spam("Hey, honey, don't forget to buy milk!", all_words, spam_words, ham_words, 2)
check_spam("23423 2dfs sf23r df 23!", all_words, spam_words, ham_words, 2)
check_spam("abc dbhd pbdcv oqiewdf iijdcoqwd oqihwdok[ nsoihjdo hjodj", all_words, spam_words, ham_words, 2)
