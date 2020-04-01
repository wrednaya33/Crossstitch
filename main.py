from flask import Flask, render_template
from data import db_session
from data.kits import Kit
import push

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route("/")
def index():
    session = db_session.create_session()
    kits = session.query(Kit).all()
    return render_template("index.html", kits=kits)

def main():
    db_session.global_init("db/CrossStitch.sqlite")
    #push.push_data()
    app.run()


if __name__ == '__main__':
    main()