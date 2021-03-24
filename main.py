from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta, datetime, date
import requests
import random
import json

app = Flask(__name__)
app.secret_key = b'SecurePassword1234'
app.permanent_session_lifetime = timedelta(weeks=52.17857)

base = json.loads(requests.get('https://kitsu.io/api/edge/anime').content)['meta']['count']

@app.route('/')
def index():
    return render_template('index.html', trend=json.loads(requests.get('https://kitsu.io/api/edge/trending/anime').content), adventure=json.loads(requests.get('https://kitsu.io/api/edge/anime?sort=-averageRating&filter[categories]=adventure').content),romance=json.loads(requests.get('https://kitsu.io/api/edge/anime?sort=-averageRating&filter[categories]=romance').content),cooking=json.loads(requests.get('https://kitsu.io/api/edge/anime?sort=-averageRating&filter[categories]=cooking').content),highschool=json.loads(requests.get('https://kitsu.io/api/edge/anime?sort=-averageRating&filter[categories]=high-school').content),magic=json.loads(requests.get('https://kitsu.io/api/edge/anime?sort=-averageRating&filter[categories]=magic').content),fantasy=json.loads(requests.get('https://kitsu.io/api/edge/anime?sort=-averageRating&filter[categories]=fantasy&page[offset]=20').content),demon=json.loads(requests.get('https://kitsu.io/api/edge/anime?sort=-averageRating&filter[categories]=demon').content),combat=json.loads(requests.get('https://kitsu.io/api/edge/anime?sort=-averageRating&filter[categories]=combat').content),top=json.loads(requests.get('https://kitsu.io/api/edge/anime?sort=ratingRank').content), base=base)

@app.route('/browse/', defaults={'page':0})
@app.route('/browse/<string:page>')
def browse(page):
    return render_template('browse.html', anime=json.loads(requests.get(f'https://kitsu.io/api/edge/anime?page[limit]=8&sort=-averageRating&page[offset]={page}').content),base=base,page=page)  


@app.route('/s/', defaults={'anime': None,'page':0})
@app.route('/s/<string:anime>', defaults={'page':0})
@app.route('/s/<string:anime>/<string:page>')
def animelist(anime, page):
    if anime == None:
        return redirect(url_for('index'))
    else:
        return render_template('searchlist.html', anime=json.loads(requests.get(f"https://kitsu.io/api/edge/anime?filter[text]={anime}&page[limit]=20&page[offset]={page}").content), search=anime, page=page, id=anime, base=base)

@app.route('/search/post', methods=["POST"])
def searchlist():
    anime = request.form['animes']
    return redirect(url_for('animelist', anime=anime))

@app.route('/a/', defaults={'anime': None})
@app.route('/a/<string:anime>/')
def anime(anime):
    if anime == None:
        return redirect(url_for('index'))
    else:
        return render_template('anime.html', anime=json.loads(requests.get(f"https://kitsu.io/api/edge/anime/{anime}").content)['data'], genere=json.loads(requests.get(f"https://kitsu.io/api/edge/anime/{anime}/categories").content)['data'], episodes=json.loads(requests.get(f"https://kitsu.io/api/edge/anime/{anime}/episodes").content)['data'] ,base=base)
    
@app.route('/c/', defaults={'offset': 0})
@app.route('/c/<int:offset>')
def category(offset):
    try:
        offset = int(offset)
        if offset > 208:
            return render_template('category.html', data=json.loads(requests.get(f'https://kitsu.io/api/edge/categories?page%5Blimit%5D=10&page%5Boffset%5D=208').content), offset=208, base=base)
        else:
            return render_template('category.html', data=json.loads(requests.get(f'https://kitsu.io/api/edge/categories?page%5Blimit%5D=10&page%5Boffset%5D={offset}').content), offset=offset, base=base)
    except:
        return render_template('category.html', data=json.loads(requests.get(f'https://kitsu.io/api/edge/categories?page%5Blimit%5D=10&page%5Boffset%5D=0').content), offset=0, base=base)

@app.route('/c/s/', defaults={'ids': 0,'page':0})
@app.route('/c/s/<string:ids>', defaults={'page':0})
@app.route('/c/s/<string:ids>/<string:page>')
def categorySearch(ids, page):
    if ids == 0:
        return redirect(url_for('category'))
    else:
        #return f"id = {ids}, page = {page}"
        return render_template('catSearch.html', anime=json.loads(requests.get(f'https://kitsu.io/api/edge/categories/{ids}/anime?page[offset]={page}').content), id=ids, page=page, base=base)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='localhsot', port=80, debug=True)  