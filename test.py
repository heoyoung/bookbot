# from test import *
import json
import os
import re
import urllib.request

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

# def call_key(text):
#     url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&start=we"
#     soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")
#
#     images = soup.find_all("div", class_="ss_book_box")
#     images = images[:30]
#
#     image = []
#     for i in images:
#         image.append(i.find("img")["src"])
#
#     print (image)
#     return image

def key():
    set_key = []
    set_key.append("키워드를 입력해주세요")
    set_key.append("1. 주간베스트 (이번 주의 베스트셀러 10위까지 보여집니다)")
    set_key.append("2. 주간베스트 검색 (●년 ●월 ●주를 입력하세요)")
    set_key.append("3. 월간베스트 (이번 달의 베스트셀러 10위까지 보여집니다)")
    set_key.append("4. 월간베스트 검색 (●년 ●월를 입력하세요)")
    set_key.append("5. 새로나온 책")
    set_key.append("6. 새로나올 책")

    image =""
    bookurl=""
    return 1, u'\n'.join(set_key), image, bookurl
    # return 1, set_key, image


def weekly_best():
    url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&start=we"
    soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")

    book_titles = soup.find_all("div", class_="ss_book_list")
    book_titles = book_titles[:30]

    book_title = []
    for ui in book_titles:
        for li in ui.find_all("li"):
            # print(li)
            # print("------")
            if li.find('a', href=True) and li.find("a")["href"]:
                if li.find("a")["href"].startswith("/Search"):
                    book_title.append(li.get_text().strip())
                    #print(li.get_text())
            if li.find_all("a", class_="bo3"):
                book_title.append(li.get_text().strip())
                #print(li.get_text().strip())


    rank = ['금주의 베스트셀러']
    for i in range(0, 10):
        rank.append("\n")
        rank.append(str(i + 1) + "위 " + book_title[2 * i] + '\n' + book_title[1 + 2 * i])

    images = soup.find_all("div", class_="ss_book_box")
    images = images[:30]

    image = [" "]
    for i in images:
        image.append(i.find("img")["src"])

    # urls = soup.find_all("div", class_="ss_book_list")
    #     #
    #     # book_url = []
    #     #
    #     # for ul in urls:
    #     #     for li in ul.find_all("li"):
    #     #         book_url.append(li.find("a")["href"])
    #     # print(book_url)
    #print(image)
    bookurl = []
    soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")
    book = soup.find_all("div", class_="ss_book_list")

    for ul in book:
        for li in ul.find_all("li")[0:2]:
            if li.find_all('a', class_=True):
                bookurl.append(li.find("a")["href"])

    return 2, rank, image, bookurl

def monthly_best():
    url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&BestType=MonthlyBest"
    soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")

    book_titles = soup.find_all("div", class_="ss_book_list")
    book_titles = book_titles[:30]

    book_title = []
    for ui in book_titles:
        for li in ui.find_all("li"):
            # print(li)
            # print("------")
            if li.find('a', href=True) and li.find("a")["href"]:
                if li.find("a")["href"].startswith("/Search"):
                    book_title.append(li.get_text().strip())
                    # print(li.get_text())
            if li.find_all("a", class_="bo3"):
                book_title.append(li.get_text().strip())
    # print (book_title)
    rank = ['월간베스트셀러']
    for i in range(0, 10):
        rank.append("\n")
        rank.append(str(i + 1) + "위 " + book_title[2 * i] + '\n' + book_title[1 + 2 * i])

    images = soup.find_all("div", class_="ss_book_box")
    images = images[:30]

    image = [" "]
    for i in images:
        image.append(i.find("img")["src"])

    bookurl = []
    soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")
    book = soup.find_all("div", class_="ss_book_list")

    for ul in book:
        for li in ul.find_all("li")[0:2]:
            if li.find_all('a', class_=True):
                bookurl.append(li.find("a")["href"])

    return 2, rank, image, bookurl
    # return u'\n'.join(rank)

def week_search(year,month,week):

  url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&CID=0&Year="+str(year)+"&Month="+str(month)+"&Week="+str(week)+"&BestType=Bestseller&SearchSubBarcode="

  soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")

  book_titles = soup.find_all("div", class_="ss_book_list")
  book_titles = book_titles[:30]

  book_title = []
  for ui in book_titles:
      for li in ui.find_all("li"):
          # print(li)
          # print("------")
          if li.find('a', href=True) and li.find("a")["href"]:
              if li.find("a")["href"].startswith("/Search"):
                  book_title.append(li.get_text().strip())
                  # print(li.get_text())
          if li.find_all("a", class_="bo3"):
              book_title.append(li.get_text().strip())


  # print(u'\n'.join(book_title))
  rank=[]
  rank.append(str(year)+"년 "+str(month)+"월 "+str(week)+"주의 베스트셀러입니다.")
  for i in range(0, 10):
      rank.append("\n")
      rank.append(str(i + 1) + "위 " + book_title[2 * i] + '\n' + book_title[1 + 2 * i])

  images = soup.find_all("div", class_="ss_book_box")
  images = images[:30]

  image = [" "]
  for i in images:
      image.append(i.find("img")["src"])

  bookurl = []
  soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")
  book = soup.find_all("div", class_="ss_book_list")

  for ul in book:
      for li in ul.find_all("li")[0:2]:
          if li.find_all('a', class_=True):
              bookurl.append(li.find("a")["href"])

  return 2, rank, image, bookurl

  # return u'\n'.join(rank)


