from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
db.init_app(app)


class Game(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    game: Mapped[str] = mapped_column(unique=True)
    year: Mapped[str]


@app.route('/')
def index():
    games = db.session.execute(db.select(Game).order_by(Game.year)).scalars()
    return render_template('index.html', games=games)


@app.route('/', methods=['POST'])
def add_game():
    game = request.form['game']
    year = request.form['year']

    new_game = Game(game=game, year=year)
    db.session.add(new_game)
    db.session.commit()

    return redirect(url_for('index'))


with app.app_context():
    db.create_all()
