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

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)
