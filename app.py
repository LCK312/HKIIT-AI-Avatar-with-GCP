from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html.j2')

@app.route('/login')
def login():
    return render_template('login.html.j2')

@app.route('/reviews')
def reviews():
    return render_template('reviews.html.j2')

@app.route('/reviewa')
def reviewa():
    return render_template('reviewa.html.j2')

@app.route('/payment')
def payment():
    return render_template('payment.html.j2')

# Sample movie data (replace with your database or data source)
movies = [
    {'id': 1, 'title': 'IMAX 美國隊長4：勇敢新世界', 'description': '美國超級英雄電影', 'showtimes': '10:00, 13:00, 16:00'},
    {'id': 2, 'title': 'IMAX 封神第二部：戰火西岐', 'description': '姜子牙、姬發帶隊堅守西岐，家園保衛戰一觸即發！', 'showtimes': '11:00, 14:00, 17:00'},
    {'id': 3, 'title': '柏靈頓：秘魯大冒險(英語版)', 'description': '家庭喜劇', 'showtimes': '12:00, 15:00, 18:00'},
    {'id': 4, 'title': '完美伴侶', 'description': '愛情喜劇', 'showtimes': '13:30, 16:30, 19:30'},
    {'id': 5, 'title': '麻雀女王追男仔', 'description': '浪漫愛情喜劇', 'showtimes': '14:30, 17:30, 20:30'},
    {'id': 6, 'title': '原始巨星', 'description': '冒險動作片', 'showtimes': '15:30, 18:30, 21:30'}
]

@app.route('/daymovie')
def daymovie():
    return render_template('daymovie.html.j2', movies=movies)

@app.route('/seatingmap')
def seatingmap():
    return render_template('seatingmap.html.j2')

@app.route('/settlement')
def settlement():
    return render_template('settlement.html.j2')

if __name__ == '__main__':
    app.run(debug=True)