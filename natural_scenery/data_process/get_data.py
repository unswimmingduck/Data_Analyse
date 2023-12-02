import os
import time
import json
import random
import requests
import csv
from fake_useragent import UserAgent



def get_city_scenic(city, page, writer:csv.DictWriter):
    ua = UserAgent(verify_ssl=False)
    headers = {'User-Agent': ua.random}
    url = f'https://piao.qunar.com/ticket/list.json?keyword={city}&region=&from=mpl_search_suggest&sort=pp&page={page}'
    result = requests.get(url, headers=headers, timeout=10)
    result.raise_for_status()
    return  get_scenic_info(city, result.text, writer)


def get_scenic_info(city, response:json, writer:csv.DictWriter):
    response_info = json.loads(response, strict = False)
    sight_list = response_info['data']['sightList']
    l = []
    for sight in sight_list:
        result_list = {}
        name = sight['sightName'] # 景点名称
        star = sight.get('star', None) # 星级
        score = sight.get('score', 0) # 评分
        price = sight.get('qunarPrice', 0) # 价格
        sale = sight.get('saleCount', 0) # 销量
        districts = sight.get('districts', None) # 省，市，区
        point = sight.get('point', None) # 坐标
        intro = sight.get('intro', None) # 简介
        free = sight.get('free', True) # 是否免费
        address = sight.get('address', None) # 具体地址
        result_list = {'景点名称':name, '星级':star, '评分':score, 
                       '价格':price, '销量':sale, '省，市，区':districts,
                       '坐标':point,  '简介':intro,
                       '是否免费':free, '具体地址':address}
        l.append(result_list)
    writer.writerows(l)
        




def main():
    with open('FJ_ALLSights.csv','a',newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f,fieldnames=['景点名称', '星级', '评分', 
                                              '价格', '销量', '省，市，区',
                                              '坐标',  '简介',
                                              '是否免费', '具体地址'])
        writer.writeheader()
        for page in range(136):
            get_city_scenic("福建", page+1, writer)


if __name__ == "__main__":
    main()