from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from data import db_session
from data.admins import Admin
from data.kits import Kit
from data.producers import Producer
from data.booklets import Booklet
import os
import push

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
filename = ''


@login_manager.user_loader
def load_admin(admin_id):
    session = db_session.create_session()
    return session.query(Admin).get(admin_id)


@app.route("/")
def index():
    session = db_session.create_session()
    kits = session.query(Kit).all()
    return render_template("index.html", kits=kits)


@app.route("/producers")
def prod():
    session = db_session.create_session()
    producers = session.query(Producer).all()
    return render_template("producers.html", producers=producers)


@app.route("/booklets")
def book():
    session = db_session.create_session()
    booklets = session.query(Booklet).all()
    return render_template("booklets.html", booklets=booklets)


@app.route("/filter-prod/<int:id>")
def filter_prod(id):
    session = db_session.create_session()
    producer = session.query(Producer).filter(Producer.id == id).first()
    kits = session.query(Kit).filter(Kit.prod_id == id).all()
    books = session.query(Booklet).filter(Booklet.prod_id == id).all()
    return render_template("filter-prod.html", prod=producer, kits=kits, books=books)


@app.route("/filter-country/<string:country>")
def filter_country(country):
    session = db_session.create_session()
    producers = session.query(Producer).filter(Producer.country == country).all()
    return render_template("filter-country.html", producers=producers, country=country)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        admin = session.query(Admin).filter(Admin.name == form.name.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add-producer', methods=['GET', 'POST'])
@login_required
def add_producer():
    form = ProducerForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        prod = Producer()
        prod.name = form.title.data
        prod.about = form.content.data
        prod.country = form.country.data
        if form.logo.data is None:
            prod.logo = 'empty.png'
        else:
            prod.logo = secure_filename(form.logo.data.filename)
            form.logo.data.save(os.path.join('static/img/logo_prod/', prod.logo))
        session.add(prod)
        session.commit()
        return redirect('/producers')
    return render_template('add-producer.html', title='Добавление производителя',
                           form=form, image='')


@app.route('/add-producer/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_producer(id):
    form = ProducerForm()
    global filename
    if request.method == "GET":
        session = db_session.create_session()
        prod = session.query(Producer).filter(Producer.id == id).first()
        if prod:
            form.title.data = prod.name
            form.content.data = prod.about
            form.country.data = prod.country
            filename = prod.logo
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        prod = session.query(Producer).filter(Producer.id == id).first()
        if prod:
            prod.name = form.title.data
            prod.about = form.content.data
            prod.country = form.country.data
            if form.logo.data is None:
                prod.logo = filename
            else:
                prod.logo = secure_filename(form.logo.data.filename)
                form.logo.data.save(os.path.join('static/img/logo_prod/', prod.logo))
            session.commit()
            return redirect('/producers')
        else:
            abort(404)
    return render_template('add-producer.html', title='Редактирование производителя', form=form, image=filename)


@app.route('/delete-producer/<int:id>', methods=['GET', 'POST'])
@login_required
def producer_delete(id):
    session = db_session.create_session()
    prod = session.query(Producer).filter(Producer.id == id).first()
    if prod:
        session.delete(prod)
        session.commit()
    else:
        abort(404)
    return redirect('/producers')


class ProducerForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = TextAreaField("Описание", validators=[DataRequired()])
    country = StringField('Страна', validators=[DataRequired()])
    logo = FileField('Логотип')
    submit = SubmitField('Применить')


class LoginForm(FlaskForm):
    name = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


def main():
    db_session.global_init("db/CrossStitch.sqlite")
    # push.push_data()
    app.run()


if __name__ == '__main__':
    main()