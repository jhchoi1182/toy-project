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

@app.route('/pre-movies')
def premovies():
    return render_template('premovies.html')

@app.route('/pre', methods=['GET'])
def pre_get():
    premovie_list = list(db.preMovies.find({}, {'_id': False}))
    return jsonify({'preMovies': premovie_list})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)


# 상영예정작 크롤링 ##
#
# tagTemp = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(number) > li'
# for i in range(4,52,2):
#     tag = tagTemp.replace('number',str(i))
#     movies = soup.select(tag)
#
#     for movie in movies:
#         title = movie.select_one('div.box-contents > a > strong').text
#         img = movie.select_one('div.box-image > a > span > img')['src']
#         link = movie.select_one('div.box-image > a')['href']
#         booking = movie.select_one('div.box-contents > div > strong').text
#         date = movie.select_one('div.box-contents > span.txt-info > strong').text.split()[0]
#         schedule = movie.select_one('div.box-contents > span.txt-info > strong > span').text
#
#         doc = {
#             'title': title,
#             'img': img,
#             'link': link,
#             'booking': booking,
#             'date': date,
#             'schedule': schedule
#         }
#
#         db.preMovies.insert_one(doc)

