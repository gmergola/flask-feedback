from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    username = db.Column(db.Text, 
                         primary_key=True,
                         nullable=False, 
                         unique=True)

    password = db.Column(db.Text, 
                         nullable=False)
    
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)

    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)

    @classmethod 
    def register(cls, username, password, email, first_name, last_name):
        """ Register user with hased password and return user """

        hashed = bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode('utf8')

        return cls(username=username, password=hashed_utf8, email=email, 
                   first_name=first_name, last_name=last_name)


    @classmethod
    def authenticate(cls, username, password):
        """ Validate user to be logged in """

        user = User.query.filter_by(username=username).one()

        if user and bcrypt.check_password_hash(user.password, password):
            return user

        else:
            return False


class Feedback(db.Model):
    """User feedback."""

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100), 
                      nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)
    
    author = db.Column(db.Text,
                       nullable=False)
    
    username = db.Column(db.ForeignKey("users.username"))

    users = db.relationship("User", backref="feedbacks")