import vk
import requests
import re
import sys


p = re.compile('[a-zа-яёóá0-9- .,?!`\':&/+()"]')
m = re.compile('[a-z]')
with open("token.txt", 'r', encoding="utf-8") as fl:
    token = fl.readline()


def change_the_artist(string):
    new_temp = str()
    for l in string:
        if l == 'ó':
            new_temp += 'o'
        elif l == 'á':
            new_temp += 'a'
        elif l == 'ё' and m.match(new_temp[-1]):
            new_temp += 'e'
        elif l == 'ё' and not m.match(new_temp[-1]):
            new_temp += 'е'
        else:
            new_temp += l
    return new_temp


def fill_the_dict(list_of_dicts):
    result_dict = dict()
    for i in list_of_dicts:
        i = {key: i[key].lower() for key in i if not isinstance(i[key], int)}
        result_dict.setdefault(change_the_artist(i['artist']), []).append(i['title'])
        # result_dict[change_the_artist(i['artist'].lower())] = list()
    # for i in list_of_dicts:
        # result_dict[change_the_artist(i['artist'].lower())].append(i['title'].lower())
    # print(result_dict.keys())
    return result_dict


def remove_unneccessary_symbols(string):
    result = str()
    for i in string:
        if p.match(i):
            result += i
    return result


def correct_all_the_titles(dictionary):
    for i in dictionary:
        for k in range(len(dictionary[i])):  # для каждого названия из списка
            item = dictionary[i][k]
            if len(p.findall(item)) != len(item):
                dictionary[i][k] = remove_unneccessary_symbols(item)


def main():
    try:
        vkapi = vk.API(access_token=token)
    except ValueError:
        print("Нету токена!")
        sys.exit()

    try:
        answ1 = vkapi.audio.get(owner_id=19856589, need_user=0)
        answ2 = vkapi.audio.get(owner_id=17370867, need_user=0) # 13980632
    except requests.exceptions.ConnectionError:
        print("Connection failed")
        sys.exit()
    except requests.exceptions.ReadTimeout:
        print("Read timed out")
        sys.exit()
    except vk.api.VkAuthorizationError:
        print("В токене шняга какая-то")
        sys.exit()
    dictOfMySongs = fill_the_dict(answ1['items'])
    dictOfOthersSongs = fill_the_dict(answ2['items'])

    # создаём пустой словарь. бежим по заполненному словарю. берём ключ, "обрабатываем" (проверяем?), вставляем в пустой
    # значения по взятому ключу, но сам ключ берём "обработанный"
    newDictOfMySongs = dict()
    for i in list(dictOfMySongs.keys()):
        if len(p.findall(i)) == len(i):
            newDictOfMySongs[i] = dictOfMySongs[i]
        else:
            newDictOfMySongs[remove_unneccessary_symbols(i)] = dictOfMySongs[i]
    correct_all_the_titles(newDictOfMySongs)

    newDictOfOthersSongs = dict()
    for i in list(dictOfOthersSongs.keys()):
        if len(p.findall(i)) == len(i):
            newDictOfOthersSongs[i] = dictOfOthersSongs[i]
        else:
            newDictOfOthersSongs[remove_unneccessary_symbols(i)] = dictOfOthersSongs[i]
    correct_all_the_titles(newDictOfOthersSongs)

    # бежим по первому словарю и сравниваем ключи с ключами второго
    matchedArtists = list()
    for i in newDictOfMySongs:
        # print(i, i in newDictOfOthersSongs)
        if i in list(newDictOfOthersSongs.keys()):
            matchedArtists.append(i)

    print(matchedArtists)

if __name__ == '__main__':
    main()