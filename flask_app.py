from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from apscheduler.schedulers import Scheduler
import atexit

#imports to show project 1
import processNewsOnline as project1


#import pymysql
# sql_user = 'shartrich'
# sql_pwd = 'MySQL123!'
# sql_db = 'shartrich$flask_app'
# sql_host = 'shartrich.mysql.pythonanywhere-services.com'

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="shartrich",
    password="MySQL123!",
    hostname='shartrich.mysql.pythonanywhere-services.com',
    databasename="shartrich$flask_app_db",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
class Comment(db.Model):

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))



# Explicitly kick off the background thread
cron = Scheduler(daemon=True)
cron.start()
@cron.interval_schedule(hours=1)
def job_function():
    #project1.run_main()
    print('Test:', str(datetime.today()))

# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())


    comment = Comment(content=request.form["contents"])
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))

#header_diretions = {'Home': ['', '/aboutMe'], 'Past Experience': ['', '/pastExp'], 'Skills': ['', '/skills']}
index_header = {'Home': ['active', '/aboutMe'], 'Past Experience': ['', '/pastExperience'], 'Skills': ['', '/skills'], 'Side Projects': ['', '/sideProjects']}
experience_header = {'Home': ['', '/aboutMe'], 'Past Experience': ['active', '/pastExperience'], 'Skills': ['', '/skills'], 'Side Projects': ['', '/sideProjects']}
skills_header = {'Home': ['', '/aboutMe'], 'Past Experience': ['', '/pastExperience'], 'Skills': ['active', '/skills'], 'Side Projects': ['', '/sideProjects']}
side_projects_header = {'Home': ['', '/aboutMe'], 'Past Experience': ['', '/pastExperience'], 'Skills': ['', '/skills'], 'Side Projects': ['active', '/sideProjects']}
misc_page_header = {'Home': ['', '/aboutMe'], 'Past Experience': ['', '/pastExperience'], 'Skills': ['', '/skills'], 'Side Projects': ['', '/sideProjects']}

# side_bar_skills = {'Coding': ["#one", "active"], 'Python Libraries': ['#two', ''], 'Software': ['#three', ''], 'Extras': ['#four', '']}
# side_bar_past_exp = {'Data Analytics Specialist': ["#one", "active"], 'Operations Data Analyst': ['#two', ''], 'Operations Analyst': ['#three', ''], 'Past Academic Projects': ['#four', '']}
# side_bar_index = {'About': ["#one", "active"], 'Education': ['#two', ''], 'Skills': ['#three', '']}

side_bar_index = [['About', "#one", "active"], ['Education', '#two', ''], ['Skills', '#three', '']]
side_bar_past_exp = [['Data Analytics Specialist', "#one", "active"], ['Operations Data Analyst', '#two', ''], ['Operations Analyst', '#three', ''], ['Past Academic Projects', '#four', '']]
side_bar_skills = [['Coding', "#one", "active"], ['Python Libraries', '#two', ''], ['Software', '#three', ''], ['Extras', '#four', '']]
side_bar_projects = [['Tracking the News'"#one", "active"]]


@app.route("/hello")
def index_hello():
    return "Hello World!"

@app.route("/aboutMe")
def me_page():
    return render_template('index.html', header_info = index_header, side_bar = side_bar_index)

@app.route("/pastExperience")
def exp_page():
    return render_template('pastExperience.html', header_info = experience_header, side_bar = side_bar_past_exp)

@app.route("/skills")
def skills_page():
    return render_template('skills.html', header_info = skills_header, side_bar = side_bar_skills)

@app.route("/sideProjects")
def projects_page():
    return render_template('sideProjects.html', header_info = side_projects_header, side_bar = side_bar_projects)


@app.route("/project1")
def projects_page():
    return render_template('static/Project Files/test2.html', header_info = misc_page_header, side_bar = side_bar_projects)





