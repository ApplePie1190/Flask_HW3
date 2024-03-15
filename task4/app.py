from flask import Flask, render_template, flash, redirect, url_for, request
from models import db, User
from forms import RegistrationForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'mysecretkey'
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует', 'error')
            return redirect(url_for('register'))
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Пользователь с такой электронной почтой уже существует', 'error')
            return redirect(url_for('register'))
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация успешна!', 'success')
    return render_template('index.html', form=form)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')