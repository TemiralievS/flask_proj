from flask import Flask, render_template
from blog.views.users import users_app
from blog.views.articles import articles_app
from blog.models.database import db
from blog.views.auth import login_manager, auth_app
import os
from flask_migrate import Migrate


app = Flask(__name__)
migrate = Migrate(app, db, compare_type=True)

cfg_name = os.environ.get("CONFIG_NAME") or "ProductionConfig"
app.config.from_object(f"blog.configs.{cfg_name}")


@app.route("/")
def index():
    return render_template("index.html")


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('done')


@app.cli.command('create-users')
def create_users():
    from blog.models import User
    admin = User(username='admin', is_staff=True)
    user_1 = User(username='Sergey')

    print('OK! Created users:', admin, user_1)


app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")
app.register_blueprint(auth_app, url_prefix="/auth")

login_manager.init_app(app)

app.config["SECRET_KEY"] = "abcdefg123456"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

