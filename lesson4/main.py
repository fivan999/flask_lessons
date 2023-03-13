import os
import json
import requests

from typing import Union, Callable
from werkzeug.exceptions import NotFound

from flask import (
    Flask,
    url_for,
    render_template,
    request,
    redirect,
    Response,
    make_response,
    jsonify
)
from flask_restful import reqparse, abort, Api, Resource
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from data import db_session, api
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from forms import (
    EmergencyAccessForm,
    RegisterForm,
    LoginForm,
    JobCreateForm,
    DepartmentCreateForm
)
from support import get_place_map, get_place_toponym


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key'
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


def main() -> None:
    """инициализация бд, запуск приложения"""
    db_session.global_init('db/mars_mission.sqlite3')
    app.register_blueprint(api.blueprint)
    app.run(port=8080, host='127.0.0.1')


def handle_api_errors(handler: Callable):
    """декоратор для проверки функции на принадлежность к апи"""
    def custom_handler(error: NotFound) -> Response:
        """не хочу, чтобы все ошибки обрабатывались апи"""
        if request.path.startswith('/api/'):
            return handler(error)
        else:
            return Response(status=error.code)
    return custom_handler


@app.errorhandler(404)
@handle_api_errors
def not_found(error: NotFound) -> Response:
    """ошибка 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
@handle_api_errors
def bad_request(error: NotFound) -> Response:
    """ошибка 400"""
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    db_sess.query(User).get(user_id)
    return user


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


@app.route('/emergency/', methods=['GET', 'POST'])
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
    db_sess = db_session.create_session()
    jobs = db_sess.query(
        User.surname,
        User.name,
        Jobs.job,
        Jobs.work_size,
        Jobs.collaborators,
        Jobs.is_finished,
        Jobs.team_leader,
        Jobs.id,
        Jobs.category_id
    ).filter(User.id == Jobs.team_leader)
    db_sess.close()
    try:
        user_id = current_user.id
    except AttributeError:
        user_id = -1
    return render_template('jobs.html', jobs=jobs, user_id=user_id)


@app.route('/register/', methods=['GET', 'POST'])
def register() -> str:
    """регистрация"""
    form = RegisterForm()
    if form.validate_on_submit():
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
        db_sess.close()
        return redirect('/login/')
    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login() -> str:
    """авторизация"""
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data
        ).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            db_sess.close()
            return redirect('/jobs/')
        return render_template('login.html',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('login.html', form=form)


@app.route('/jobs/add/', methods=['GET', 'POST'])
def add_job() -> str:
    """добавление работы"""
    form = JobCreateForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
            team_leader=form.team_leader.data,
            category_id=form.category.data
        )
        db_sess.add(job)
        db_sess.commit()
        db_sess.close()
        return redirect('/jobs/')
    return render_template('add_job.html', form=form)


@app.route('/jobs/edit/<int:job_id>/', methods=['GET', 'POST'])
@login_required
def edit_job(job_id: int) -> Response:
    """изменение работы"""
    form = JobCreateForm()
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if form.validate_on_submit():
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        job.team_leader = form.team_leader.data
        job.category_id = form.category.data
        db_sess.commit()
        db_sess.close()
        return redirect('/jobs/')
    if job:
        if current_user.id in (1, job.team_leader):
            return render_template('add_job.html', form=form)
        return Response(status=403)
    return Response(status=404)


@app.route('/jobs/delete/<int:job_id>/', methods=['GET', 'POST'])
@login_required
def delete_job(job_id: int) -> Response:
    """удаление работы"""
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id)
    if job.count():
        if current_user.id in (1, job.first().team_leader):
            job.delete()
            db_sess.commit()
            db_sess.close()
            return redirect('/jobs/')
        return Response(status=403)
    return Response(status=404)


@app.route('/departments/')
def departments() -> str:
    """список департаментов"""
    db_sess = db_session.create_session()
    departments = db_sess.query(
        User.surname,
        User.name,
        Department.title,
        Department.chief,
        Department.members,
        Department.email,
        Department.id
    ).filter(User.id == Department.chief)
    db_sess.close()
    try:
        user_id = current_user.id
    except AttributeError:
        user_id = -1
    return render_template(
        'departments.html', departments=departments, user_id=user_id
    )


@app.route('/departments/add/', methods=['GET', 'POST'])
def add_department() -> str:
    """добавление работы"""
    form = DepartmentCreateForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )
        db_sess.add(department)
        db_sess.commit()
        db_sess.close()
        return redirect('/departments/')
    return render_template('add_department.html', form=form)


@app.route('/departments/delete/<int:department_id>/', methods=['GET', 'POST'])
@login_required
def delete_department(department_id: int) -> Response:
    """удаление департамента"""
    db_sess = db_session.create_session()
    department = db_sess.query(
        Department
    ).filter(Department.id == department_id)
    if department.count():
        if current_user.id in (1, department.first().chief):
            department.delete()
            db_sess.commit()
            db_sess.close()
            return redirect('/departments/')
        return Response(status=403)
    return Response(status=404)


@app.route('/departments/edit/<int:department_id>/', methods=['GET', 'POST'])
@login_required
def edit_departments(department_id: int) -> Response:
    """изменение департамента"""
    form = DepartmentCreateForm()
    db_sess = db_session.create_session()
    department = db_sess.query(
        Department
    ).filter(Department.id == department_id).first()
    if form.validate_on_submit():
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data
        db_sess.commit()
        db_sess.close()
        return redirect('/departments/')
    if department:
        if current_user.id in (1, department.chief):
            return render_template('add_department.html', form=form)
        return Response(status=403)
    return Response(status=404)


@app.route('/users_show/<int:user_id>/')
def users_show(user_id: int) -> Union[str, Response]:
    """отображение города марсианина"""
    response = requests.get(
        f'http://127.0.0.1:8080/api/users/{user_id}/'
        ).json()
    if 'error' in response:
        return Response(status=404)
    user_name = f'{response["user"]["surname"]} {response["user"]["name"]}'
    city_from = response['user']['city_from'].lower().strip()
    slugified_name = ''.join(
        [slugify(letter, language_code='ru') for letter in city_from]
    )
    filename = url_for('static', filename=f'img/cities/{slugified_name}.png')
    try:
        place_coords = get_place_toponym(
            city_from
        ).json()['response'][
            'GeoObjectCollection'
        ]['featureMember'][0]['GeoObject']['Point']['pos'].split()
        static_maps_response = get_place_map(place_coords)
        with open(filename.strip('/'), mode='wb') as img:
            img.write(static_maps_response.content)
    except Exception:
        filename = url_for('static', filename='img/image_mars.jpg')
    return render_template(
        'user_show_city.html',
        user_name=user_name,
        image_src=filename,
        city_from=city_from
    )


@app.route('/logout/')
@login_required
def logout() -> Response:
    """выход из системы"""
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    main()
