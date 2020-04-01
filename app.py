from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, AddFeedbackForm, UpdateFeedbackForm

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
def register_form():
    """ Shows and handles form for creating a user """

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
       
        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        return redirect(f"/users/{username}")

    else:
        return render_template("user_new.html", form=form)


@app.route('/login', methods=['POST', 'GET'])
def login_form():
    """ Shows and handles form for logging in a user """

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
    
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{username}")
            
        else:
            form.username.errors = ["Bad name/password"]
            
    return render_template("user_login.html", form=form)


@app.route('/users/<username>')
def show_user_page(username):
    """Show secret page to the logged in users """

    user = User.query.get_or_404(username)
    
    if "username" not in session:
        flash("You must be logged in to view this page")
        return redirect("/login")
    
    else:
        return render_template("user_details.html",
                               user=user)


@app.route('/logout')
def logout_user():
    """Logs user out and redirects to the homepage """
    session.pop("username")
    return redirect("/")


# @app.route('/users/<username>/delete', methods=['POST'])
# def delete_user(username):
#     """ Delete a user """




@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    """ Add feeback if user is logged in """

    form = AddFeedbackForm()
    user = User.query.get_or_404(username)
    
    if "username" not in session:
        flash("You must be logged in to view this page")
        return redirect("/login")
    else:
        if form.validate_on_submit():

            title = form.title.data
            content = form.content.data
        
            feedback = Feedback(title=title, content=content,
                                author=session["username"], username=username)
            
            db.session.add(feedback)
            db.session.commit()

            return redirect(f"/users/{username}")
        
        else:
            
            return render_template("add_feedback.html", 
                                   form=form, 
                                   user=user)

@app.route('/users/feedback/<int:feedback_id>/update')
def edit_feedback(feedback_id):
    """ Edit feedback """

    form = UpdateFeedbackForm()
    
    feedback = Feedback.query.get_or_404(feedback_id)
    author = feedback.author

    if "username" in session and session["username"] == author:
        form = UpdateFeedbackForm(obj=feedback)
        
        if form.validate_on_submit():
            
            title = form.title.data
            content = form.content.data

            feedback.title = title
            feedback.content = content

            db.session.commit()

            return redirect(f"/users/{feedback.username}")

        else:
            return render_template("edit_feedback.html", 
                                   form=form, 
                                   feedback=feedback)
    else:
        flash("You are not the author of this feeback!")
        return redirect(f"/users/{feedback.username}")