def month_search(year, month):

   url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&CID=0&Year=" + year + "&Month=" +month + "&BestType=MonthlyBest&SearchSubBarcode="
   soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")

   book_titles = soup.find_all("div", class_="ss_book_list")
   book_titles = book_titles[:30]

   book_title = []
   for ui in book_titles:
       for li in ui.find_all("li"):
           # print(li)
           # print("------")
           if li.find('a', href=True) and li.find("a")["href"]:
               if li.find("a")["href"].startswith("/Search"):
                   book_title.append(li.get_text().strip())
                   # print(li.get_text())
           if li.find_all("a", class_="bo3"):
               book_title.append(li.get_text().strip())

   # print(u'\n'.join(book_title))
   rank = []
   rank.append(str(year) + "년 " + str(month) + "월의 베스트셀러입니다.")
   for i in range(0, 10):
       rank.append("\n")
       rank.append(str(i + 1) + "위 " + book_title[2 * i] + '\n' + book_title[1 + 2 * i])

   images = soup.find_all("div", class_="ss_book_box")
   images = images[:30]

   image = [" "]
   for i in images:
       image.append(i.find("img")["src"])

   bookurl = []
   soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")
   book = soup.find_all("div", class_="ss_book_list")

   for ul in book:
       for li in ul.find_all("li")[0:2]:
           if li.find_all('a', class_=True):
               bookurl.append(li.find("a")["href"])

   return 2, rank, image, bookurl

def new_book():

    url = "https://www.aladin.co.kr/shop/common/wnew.aspx?BranchType=1"

    soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")

    book_titles = soup.find_all("div", class_="ss_book_list")
    book_titles = book_titles[:30]

    book_title = []
    #book_author =[]
    for ui in book_titles:
        for li in ui.find_all("li"):
            # print(li)
            # print("------")
            if li.find('a', href=True) and li.find("a")["href"]:
                if li.find("a")["href"].startswith("/Search"):
                    book_title.append(li.get_text().strip())
                    # print(li.get_text())
            if li.find_all("a", class_="bo3"):
                book_title.append(li.get_text().strip())

    # print(u'\n'.join(book_title))
    rank = []
    rank.append("새로나온 책입니다.")
    for i in range(0, 10):
        rank.append("\n")
        rank.append(str(i + 1) + ". " + book_title[2 * i] + '\n' + book_title[1 + 2 * i])
    images = soup.find_all("div", class_="ss_book_box")
    images = images[:30]

    image = [" "]
    for i in images:
        image.append(i.find("img")["src"])

    bookurl = []
    soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")
    book = soup.find_all("div", class_="ss_book_list")

    for ul in book:
        for li in ul.find_all("li")[0:2]:
            if li.find_all('a', class_=True):
                bookurl.append(li.find("a")["href"])

    return 2, rank, image, bookurl

def comming_book():
    url = "https://www.aladin.co.kr/shop/common/wcomming_new.aspx"

    soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")

    book_titles = soup.find_all("div", class_="ss_book_list")
    book_titles = book_titles[:30]

    book_title = []
    for ui in book_titles:
        for li in ui.find_all("li"):
            # print(li)
            # print("------")
            if li.find('a', href=True) and li.find("a")["href"]:
                if li.find("a")["href"].startswith("/Search"):
                    book_title.append(li.get_text().strip())
                    # print(li.get_text())
            if li.find_all("a", class_="bo3"):
                book_title.append(li.get_text().strip())

    # print(u'\n'.join(book_title))
    rank = []
    rank.append("새로나올 책입니다.")
    for i in range(0, 10):
        rank.append("\n")
        rank.append(str(i + 1) + ". " + book_title[2 * i] + '\n' + book_title[1 + 2 * i])
    images = soup.find_all("div", class_="ss_book_box")
    images = images[:30]

    image = [" "]
    for i in images:
        image.append(i.find("img")["src"])

    bookurl = []
    soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")
    book = soup.find_all("div", class_="ss_book_list")

    for ul in book:
        for li in ul.find_all("li")[0:2]:
            if li.find_all('a', class_=True):
                bookurl.append(li.find("a")["href"])

    return 2, rank, image, bookurl
