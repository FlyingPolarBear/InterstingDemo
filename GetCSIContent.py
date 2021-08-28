'''
Author: Derry
Email: drlv@stu.xidian.edu.cn
Date: 2021-06-10 21:09:06
LastEditors: Derry
LastEditTime: 2021-06-11 11:22:21
Description: 一个小工具，来快速获得中证指数的成分股权重
'''
import matplotlib.pyplot as plt
import requests
import seaborn as sns
from bs4 import BeautifulSoup


class GetIndexContent(object):
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.base_url = "http://www.csindex.com.cn/zh-CN/indices/index-detail/"
        self.headers = {}
        requests.packages.urllib3.disable_warnings()
        sns.set()
        plt.rcParams['font.sans-serif'] = ['SimHei']

    def request_html(self):
        url = self.base_url + self.code
        r = requests.get(url, headers=self.headers, verify=False)
        r.encoding = r.apparent_encoding
        self.soup = BeautifulSoup(r.text, 'lxml')
        return self.soup

    def parse_html(self):
        table_header = self.soup.select(
            "body > div.zsxq.w1200.mt-30.mb-40 > div > div.details_r.fr > table > thead > tr")[0]
        ths = table_header.find_all('th')
        header = [ths[i].text for i in range(len(ths))]

        table_content = soup.select(
            "body > div.zsxq.w1200.mt-30.mb-40 > div > div.details_r.fr > table > tbody")[0]
        table = []
        for idx, tr in enumerate(table_content.find_all('tr')):
            tds = tr.find_all('td')
            tds_list = [tds[i].text for i in range(len(tds))]
            table.append(tds_list)
        self.table = table
        return header, table

    def plot(self):
        name = []
        percentage = []
        for t in self.table:
            percentage.append(round(float(t[-1]), 2))
            name.append(t[1]+' '+str(percentage[-1]))
        percentage.append(round(100-sum(percentage), 2))
        name.append('其他'+' '+str(percentage[-1]))
        plt.figure()
        plt.pie(percentage, labels=name)
        plt.savefig(self.name+'.png')


if __name__ == "__main__":
    name2code = {'银行': '000947', '电子': '930652',
                 '钢铁': '930606', '光伏': '931151'}

    for name, code in name2code.items():
        tool = GetIndexContent(name, code)
        while True:
            soup = tool.request_html()
            if len(soup):
                break
            else:
                print(name, "Error, retrying")
        header, table = tool.parse_html()
        tool.plot()

        with open(name+".txt", 'w', encoding='utf-8') as f:
            f.write('\t'.join(header)+'\n'+'\n'.join('\t'.join(t)for t in table) +
                    '\n总权重\t'+str(round(sum([float(t[-1]) for t in table]), 2)))
        print(name, 'Finished!')
