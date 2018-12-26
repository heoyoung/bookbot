def week_search(year,month,week):

  url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&CID=0&Year="+str(year)+"&Month="+str(month)+"&Week="+str(week)+"&BestType=Bestseller&SearchSubBarcode="

  soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")

  book_titles = soup.find_all("div", class_="ss_book_list")
  book_titles = book_titles[:30]

  book_title = []

  for ui in book_titles:
      for li in ui.find_all("li")[0:3]:
          if li.find_all("span", class_="ss_ht1"):
              continue
          elif li.get_text().startswith("이 책의 전자책"):
              continue
          elif "개정판이 새로" in li.get_text():
              continue
          elif "여기를 누르세요" in li.get_text():
              continue
          elif li.get_text().startswith("반품 및 교환 불가"):
              continue
          elif li.get_text().startswith("지금 주문하면"):
              continue
          elif li.get_text().startswith("출고예상일"):
              continue
          elif "10%할인" in li.get_text():
              continue
          elif li.get_text().startswith("*"):
              continue
          else:
              book_title.append(li.get_text().strip())

  # print(u'\n'.join(book_title))
  rank=[]
  rank.append(str(year)+"년 "+str(month)+"월 "+str(week)+"주의 베스트셀러입니다.")
  for i in range(0, 10):
      rank.append("---------------------------------------------")
      rank.append(str(i + 1) + "위 " + book_title[2 * i] + '\n' + book_title[1 + 2 * i])

  return u'\n'.join(rank)


def month_search(year, month):

   url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&CID=0&Year=" + year + "&Month=" +month + "&BestType=MonthlyBest&SearchSubBarcode="
   soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('cp949', 'ignore'), "html.parser")

   book_titles = soup.find_all("div", class_="ss_book_list")
   book_titles = book_titles[:30]

   book_title = []

   for ui in book_titles:
       for li in ui.find_all("li")[0:3]:
           if li.find_all("span", class_="ss_ht1"):
               continue
           elif li.get_text().startswith("이 책의 전자책"):
               continue
           elif "개정판이 새로" in li.get_text():
               continue
           elif li.get_text().startswith("반품 및 교환 불가"):
               continue
           elif li.get_text().startswith("지금 주문하면"):
               continue
           elif li.get_text().startswith("출고예상일"):
               continue
           elif "여기를 누르세요" in li.get_text():
              continue
           elif "10%할인" in li.get_text():
               continue
           elif li.get_text().startswith("*"):
               continue
           else:
               book_title.append(li.get_text().strip())

   # print(u'\n'.join(book_title))
   rank = []
   rank.append(str(year) + "년 " + str(month) + "월의 베스트셀러입니다.")
   for i in range(0, 10):
       rank.append("---------------------------------------------")
       rank.append(str(i + 1) + "위 " + book_title[2 * i] + '\n' + book_title[1 + 2 * i])

   return u'\n'.join(rank)

year = re.findall('[0-9]+[년]', text)
   month = re.findall('[0-9]+[월]', text)
   week = re.findall('[0-9]+[주]', text)



   if len(year) == 1 and len(month) == 1 and len(week) == 1 :
       return week_search(year[0][0:-1], month[0][0:-1], week[0][0:-1])
   elif len(year) == 1 and len(month) == 1 and len(week) == 0 :
       return month_search(year[0][0:-1], month[0][0:-1])
   elif "주간베스트" in text:
       return weekly_best()
   elif "월간베스트" in text:
       return monthly_best()
   else:
       return " 키워드를 입력해주세요\n 1. 주간베스트(이번 주의 베스트셀러 10위까지 보여집니다)\n 2. 월간베스트(이번 달의 베스트셀러 10위까지 보여집니다)"
