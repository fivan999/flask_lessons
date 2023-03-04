import os
import json

from typing import Union

from flask import (
    Flask,
    url_for,
    render_template,
    request,
    redirect,
    Response
)

from data import db_session
from data.users import User
from data.jobs import Jobs
from forms import EmergencyAccessForm, RegisterForm


app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main() -> None:
    """инициализация бд, запуск приложения"""
    db_session.global_init('db/mars_mission.sqlite3')
    app.run(port=8080, host='127.0.0.1')


@app.route('/')
@app.route('/index/')
def index() -> str:
    """главная страница"""
    return render_template('base.html')


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


@app.route('/galery/', methods=['GET', 'POST'])
def galery() -> str:
    """страница с каруселью из пейзажев Марса"""
    if request.method == 'POST':
        photo = request.files['photo']
        if photo and photo.filename[photo.filename.find('.') + 1:] in (
            'png',
            'jpg',
            'jpeg'
        ):
            print(f'static/img/galery/{photo.filename}')
            with open(f'static/img/galery/{photo.filename}', 'wb') as file:
                file.write(photo.read())
    styles = url_for('static', filename='css/carousel.css')
    images_url = [
        [
            url_for(
                'static', filename='img/galery/' + image
            ) for image in images
        ] for _, _, images in os.walk('static/img/galery')
    ]
    return render_template('galery.html', styles=styles, images=images_url[0])


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
def emergency_access() -> str:
    """доступ"""
    form = EmergencyAccessForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('emergency_access.html', form=form)


@app.route('/distribution/')
def distribution() -> str:
    """размешение по каютам"""
    param = dict()
    param['people'] = ['Гений Генич', 'Евген', 'Олег', 'Стас Борецкий']
    return render_template('people_distribution.html', **param)


@app.route('/table/<sex>/<int:age>/')
def room(sex: str, age: int) -> Union[str, Response]:
    """каюта"""
    param = dict()
    if sex == 'male':
        if age < 21:
            param['color'] = 'rgb(0, 217, 255)'
            param['image'] = url_for('static', filename='img/little_guy.jpg')
        else:
            param['color'] = 'rgb(25, 0, 255)'
            param['image'] = url_for('static', filename='img/big_guy.jpg')
    else:
        if age < 21:
            param['color'] = 'rgb(251, 255, 0)'
            param['image'] = url_for('static', filename='img/little_guy.jpg')
        else:
            param['color'] = 'rgb(255, 153, 0)'
            param['image'] = url_for('static', filename='img/big_guy.jpg')
    if sex in ('male', 'female'):
        return render_template('room.html', **param)
    else:
        return Response(status=404)


@app.route('/member/')
def member() -> str:
    """участник экспедиции"""
    with open('templates/crew.json', encoding='utf-8') as file:
        crew = json.load(file)
    return render_template('member.html', crew=crew)


@app.route('/jobs/')
def jobs() -> str:
    """работы"""
    session = db_session.create_session()
    jobs = session.query(
        User.surname,
        User.name,
        Jobs.job,
        Jobs.work_size,
        Jobs.collaborators,
        Jobs.is_finished,
        Jobs.id
    ).filter(User.id == Jobs.team_leader)
    return render_template('jobs.html', jobs=jobs)


@app.route('/register/', methods=['GET', 'POST'])
def register() -> str:
    """регистрация"""
    form = RegisterForm()
    if request.method == 'POST':
        if form.password.data != form.password_again.data:
            return render_template(
                'register.html',
                form=form,
                message='Пароли не совпадают'
            )
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                'register.html',
                form=form,
                message='Такой пользователь уже есть'
            )
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login/')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    main()
