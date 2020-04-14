from flask import Flask, render_template
from flask_login import LoginManager

from data import db_session
from data.kits import Kit
from data.producers import Producer
from data.booklets import Booklet
import push

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

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
    return render_template("filter-prod.html", prod=producer, kits=kits)

def main():
    db_session.global_init("db/CrossStitch.sqlite")
    #push.push_data()
    app.run()


if __name__ == '__main__':
    main()