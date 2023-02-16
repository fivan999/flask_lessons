from flask import (
    Flask,
    url_for,
    render_template
)


app = Flask(__name__)


@app.route('/')
def home():
    return 'Миссия Колонизация Марса'


@app.route('/index/')
def index():
    return 'И на Марсе будут яблони цвести!'


@app.route('/promotion/')
def promotion():
    return (
        'Человечество вырастает из детства.<br>'
        'Человечеству мала одна планета.<br>'
        'Мы сделаем обитаемыми безжизненные пока планеты.<br>'
        'И начнем с Марса!<br>'
        'Присоединяйся!<br>'
    )


@app.route('/image_mars/')
def image_mars():
    img = url_for('static', filename='img/image_mars.jpg')
    return render_template('image_mars.html', image=img)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
