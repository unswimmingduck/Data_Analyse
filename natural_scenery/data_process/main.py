import time

import requests
import pandas as pd
import csv


class Qunar:
    def __init__(self):
        self.url = 'https://piao.qunar.com/ticket/list.json'
        self.key_words = '福建'
        self.session = requests.session()
        self.headers = {
            'Cookie': 'SECKEY_ABVK=tOOPE3+CrSYwl5g06mtmyoFv5ar6WM0jc0BDUHgG6Z4%3D; BMAP_SECKEY=l4bRVErr6QGEKYGbowaMsX7svFyjmjlY3IIFlcTivurK3R-0T5rRXRWYMTRkyWj61tXnHYIfD3IlLDIQnoewYJQch1DvIxVE6OTN4UoImvapbwpJQdcWTypJgikP6PcY0_CW15j94XDifVorb7hHy7XTmxX3zxix2gCrTuYXNk18UZNZAZSSJRoLZDcAnpXx; QN1=000080802eb45158b4281c5c; QN71="MTAxLjk0LjI1MS4xNTY65LiK5rW3OjE="; QN300=link.zhihu.com; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; csrfToken=9kvLDMMP7RPz2gPBymlUKPlfhWr8kxYv; QN269=6A27EB10FE1611ED9CB5FA163ED315CF; _i=ueHd8SP8v3YX4UEX-NZP0cCtN8AX; QN57=16853607747150.6354033031507407; Hm_lvt_15577700f8ecddb1a927813c81166ade=1685360776; fid=3dd2ccd9-4761-43b5-8ae9-72cd285da296; QN205=organic; QN277=organic; QN99=4604; QunarGlobal=10.68.20.162_-751f5d42_18867229119_-3570|1685361043851; QN601=0d6cbf88fbaf3dd96d9c53b549937ca6; ariaDefaultTheme=null; QN48=tc_bddeb958fb458c83_1886758ad03_e291; QN163=0; _vi=G_GCZ1QRX1ORHnTAwTlDMPC9QJwWlYbyfsjflzHTg6IBbjYaueMUdeIJ-MRDOUgzuCtiVfPk0iXGfrnozA1NHEKYg6WxsVvNaWnbwg6AmzaLl2LBe9C8D4hNDCyloYmlUu0KF7_QK9DNAqOMoZHvSRh81bLa0KtIykzDu5wfcs5l; QN63=%E7%A6%8F%E5%BB%BA; QN267=2067279852f1c78a1a; QN58=1685360774713%7C1685363415819%7C15; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1685363416; QN271=3a545c74-a39f-4e29-bff3-d1330211f0c3; JSESSIONID=DF6A6D4802A0ACF104B04782DEF4DE6C; __qt=v1%7CVTJGc2RHVmtYMS9DT3I2UXlDQnA3d1dWTHlWMW56U2xEbEYvK2UzVEhWWTN3MWVJYmszbWVJeS91cHhyQzZZT3V2VWczTTBnN1dnaEtkckJRNGtqWEZsa1Y2RENlTFZENXgxRnZVVGhWSFNhd1QxL2Z5VmJhbUY1OEJxaDNra08zRVZmUmd0OHZ1WEFQWC9vV3lYOTZIV0pZOGh0QVZDVjRxRDFhcm1zMFBjPQ%3D%3D%7C1685363431342%7CVTJGc2RHVmtYMTlKUWlJVFA4NFQwdFNoa3pQWUIvS1grWGt0c3ppR0JwRGRXY0lGOC9wS0xJR05OS3VpZk1QdDdkVisrempUWi9zcnBrU1IwbnZkL0E9PQ%3D%3D%7CVTJGc2RHVmtYMTlET2lvSXE2eFZvVlM4WFkrN1hEMTBlNks1S3krRkl1VUxxaXE3c0E2VXhKK0g5M0FJWi9JWWw5NWtwVWUreUd2NnRLNUcrVEszZ0RTeDlQYzFWdG1hT1ZxcVY5cldOUWpPdkdIRGdHb2R5MUZpK1ZleVFMQWVvRWtlcEFCZ1RGcmtYQ2h5YlZDTkdIVlZJNlh1YlJzbGJLUmFQZ29YUDN4MWVrdEUyd2poOVlucjA3aSs5Sk5BSmZNYVo4L2ZGMHFSRWZsaVdCdWdhbFVka1VjMTBSMnkyMENnNzdnZk5ZblZCazVjM1hncGYvanZWMjZkUEJoYUc4QTkvWE5SZTI0NHY3NG5ZYjVMWmdLTllYVm52U3A2ckIrL1gwNE5uYmhtOEl4endseGhxUHg4eWFsRUltRG5JUjdyV3A4b2xYWFJ4VDFabytIZGZDYW4rd2hpNWlCRSttVmZEMUZvWmRlM2NmVERTMXVaYVhlU3ExZDJrYzUrMkN1ZGNkMW5vWFBwNmxuSW0rQlBsRlZ2cXpmY2pUTEFYQXFaOUZTMTd5eWw0MlFBYXY1Rkt5Mzh6ekhLc0RsMEZ4OVpPbHpjT2IwbHlvZzN3SDBNVWtkaGJ0K1o1UWpQN3loSnpHTXBnSUQrR3g1YzBVQkFWblVLSS8rMkx2eVdiQTVyL3FxcHhBai9rbjhqK1c5ZEZGdzRiTEg3WGEzc2J0dXpvV2hmM20rWFdZZ0JITXRwbWdlNnBvaFhVSFdNWGhMdTM3VTEvVTYxQVNyNWk2MGVVS2ZVVEhjUkwwajdUNnpYL0FDQ3ozNW0rK2w1ZzFFWXFUS3JmVmRDTldWYkI4d21jOEdNVDB4eHB6ZFMvQ3djbUNkOWZPMlMxblFFd0FGZldpZ1Vrb1BCcndva2pYMzBEK3BucEFKbEpjQ3NwOGxRSzlGQVhtVTRsOHJLQW1EVEM4cGhXZlJ5bUxaSjZkYW5ZRXhKQUk4dUJsMWhFSFFXa3JRNVNZeUZKb0Vi',
            'Referer': 'https://piao.qunar.com/ticket/list.htm?keyword=%E7%A6%8F%E5%BB%BA&region=&from=mpl_search_suggest&page=2',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }
        self.session.headers = self.headers


    def __get_params(self, page):
        return {
            'keyword': self.key_words,
            'region': 'null',
            'from': 'mps_search_suggest',
            'page': page
        }

    def get_one_page(self, page):
        time.sleep(1)
        print(f'正在爬取{self.key_words}第{page}页')
        with self.session.get(url=self.url, params=self.__get_params(page)) as resp:
            result = resp.json()
            infos = self.__parse_page(result)
            return infos

    def __parse_page(self, page_json):
        lists = page_json['data']['sightList']
        infos = []
        for sight in lists:
            sightName = sight['sightName']
            star = sight.get('star', '')
            saleCount = sight['saleCount']
            qunarPrice = sight.get('qunarPrice', '')
            intro = sight.get('intro', '')
            districts = sight['districts']
            score = sight['score'].replace('0.0', '3.5')
            result = {
                      "sightName":sightName, 
                      "star":star, 
                      "saleCount":saleCount, 
                      "qunarPrice":qunarPrice, 
                      "intro":intro, 
                      "districts":districts, 
                      "score":score
                      }
            infos.append(result)
        self.writer.writerows(infos)
        return True

    def get_whole_province(self, begin=1):
        with open("福建省旅游数据.csv",'a',newline='',encoding='utf-8') as f:
            self.writer = csv.DictWriter(f,fieldnames=
                ["sightName","star","saleCount","qunarPrice","intro","districts", "score"])
            self.writer.writeheader()
            try:
                while self.get_one_page(begin):
                    begin += 1
                print(f'{self.key_words}爬取完毕')
            except:
                print('爬太快ip被封了')


if __name__ == '__main__':
    qunar = Qunar()
    qunar.key_words = '福建'
    qunar.get_whole_province(begin=1)
