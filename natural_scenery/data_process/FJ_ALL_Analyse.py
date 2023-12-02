import pandas as pd
from pyecharts.globals import GeoType
from pyecharts import options as opts
import webbrowser
import plotly_express as px
from pyecharts.charts import Geo, Map, Pie
import jieba

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np



class FJ_Province():
    def __init__(self) -> None:
        self.data = pd.read_csv("data/福建省旅游数据.csv", encoding='utf-8')
        # 数据的清洗，填补空缺值
        self.data['qunarPrice'] = self.data['qunarPrice'].fillna(float(0))
        self.data['saleCount'] = self.data['saleCount'].fillna(float(0))
        self.data = self.data.fillna("0")
        
        self.counties = ["福州市", "莆田市", "泉州市", "厦门市", "漳州市", "南平市", "三明市", "龙岩市", "宁德市"]
        
        self.sights_5A_data = self.data[self.data['star'] == "5A"]
        self.sights_4A_data = self.data[self.data['star'] == "4A"]
        self.sight_A_data = self.data[self.data['star'].str.contains("A")]
        
    def Sight_Star(self):
        sights_5A_scater = [
                            [
                                self.counties[i], 
                                len(self.sights_5A_data[self.sights_5A_data["districts"].str.contains(self.counties[i][:2])])
                             ] for i in range(len(self.counties))
                           ]
        print(sights_5A_scater)
        Map_5A = (
                    Map(init_opts=opts.InitOpts(width="1080px", height="1080px"))
                    .add
                    (
                        "",
                        sights_5A_scater,
                        "福建",
                    )
                    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                    .set_global_opts
                    (
                        title_opts=opts.TitleOpts(title='福建省5A景区分布图'),
                        visualmap_opts=opts.VisualMapOpts(
                            max_=5,
                            split_number=5,
                            is_piecewise=True)
                    )
                    .render("5A_sights_scater.html")
                )
        webbrowser.open_new_tab(Map_5A)

        sights_4A_scater = [
                            [
                                self.counties[i], 
                                len(self.sights_4A_data[self.sights_4A_data["districts"].str.contains(self.counties[i][:2])])
                             ] for i in range(len(self.counties))
                           ]
        Map_4A = (
                    Map(init_opts=opts.InitOpts(width="1080px", height="1080px"))
                    .add
                    (
                        "",
                        sights_4A_scater,
                        "福建",
                    )
                    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                    .set_global_opts
                    (
                        title_opts=opts.TitleOpts(title='福建省4A景区分布图'),
                        visualmap_opts=opts.VisualMapOpts(
                            max_=20,
                            split_number=10,
                            is_piecewise=True)
                    )
                    .render("4A_sights_scater.html")
                )
        webbrowser.open_new_tab(Map_4A)

        
    def Heat_Scatter(self):
        heat_scatter = [
                        [
                            self.counties[i],
                            self.sight_A_data[self.sight_A_data["districts"].str.contains(self.counties[i][:2])]["score"].mean()
                        ] for i in range(len(self.counties))
                       ]
        heat_map = (
                    Map(init_opts=opts.InitOpts(width="1080px", height="1080px"))
                   .add
                    (
                        "",
                        heat_scatter,
                        "福建",
                    )
                    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                    .set_global_opts
                    (
                        title_opts=opts.TitleOpts(title='福建省各市旅游热度图'),
                        visualmap_opts=opts.VisualMapOpts(
                            max_=5,
                            split_number=10,
                            is_piecewise=True)
                    )
                    .render("heat_sights_scater.html")                                        
        )
        webbrowser.open_new_tab(heat_map)

        price_scatter = [
                        [
                            self.counties[i],
                            self.sight_A_data[self.sight_A_data["districts"].str.contains(self.counties[i][:2])]["qunarPrice"].mean()  
                        ] for i in range(len(self.counties))
                       ]
        price_map = (
                    Map(init_opts=opts.InitOpts(width="1080px", height="1080px"))
                   .add
                    (
                        "",
                        price_scatter,
                        "福建",
                    )
                    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                    .set_global_opts
                    (
                        title_opts=opts.TitleOpts(title='福建省各市旅游景区平均门票价格图'),
                        visualmap_opts=opts.VisualMapOpts(
                            max_=200,
                            split_number=10,
                            is_piecewise=True)
                    )
                    .render("price_sights_scater.html")                                        
        )
        webbrowser.open_new_tab(price_map)        

    
    def word_show(self):
        for i in range(len(self.counties)):
            jieba_list = []
            
            for intro in self.sight_A_data[self.sight_A_data['districts'].str.contains(self.counties[i][:2])]['intro']:
                seg_list = jieba.cut(intro)
                for each in seg_list:
                    jieba_list.append(each)
                                       
            stopwords = [
                line.strip() for line in open(
                    "data/word/stop_word.txt",
                    'r',
                    encoding='utf-8').readlines()]
            
            stopword_list = []
            for word in jieba_list:
                if word not in stopwords:
                    if word != "\t" and word != " ":
                        stopword_list.append(word)

            text = " ".join(i for i in stopword_list)


            wc = WordCloud(collocations=False, 
                font_path= "C:\Windows\Fonts\SIMYOU.ttf",
                max_words=2000,width=4000,
                height=4000, margin=2).generate(text.lower())

            plt.imshow(wc)
            plt.axis("off")
            plt.show()

            wc.to_file("data/" + self.counties[i] + "_intro.png")

            
    def ticket(self):
        price_bins = [-1,0, 30, 50, 100, 150, 200, 250, 300]
        a, b = pd.cut(x=self.sight_A_data['qunarPrice'], bins=price_bins, labels=["免费","0-30 RMB" ,"30-50 RMB", "50-100 RMB", "100-150 RMB", '150-200 RMB', "200-250 RMB", "250-300 RMB"],right=True,retbins=True)
        print(a)
        print("b:",b)
        pie = Pie(init_opts=opts.InitOpts(width='1080px', height='1080px', bg_color='white'))
        pie.add(
            '', [list(z) for z in zip([price for price in a.value_counts().index], a.value_counts())],
            radius=['10%', '70%'], center=['50%', '50%'], rosetype="radius"
        ).set_series_opts(
            label_opts=opts.LabelOpts(formatter="{b}: {c}")
        ).set_global_opts(
            title_opts=opts.TitleOpts(title='福建省景区票价汇总)', pos_left='300', pos_top='20',
                title_textstyle_opts=opts.TextStyleOpts(color='black', font_size=16)),
            legend_opts=opts.LegendOpts(is_show=False)
        ).render('tickets_prices.html')
        # webbrowser.open_new_tab(pie)


        # 各市旅游景点门票销量
        sales_scatter = [
                        [
                            self.counties[i],
                            int(self.sight_A_data[self.sight_A_data["districts"].str.contains(self.counties[i][:2])]["saleCount"].sum()) 
                        ] for i in range(len(self.counties))
                       ]
        sales_map = (
                    Map(init_opts=opts.InitOpts(width="1080px", height="1080px"))
                   .add
                    (
                        "",
                        sales_scatter,
                        "福建",
                    )
                    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                    .set_global_opts
                    (
                        title_opts=opts.TitleOpts(title='福建省各市旅游景区平均门票销售情况'),
                        visualmap_opts=opts.VisualMapOpts(
                            max_=10000,
                            split_number=10,
                            is_piecewise=True)
                    )
                    .render("heat_sale_scater.html")                                        
        )
        webbrowser.open_new_tab(sales_map)    

            
if __name__ == "__main__":
    data = FJ_Province()
    data.Sight_Star()
    data.Heat_Scatter()
    data.ticket()
    data.word_show()
    