import sys

import requests
from flask import Flask, render_template, make_response, request, session
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data import db_session
from data.users import User
from data.news import News
import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from forms.news import NewsForm
from forms.user import LoginForm, RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
#     days=365
# )
# session.pop('visits_count', None)
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    return render_template("index.html", news=news)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login_app.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login_app.html', title='Авторизация', form=form)

# регистрация пользователей
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/items',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        news.cost = form.cost.data
        news.contet = form.contet.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление товара',
                           form=form)


@app.route('/items/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_items(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.cost.data = news.cost
            form.contet.data = news.contet
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование товара',
                           form=form
                           )


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_items(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


all_cost = 0


@app.route('/buy/<id>', methods=['GET', 'POST'])
@login_required
def buy_items(id):
    global all_cost
    News.id = id
    all_cost += int(db_session.create_session().query(News)[id - 1].cost)
    id_items = current_user.item.split(", ")
    id_items.append(id)
    current_user.item = ", ".join(id_items)
    return redirect('/')



@app.route('/cart/', methods=['GET', 'POST'])
@login_required
def cart():
    global all_cost
    db_sess = db_session.create_session()
    id_items = current_user.item.split(", ")
    id_items = list(map(int, id_items))
    news = []
    for id_item in id_items:
        news.append(db_sess.query(News).get(News.id == id_item))
    return render_template("items.html", news=news, all_cost=all_cost)


@app.route('/delete_item/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_item(id):
    global all_cost
    News.id = id
    db_sess = db_session.create_session()
    item = db_sess.query(News)[id - 1]
    all_cost -= int(item.cost)
    # del buy[id - 1]
    return redirect('/cart')

@app.route('/map')
def GetMap():
    req = "http://static-maps.yandex.ru/1.x/?ll=87.129191,53.769267&spn=0.002,0.002&l=map&pt=87.129191,53.769267,pm2rdm"
    # тут будет код создающий ссылку на картинку
    return render_template('maps.html', map=req)

def main():
    db_session.global_init("db/blogs.db")
    app.run()

if __name__ == '__main__':
    main()