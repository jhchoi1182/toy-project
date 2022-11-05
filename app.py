import re

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import datetime
import jwt
import hashlib
import requests
from bs4 import BeautifulSoup

m = hashlib.sha256()
m.update('Life is too short'.encode('utf-8'))

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.lyxqol2.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('http://www.cgv.co.kr/movies/pre-movies.aspx', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pre-movies')
def premovies():
    return render_template('premovies.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    db.movies.drop()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('http://www.cgv.co.kr/movies/?lt=1&ft=0', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title_temp = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(2) > li:nth-child(number) > div.box-contents > a > strong'
    rank_temp = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(2) > li:nth-child(number) > div.box-image > strong'
    rate_temp = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(2) > li:nth-child(number) > div.box-contents > div > strong'
    image_temp = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(2) > li:nth-child(number) > div.box-image > a > span > img'

    for i in range(1, 4):
        title_tag = title_temp.replace('number', str(i))
        rank_tag = rank_temp.replace('number', str(i))
        rate_tag = rate_temp.replace('number', str(i))
        image_tag = image_temp.replace('number', str(i))

        titles = soup.select_one(title_tag).text
        ranks = soup.select_one(rank_tag).text
        rates = soup.select_one(rate_tag).text
        images = soup.select_one(image_tag)['src']

        doc = {
            'title': titles,
            'rank': ranks,
            'rate': rates,
            'image': images
        }
        db.movies.insert_one(doc)

    title_temp2 = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(3) > li:nth-child(number) > div.box-contents > a > strong'
    rank_temp2 = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(3) > li:nth-child(number) > div.box-image > strong'
    rate_temp2 = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(3) > li:nth-child(number) > div.box-contents > div > strong'
    image_temp2 = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol:nth-child(3) > li:nth-child(number) > div.box-image > a > span > img'

    for i in range(1, 5):
        title_tag2 = title_temp2.replace('number', str(i))
        rank_tag2 = rank_temp2.replace('number', str(i))
        rate_tag2 = rate_temp2.replace('number', str(i))
        image_tag2 = image_temp2.replace('number', str(i))

        titles2 = soup.select_one(title_tag2).text
        ranks2 = soup.select_one(rank_tag2).text
        rates2 = soup.select_one(rate_tag2).text
        images2 = soup.select_one(image_tag2)['src']

        doc = {
            'title': titles2,
            'rank': ranks2,
            'rate': rates2,
            'image': images2
        }
        db.movies.insert_one(doc)

    title_temp3 = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol.list-more > li:nth-child(number) > div.box-contents > a > strong'
    rank_temp3 = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol.list-more > li:nth-child(number) > div.box-image > strong'
    rate_temp3 = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol.list-more > li:nth-child(number) > div.box-contents > div > strong'
    image_temp3 = '#contents > div.wrap-movie-chart > div.sect-movie-chart > ol.list-more > li:nth-child(number) > div.box-image > a > span > img'

    for i in range(1, 13):
        title_tag3 = title_temp3.replace('number', str(i))
        rank_tag3 = rank_temp3.replace('number', str(i))
        rate_tag3 = rate_temp3.replace('number', str(i))
        image_tag3 = image_temp3.replace('number', str(i))

        titles3 = soup.select_one(title_tag3).text
        ranks3 = soup.select_one(rank_tag3).text
        rates3 = soup.select_one(rate_tag3).text
        images3 = soup.select_one(image_tag3)['src']

        doc = {
            'title': titles3,
            'rank': ranks3,
            'rate': rates3,
            'image': images3
        }
        db.movies.insert_one(doc)

    return jsonify({'msg': '로딩완료'})



@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({}, {'_id': False}))

    return jsonify({'movies':movie_list})


@app.route('/pre', methods=['GET'])
def pre_get():
    premovie_list = list(db.preMovies.find({}, {'_id': False}))
    return jsonify({'preMovies': premovie_list})

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def signup():
    reg = "^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$"

    user_name = request.form['user_name']
    user_id = request.form['user_id']
    user_password = request.form['user_password']
    user_re_password = request.form['user_re_password']

    if not (user_id and user_password and user_re_password):
        return jsonify({'msg': '정보를 모두 입력해주세요!'})
    if bool(re.Match(reg,user_id)):
        return jsonify({'msg': '유효한 이메일 주소가 아닙니다.'})
    elif user_password != user_re_password:
        return jsonify({'msg': '비밀번혹가 일치하지 않습니다.'})
    else:
        doc = {
            'user_name' : user_name,
            'user_id': user_id,
            'user_password': user_password,
            'user_re_password': user_re_password
        }
    db.hiuser.insert_one(doc)

    return jsonify({'msg': '회원가입 완료!'})


SECRET_PRE = 'SPARTA'


@app.route('/login', methods=['POST'])
def login():

    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    result = db.hiuser.find_one({'user_id': id_receive, 'user_password': pw_receive})
    nick= db.hiuser.find_one({'user_id':id_receive})
    name = (nick['user_name'])


    print(result)
    if result is not None:
        payload = {
            'user_id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600)
        }

        token = jwt.encode(payload, SECRET_PRE, algorithm='HS256').decode('utf-8')
        return jsonify({'result': 'success', 'token': token,'name' : name});

        header = jwt.decode(payload, SECRET_PRE, algorithm='HS256')
        value = header.get("user_name")
        print(value)

    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'});

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)
