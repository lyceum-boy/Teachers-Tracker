#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Teachers-Tracker.

A flask app with social network bots that informs about teachers
absence and substitute teachers.
"""

import random

from flask import Flask
from flask import redirect
from flask import render_template

from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from data import db_session
from data.groups import Group
from data.students import Student
from data.teachers import Teacher

from forms.login import LoginForm
from forms.user import RegisterForm

__author__ = "Ilya B. Anosov"
__credits__ = ["Maria A. Zamaryokhina", "Sofia P. Kalinina"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Ilya B. Anosov"
__email__ = "anosovilya465@yandex.ru"
__status__ = "Development"

LOGIN = "LOGIN"
PASSWORD = "PASSWORD"

PUBLIC_ID = 204496694
TOKEN = "BOT_TOKEN"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Teacher).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    teachers = db_sess.query(Teacher).all()
    names = {teacher.id: (teacher.surname, teacher.name)
             for teacher in teachers}
    return render_template('index.html', teachers=teachers, names=names,
                           title='Управление системой | Teachers-Tracker')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                'register.html',
                title='Регистрация | Teachers-Tracker',
                form=form,
                message="Пароли не совпадают"
            )
        db_sess = db_session.create_session()
        if db_sess.query(Teacher).filter(
                Teacher.email == form.email.data).first():
            return render_template(
                'register.html',
                title='Регистрация | Teachers-Tracker',
                form=form,
                message="Такой пользователь уже есть"
            )
        teacher = Teacher()
        teacher.surname = form.surname.data
        teacher.name = form.name.data
        teacher.middle_name = form.middle_name.data
        teacher.age = form.age.data
        teacher.address = form.address.data
        teacher.phone = form.phone.data
        teacher.email = form.email.data
        teacher.education = form.education.data
        teacher.set_password(form.password.data)
        db_sess.add(teacher)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html',
                           title='Регистрация | Teachers-Tracker',
                           form=form
                           )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Teacher).filter(
            Teacher.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html',
                           title='Авторизация | Teachers-Tracker',
                           form=form
                           )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def send_message(user_id, message):
    vk_session = vk_api.VkApi(
        token=TOKEN)

    vk = vk_session.get_api()
    vk.messages.send(user_id=user_id,
                     message=message,
                     random_id=random.randint(0, 2 ** 64))


def main():
    db_session.global_init("db/teachers-tracker.db")
    app.run()

    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, PUBLIC_ID)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            vk = vk_session.get_api()
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Спасибо, что написали нам. Мы обязательно ответим",
                             random_id=random.randint(0, 2 ** 64))

    # ...


if __name__ == '__main__':
    main()
