from flask import (
    Flask,
    url_for,
    render_template,
    request
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


@app.route('/astronaut selection/', methods=['POST', 'GET'])
def astronaut_form() -> str:
    """форма астронавту"""
    styles = url_for('static', filename='css/astronaut_form.css')
    return render_template('astronaut_form.html', styles=styles)


@app.route('/choice/<planet_name>/')
def propose_planet(planet_name: str) -> str:
    """страница с предложением планеты"""
    return render_template('planet_proposal.html', planet=planet_name)


@app.route('/results/<nickname>/<int:level>/<float:rating>/')
def person_result(nickname: str, level: int, rating: float) -> str:
    """страница с результатом отбора"""
    return render_template(
        'person_result.html',
        nickname=nickname,
        level=level,
        rating=rating
    )


@app.route('/load_photo/', methods=['POST', 'GET'])
def load_photo() -> str:
    """страница с загрузкой фото"""
    if request.method == 'GET':
        img = url_for('static', filename='img/user_photo.png')
        styles = url_for('static', filename='css/load_photo.css')
        return render_template('load_photo.html', image=img, styles=styles)
    else:
        photo = request.files['photo']
        if photo and photo.filename[photo.filename.find('.') + 1:] in (
            'png',
            'jpg',
            'jpeg'
        ):
            with open('static/img/user_photo.png', 'wb') as file:
                file.write(photo.read())
            return "<h1>Успех!</h1>"
        else:
            return "<h1>Не успех!</h1>"


@app.route('/carousel/')
def mars_landscapes() -> str:
    """страница с каруселью из пейзажев Марса"""
    styles = url_for('static', filename='css/carousel.css')
    images = ['img/image_mars.jpg', 'img/landscape3.jpg', 'img/landscape2.jpg']
    images_url = [url_for('static', filename=image) for image in images]
    return render_template('carousel.html', styles=styles, images=images_url)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
