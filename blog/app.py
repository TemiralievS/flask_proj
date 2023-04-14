from flask import Flask, render_template
from blog.views.users import users_app
from blog.views.authors import authors_app
from blog.views.articles import articles_app
from blog.models.database import db
from blog.views.auth import login_manager, auth_app
import os
from flask_migrate import Migrate
from blog.security import flask_bcrypt


app = Flask(__name__)
migrate = Migrate(app, db, compare_type=True)

app.register_blueprint(authors_app, url_prefix="/authors")

cfg_name = os.environ.get("CONFIG_NAME") or "ProductionConfig"
app.config.from_object(f"blog.configs.{cfg_name}")

flask_bcrypt.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.cli.command('create-admin')
def create_admin():
    from blog.models import User

    admin = User(username="admin", is_staff=True)
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"

    db.session.add(admin)
    db.session.commit()

    print("created admin:", admin)


@app.cli.command('create-users')
def create_users():
    from blog.models import User
    admin = User(username='admin', is_staff=True)
    user_1 = User(username='Sergey')

    print('OK! Created users:', admin, user_1)


@app.cli.command("create-tags")
def create_tags():
    from blog.models import Tag
    for name in [
        "flask",
        "django",
        "python",
        "sqlalchemy",
        "news",
    ]:
        tag = Tag(name=name)
        db.session.add(tag)
    db.session.commit()
    print("created tags")


app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")
app.register_blueprint(auth_app, url_prefix="/auth")

login_manager.init_app(app)

app.config["SECRET_KEY"] = "abcdefg123456"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
