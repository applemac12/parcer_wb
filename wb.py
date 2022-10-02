import lxml
import requests
from bs4 import BeautifulSoup
import json
import os

with open('data_wb/main-menu-ru-ru.json', 'r+', encoding='utf-8') as file:
    list_main = json.load(file)
# with open("wb_dict", 'a', encoding='utf-8') as file:
#    json.dump(dict_main, file, indent=4, ensure_ascii=False)

headeras = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 Mobile Safari/537.36'
}
list_url_categoty = []
list_shard_categoty = []
list_query_categoty = []
results_name_category = []
results = []
list_errors = []
error = 0
dict_name_category = []


# Преобразует список словарей в словарь(берет первый)
def list_in_dict(list_main, list_name):
    i = 0
    while i < len(list_main):
        dict_main = list_main[i]
        search_childs(dict_main, list_name)
        i += 1

# Ищет в словаре ключ "childs", если его нет, то берет ссылку, а если есть то, отпускается туда и вызывает преобразование
#Также составляет все нужные списки дляформирования результата.
def search_childs(dict, list_name):
    if "childs" in dict:
        list_name = list_name + dict['name'] + '/'
        new_list = dict['childs']
        list_in_dict(new_list, list_name)
    else:
        try:
            global list_url_categoty, list_shard_categoty, list_query_categoty, dict_name_category
            list_name = list_name + dict['name'] + '/'
            shard = dict['shard']
            url = dict['url']
            query = dict['query']
            dict_name_category.append(list_name)
            list_url_categoty.append(url)
            list_shard_categoty.append(shard)
            list_query_categoty.append(query)
            list_name = ''
        except Exception as ex:
            dict_name_category.append('')
            list_shard_categoty.append('')
            list_query_categoty.append('')
            list_url_categoty.append('')
            list_name = ''

def search_on_page(shard, query, links, condition_low, condition_high, dict_name_category):
    l = len(shard) - 1
    count = 0
    for s in range(1, l):
        try:
            url = f"https://catalog.wb.ru/catalog/{shard[s]}/v4/filters?appType=1&couponsGeo=2,12,7,3,6,21,16&curr=rub&dest=-1221148,-140294,-1751445,-364763&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&reg=0&regions=64,58,83,4,38,80,33,70,82,86,30,69,22,66,31,40,1,48&spp=0&{query[s]}"
            req = requests.get(url, headers=headeras)
            with open('data_wb/filters.json', 'wb') as f:
                f.write(req.content)
            with open('data_wb/filters.json', 'r+', encoding='utf-8') as file:
                data = json.load(file)
            data = data['data']
            filteres = data['filters']
            filteres_dict = filteres[0]
            items = (filteres_dict['items'])
            i = True
            j = 0
        except Exception as ex:
            print(ex)
        while i == True:
            try:
                element_list = items[j]
                if (element_list['count'] <= condition_high and element_list['count'] >= condition_low):
                    results_name_category = element_list['name']
                    results_count_category = element_list['count']
                    results.append(
                        {
                            "Категория": dict_name_category[s],
                            "Название подраздела": results_name_category,
                            "Карточек товара в подразделе": results_count_category,
                            "Ccылка на категорию": "https://www.wildberries.ru" + links[s]
                        }
                    )
                    count += 1
                    print(f'Найдено {count} потенциальных ниш в дипазоне от {condition_low} до {condition_high}')
                j += 1
            except Exception as ex:
                i = False
    os.remove('data_wb/filters.json')

    with open(f"data_wb/category_results12_{condition_low}_{condition_high}", 'a', encoding='utf-8') as file:
        json.dump(results, file, indent=4, ensure_ascii=False)



condition_high = 400
condition_low = 50


list_in_dict(list_main, list_name='')
search_on_page(list_shard_categoty, list_query_categoty, list_url_categoty, condition_low, condition_high, dict_name_category)
