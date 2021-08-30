'''
Author: Derry
Email: drlv@stu.xidian.edu.cn
Date: 2021-01-27 22:46:26
LastEditors: Derry
LastEditTime: 2021-01-31 13:36:57
Description: 12306车票查询
'''

import requests
import json


class Query(object):
    def __init__(self):
        with open('station_info.json', encoding='utf-8') as f:
            self.city2code = json.load(f)
            self.code2city = {v: k for k, v in self.city2code.items()}
        with open('cities_list.txt', encoding='utf-8') as f:
            self.cities = []
            for line in f:
                self.cities.append(line.strip())

    def list2dict(self, data_list):
        train_info = {}
        train_info['运行信息'] = data_list[1]
        train_info['车次'] = data_list[3]
        train_info['起点站'] = self.code2city[data_list[4]]
        train_info['终点站'] = self.code2city[data_list[5]]
        train_info['出发站'] = self.code2city[data_list[6]]
        train_info['到达站'] = self.code2city[data_list[7]]
        train_info['出发时间'] = data_list[8]
        train_info['到达时间'] = data_list[9]
        train_info['历时'] = data_list[10]
        train_info['高级软卧'] = data_list[21]
        train_info['软卧'] = data_list[23]
        train_info['软座'] = data_list[24]
        train_info['特等座'] = data_list[25]
        train_info['无座'] = data_list[26]
        train_info['二等包座'] = data_list[27]
        train_info['硬卧'] = data_list[28]
        train_info['硬座'] = data_list[29]
        train_info['二等座'] = data_list[30]
        train_info['一等座'] = data_list[31]
        train_info['商务座'] = data_list[32]
        train_info['动卧'] = data_list[33]
        return train_info

    def request(self, from_station="北京", to_station="上海", date="2021-02-01", types=''):
        print(from_station, '->', to_station, date)
        url = ("https://kyfw.12306.cn/otn/leftTicket/queryZ?"
               "leftTicketDTO.train_date={}&"
               "leftTicketDTO.from_station={}&"
               "leftTicketDTO.to_station={}&"
               "purpose_codes=ADULT").format(date, self.city2code[from_station], self.city2code[to_station])
        headers = {
            "Cookie": "_uab_collina=160395250285657341202147; JSESSIONID=7C56E896658518A4E5BF99889839D00C; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; BIGipServerotn=1725497610.50210.0000; RAIL_EXPIRATION=1604632917257; RAIL_DEVICEID=DeBrCMshZyD9JIK2yazJV4op0oxRXXKpeio_Y27U75ZkWKFwOd6Q_i2JRVBJeN3Q9qQ7ybyTw4Vv3ImAEwdTAAh8XLXL6WGn3irR65rZyYeWtvToLkq8oVAprmAw6OPgPnqI9a9ItALNr0kFjzDkncjjGPINbqfa; BIGipServerpassport=770179338.50215.0000; route=c5c62a339e7744272a54643b3be5bf64; _jc_save_fromDate=2020-11-02; _jc_save_toDate=2020-11-01",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        }
        requests.packages.urllib3.disable_warnings()
        # verify=False参数表示不进行证书验证
        r = requests.get(url, headers=headers, verify=False)
        raw_trains = r.json()['data']['result']
        return raw_trains

    def analysis(self, raw_trains):
        train_info = []
        for raw_train in raw_trains:
            data_list = raw_train.split("|")
            train_info.append(self.list2dict(data_list))
        return train_info

    def pipeline(self):
        train_info_all = {}
        for depart in self.cities:
            for dest in self.cities:
                if depart != dest:
                    train_info = {}
                    train_info['出发地'] = depart
                    train_info['目的地'] = dest
                    while True:
                        try:
                            raw_trains = self.request(
                                depart, dest, "2021-02-10")
                            train_info['车次信息'] = self.analysis(raw_trains)
                            train_info_all[depart+'-'+dest] = train_info
                            break
                        except:
                            continue
            with open('train_info.json', 'w', encoding='utf-8') as f:
                json.dump(train_info_all, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    q = Query()
    q.pipeline()
