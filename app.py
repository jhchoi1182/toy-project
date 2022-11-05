from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://jhchoi:0000@cluster0.p7jslyb.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('http://www.cgv.co.kr/movies/pre-movies.aspx', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')


    #contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(2) > li:nth-child(1) > div.box-image > a > span > img
    #contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(3) > li:nth-child(1) > div.box-image > a > span > img
    #contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(3) > li:nth-child(4) > div.box-image > a > span > img
    #contents > div.wrap-movie-chart > div.sect-movie-chart > ol.list-more > li:nth-child(1) > div.box-image > a > span > img
    #contents > div.wrap-movie-chart > div.sect-movie-chart > ol.list-more > li:nth-child(2) > div.box-image > a > span > img

#contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(2) > li:nth-child(1) > div.box-contents > a > strong
#contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(3) > li:nth-child(1) > div.box-contents > a > strong

Atemp = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(number) > li'
for i in range(2, 3, 1):
    test = Atemp.replace('number', str(i))
    aaa = soup.select(test)

    for aa in aaa:
        titles = soup.select_one('div.box-contents > a > strong').text


        print(titles)