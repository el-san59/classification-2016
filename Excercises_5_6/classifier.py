from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import RussianStemmer
from stop_words import get_stop_words


tokenizer = RegexpTokenizer(r'[а-я]+')
stop_words = get_stop_words('ru')
stemmer = RussianStemmer()


def parse(text):
    line = text.strip().lower()
    raw_tokens = tokenizer.tokenize(line)
    stopped_tokens = [i for i in raw_tokens if (not i in stop_words) and (len(i) > 2)]
    stemmed_tokens = [stemmer.stem(i) for i in stopped_tokens]
    return ' '.join(stemmed_tokens)


def get_tag(text, model, tfidf):
    tokens = parse(text)
    mat = tfidf.transform([tokens])
    res = model.predict(mat)
    return res


# if __name__ == "__main__":
#     text = "Пресс-секретарь президента России Дмитрий Песков не уточнил, разъяснил ли президент Турции Реджеп Тайип " \
#            "Эрдоган свою позицию в телефонном разговоре с Владимиром Путиным относительно высказывания о свержении " \
#            "президента Сирии Башара Асада, передает РИА «Новости».\n«Состоялся широкий обмен мнениями», — сказал " \
#            "Песков.\nРанее Реджеп Тайип Эрдоган заявил, что турецкая армия вошла на сирийскую территорию, чтобы " \
#            "«положить конец правлению жестокого тирана» — сирийского президента Башара Асада.\nПозже Дмитрий Песков " \
#            "прокомментировал высказывание турецкого президента, отметив, что для Кремля это заявление стало новостью. " \
#            "Кроме того, он добавил, что оно диссонирует с предыдущим заявлением Эрдогана и с общим пониманием ситуации." \
#            "\nВ администрации президента Турции в свою очередь уточнили, что слова Эрдогана о намерении свергнуть Асада " \
#            "не следует понимать буквально."
#
#     print(get_tag(text))