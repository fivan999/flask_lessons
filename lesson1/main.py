from flask import (
    Flask,
    url_for,
    render_template
)


app = Flask(__name__)


@app.route('/')
def home() -> str:
    """главная страница"""
    return 'Миссия Колонизация Марса'


@app.route('/index/')
def index() -> str:
    """страница index"""
    return 'И на Марсе будут яблони цвести!'


@app.route('/promotion/')
def promotion() -> str:
    """страница promotion"""
    return (
        'Человечество вырастает из детства.<br>'
        'Человечеству мала одна планета.<br>'
        'Мы сделаем обитаемыми безжизненные пока планеты.<br>'
        'И начнем с Марса!<br>'
        'Присоединяйся!<br>'
    )


@app.route('/image_mars/')
def image_mars() -> str:
    """страница с картинкой марса"""
    img = url_for('static', filename='img/image_mars.jpg')
    return render_template('image_mars.html', image=img)


@app.route('/promotion_image/')
def promotion_image() -> str:
    """страница с рекламой марса"""
    img = url_for('static', filename='img/image_mars.jpg')
    styles = url_for('static', filename='css/styles.css')
    return render_template('promotion_image.html', image=img, styles=styles)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
