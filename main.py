from flask import Flask
from data import db_session
from data.users import User
from data.news import News
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    # app.run()

    # user = User()1
    # user.name = "Пользователь 1"
    # user.about = "биография пользователя 1"
    # user.email = "email@email.ru"
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()

    # user = User()
    # user.name = "Пользователь 2"
    # user.about = "биография пользователя 2"
    # user.email = "email2@email.ru"
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()

    # user = User()
    # user.name = "Пользователь 3"
    # user.about = "биография пользователя 3"
    # user.email = "email3@email.ru"
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()

    # вывод первого пользователя
    # user = db_sess.query(User).first()
    # print(user.name)

    # вывод всех пользователей
    # for user in db_sess.query(User).all():
    #     print(user)

    # фильтрация пользователей по заданным параметрам
    # for user in db_sess.query(User).filter(User.id > 1, User.email.notilike("%1%")):
    #     print(user)

    # запятая аналогична И, условие ИЛИ надо указывать явно
    # for user in db_sess.query(User).filter((User.id > 1) | (User.email.notilike("%1%"))):
    #     print(user)

    # Переименование пользователя
    # user = db_sess.query(User).filter(User.id == 1).first()
    # print(user)

    # user.name = "Измененное имя пользователя"
    # user.created_date = datetime.datetime.now()
    # db_sess.commit()

    # удаление записей по фильтру
    # db_sess.query(User).filter(User.id >= 3).delete()
    # db_sess.commit()

    # удаление конкретной записи
    # user = db_sess.query(User).filter(User.id == 2).first()
    # db_sess.delete(user)
    # db_sess.commit()

    # добавление записи пользователю.
    # создать объект класса News и заполнить его поля,
    # в том числе указать явно id записи автора
    # news = News(title="Первая новость", content="Привет блог!",
    #             user_id=1, is_private=False)
    # db_sess.add(news)
    # db_sess.commit()

    # Можем в качестве user указать объект класса User, выбранный
    # (или созданный) заранее
    # user = db_sess.query(User).filter(User.id == 1).first()
    # news = News(title="Вторая новость", content="Уже вторая запись!",
    #             user=user, is_private=False)
    # db_sess.add(news)
    # db_sess.commit()

    # через объект класса User мы можем взаимодействовать с его записями
    # в таблице News почти как со списком
    # user = db_sess.query(User).filter(User.id == 1).first()
    # news = News(title="Личная запись", content="Эта запись личная",
    #             is_private=True)
    # user.news.append(news)
    # db_sess.commit()

    # for news in user.news:
    #     print(news)





if __name__ == '__main__':
    main()


# Операция	Синтаксис ORM
# EQUALS	query(User).filter(User.name == 'Иван')
# NOT EQUAL	query(User).filter(User.name != 'Иван')
# LIKE	query(User).filter(User.name.like('%Иван%'))
# NOT LIKE	query(User).filter(User.name.notlike('%Иван%'))
# IN	query(User).filter(User.name.in_(['Иван', 'Петр', 'Максим']))
# NOT IN	query(User).filter(User.name.notin_(['Иван', 'Петр', 'Максим'])) или
# query(User).filter(~User.name.in_(['Иван', 'Петр', 'Максим']))
# NULL	query(User).filter(User.name == None)
# AND	query(User).filter(User.name == 'Иван', User.id > 3) или query(User).filter(User.name == 'Иван').filter(User.id > 3)
# OR	query(User).filter((User.name == 'Иван') | (User.id > 3)) или
# query(User).filter(or_(User.name == 'Иван', User.id > 3))