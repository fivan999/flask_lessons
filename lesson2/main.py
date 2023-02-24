from flask import (
    Flask,
    url_for,
    render_template,
    request,
    redirect
)

from forms import EmergencyAccessForm


app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index/')
def index() -> str:
    """главная страница"""
    return render_template('base.html', title='Марс')


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


@app.route('/training/<prof>/')
def training(prof: str) -> str:
    """тип тренировки"""
    prof = prof.lower()
    param = dict()
    if 'инженер' in prof or 'строитель' in prof:
        param['train_name'] = 'Научные симуляторы'
        param['train_img'] = url_for(
            'static', filename='img/science_training.jpg'
        )
    else:
        param['train_name'] = 'Другие'
        param['train_img'] = url_for(
            'static', filename='img/other_training.jpg'
        )
    return render_template('training.html', **param)


@app.route('/list_prof/<list_type>/')
def list_prof(list_type: str) -> str:
    """список профессий"""
    param = dict()
    param['list_type'] = list_type
    param['professions'] = [
        'Гений',
        'Умник',
        'Инженер',
        'Повар',
        'Доктор',
        'Строитель'
    ]
    return render_template('professions.html', **param)


@app.route('/answer/')
@app.route('/auto_answer/')
def answer() -> str:
    """информация из анкеты"""
    param = dict()
    param['surname'] = 'Wathy'
    param['name'] = 'Bob'
    param['education'] = 'Среднее общее'
    param['profession'] = 'Марсоходист'
    param['sex'] = 'male'
    param['motivation'] = 'Захотел'
    param['ready'] = 'True'
    param['styles'] = url_for('static', filename='css/answer.css')
    return render_template('auto_answer.html', **param)


@app.route('/login/', methods=['GET', 'POST'])
def emergency_access() -> None:
    """доступ"""
    form = EmergencyAccessForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('emergency_access.html', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
