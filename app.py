from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///flask-feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route('/')
def hompage():
    """ Redirect to /register """

    return redirect('/register')

@app.route('/register', methods=['POST', 'GET'])
def show_user_form():
    """ Shows and handles form for creating a user """

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
       
        user = User(username=username, password=password, email=email, 
                    first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        return redirect("/secret")

    else:
        return render_template("user_new.html", form=form)

