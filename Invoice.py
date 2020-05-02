# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import bs4, requests

class Invoice():
    def __init__(self):
        self.base_url = 'https://www.etax.nat.gov.tw/etw-main/web/'
        self.year = 109
        self.moth = 1
    def cin(self):
        self.year = input("請輸入要兌獎之年分 : ")
        self.moth = int(input("請輸入要兌獎之月分 : "))

    def set_date(self,year,moth):
        self.year = year
        self.moth = moth
        if self.moth % 2 == 0:
            self.moth = str(self.moth-1)
        else:
            self.moth = str(self.moth)

        if len(self.moth) != 2:
            self.moth = "0"+self.moth

    def get_number(self):
        number = []
        try:
            url = self.base_url + "ETW183W2_{}{}/".format(self.year,self.moth)
            html = requests.get(url)
            html.raise_for_status() # 驗證網頁是否下載成功
            print("網頁下載完成")
            print(url)
            print("{}年{}月開獎號碼".format(self.year,self.moth))
            html.encoding = "UTF-8"
            objSoup = bs4.BeautifulSoup(html.text, 'lxml') # 建立BeautifulSoup物件
            dataTag1 = objSoup.find("tbody")
            title_name = ["specialPrize","grandPrize","firstPrize","addSixPrize"]
            for name in title_name:
                  dataTag_title = dataTag1.find("th",id = name)
                  dataTag_number = dataTag1.find("td",headers = name)
                  print(dataTag_title.text)
                  print(dataTag_number.text)
                  number.append(dataTag_title.text+":"+dataTag_number.text)
        except Exception as e:
            print("輸入有誤",e)
            number.append("輸入有誤"+str(e))
        return number