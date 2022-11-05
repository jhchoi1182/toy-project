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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pre-movies')
def premovies():
    return render_template('premovies.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    return jsonify({'msg':'로딩완료'})


@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({}, {'_id': False}))

    return jsonify({'movies':movie_list})

@app.route('/pre', methods=['GET'])
def pre_get():
    premovie_list = list(db.preMovies.find({}, {'_id': False}))
    return jsonify({'preMovies': premovie_list})

# ----------로그인 회원가입----------
@app.route('/login')
def home():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def signup():
    user_name = request.form['user_name']
    user_id = request.form['user_id']
    user_password = request.form['user_password']
    user_re_password = request.form['user_re_password']

    if not (user_id and user_password and user_re_password):
        return jsonify({'msg': '정보를 모두 입력해주세요!'})
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
