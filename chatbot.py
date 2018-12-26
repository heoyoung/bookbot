# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request
from test import *
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template


app = Flask(__name__)
#
slack_token = 
slack_client_id =
slack_client_secret =
slack_verification =
sc = SlackClient(slack_token)
slack_ts_back =""


# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    text = re.sub(r'<@\S+> ', '', text)
    year = re.findall('[0-9]+[년]', text)
    month = re.findall('[0-9]+[월]', text)
    week = re.findall('[0-9]+[주]', text)

    if len(year) == 1 and len(month) == 1 and len(week) == 1:
        return week_search(year[0][0:-1], month[0][0:-1], week[0][0:-1])
    elif len(year) == 1 and len(month) == 1 and len(week) == 0:
        return month_search(year[0][0:-1], month[0][0:-1])
    elif "주간베스트" in text:
        return weekly_best()
    elif "월간베스트" in text:
        return monthly_best()
    elif "새로나온" in text:
        return new_book()
    elif "새로나올" in text:
        return comming_book()
    else:
        return key()
    # return u'\n'.join(keywords)

# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])
    ss = slack_event["event"]["ts"]
    time =ss
    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]
        (menu, keywords, image,book_url) = _crawl_naver_keywords(text)
        #image = call_key(text)


        #msg={}
        #msg["text"]=keywords
        #print(image[0])
        if menu ==1:
            (menu, keywords, image, book_url)=key()
            text =keywords
            sc.api_call(
                "chat.postMessage",
                channel=channel,
                text=text
            )
        elif menu==2:
            for i in range(11):
                msg= {}
                msg["title"] = u'\n'.join(keywords[2*i:2*i+2])
                # msg["title"]= u'\n'.join(keywords[2*i:2*i+2]),
                if i != 0:
                    msg["title_link"]= book_url[i-1]
                msg["thumb_url"] = image[i]
                msg["color"]="#56c759"
                sc.api_call(
                    "chat.postMessage",
                    channel=channel,
                    attachments=json.dumps([msg])
                 )

        # text=u'\n'.join(keywords[0:5]),
        # attachments='[{"image_url":"http://i.ytimg.com/vi/tntOCGkgt98/maxresdefault.jpg"}]'
        # attachments= [{"thumb_url":image[0]}]
        # text=u'\n'.join(keywords[0:4]),
        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        global slack_ts_back
        if (slack_ts_back < slack_event["event"]["ts"]):
            slack_ts_back = slack_event["event"]["ts"]
            return _event_handler(event_type, slack_event)
        else:
            make_response(message, 200, {"duplicated": 1})



    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000)# 로컬 호스트
