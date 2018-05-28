from flask import Flask, redirect, render_template, request, url_for, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
import urllib.request
import re

#imports to show project 1
import processNewsOnline as project1






def grab_stock(ticker = 'ZUO'):
    react_ids = {'Price': 14, 'Prev Close': 15, 'Open': 20, 'Volume': 43, 'Avg Volume': 48, 
                'Beta': 61, 'PE Ratio (TTM)': 66, 'EPS (TTM)': 71, '1y Target Est': 90,
                "Day's Range": 34, "52 Week Range": 38, "Market Cap": 56, 'Ex-Dividend Date': 85}

    output = {}
    output['Symbol'] = ticker.upper()

    #return yahoo finance of ticker as data
    url = "https://finance.yahoo.com/quote/%s?p=%s" % (ticker, ticker)
    request = urllib.request.urlopen(url)
    data = request.read().decode()

    # test_taken = []

    for key in react_ids.keys():
        pat = re.compile(r'(?<=data-reactid="' + str(react_ids[key]) + '">)(\d|B|\+| |\-|\-|,|\.)+?(?=<)')
        matches = re.search(pat, data)
        try:
            output[key] = matches.group()
        except AttributeError:
            #output[key] = 'ERROR'
            pass

    return jsonify(output)


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

@app.route("/sqlTest", methods=["GET", "POST"])
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

side_bar_index = [['About', "#one", "active"], ['Education', '#two', ''], ['Side Projects', '#three', '']]
side_bar_past_exp = [['Data Analytics Specialist', "#one", "active"], ['Operations Data Analyst', '#two', ''], ['Operations Analyst', '#three', ''], ['Past Academic Projects', '#four', '']]
side_bar_skills = [['Coding', "#one", "active"], ['Python Libraries', '#two', ''], ['Software', '#three', ''], ['Extras', '#four', '']]
side_bar_projects = [['Tracking the News', "#one", "active"]]



@app.route("/hello")
def index_hello():
    return "Hello World!"

@app.route("/")
def landing_page_about_me():
    path = os.path.dirname(os.path.abspath(__file__))
    bokeh_file = path + '//templates//news bokeh.html'
    project1_last_update_hours = int((datetime.utcnow().timestamp() - os.path.getmtime(bokeh_file)) / 60 / 60)
    return render_template('index.html', header_info = index_header, side_bar = side_bar_index, bokeh_updated_hours_ago = project1_last_update_hours)

@app.route("/aboutMe")
def me_page():
    path = os.path.dirname(os.path.abspath(__file__))
    bokeh_file = path + '//templates//news bokeh.html'
    project1_last_update_hours = int((datetime.utcnow().timestamp() - os.path.getmtime(bokeh_file)) / 60 / 60)
    return render_template('index.html', header_info = index_header, side_bar = side_bar_index, bokeh_updated_hours_ago = project1_last_update_hours)

@app.route("/pastExperience")
def exp_page():
    return render_template('pastExperience.html', header_info = experience_header, side_bar = side_bar_past_exp)

@app.route("/skills")
def skills_page():
    return render_template('skills.html', header_info = skills_header, side_bar = side_bar_skills)

@app.route("/sideProjects")
def projects_page_main():
    return render_template('sideProjects.html', header_info = side_projects_header, side_bar = side_bar_projects)


@app.route("/project1")
def projects_page_1():
    return render_template('news bokeh.html', header_info = misc_page_header, side_bar = side_bar_projects)
    #return render_template('/home/shartrich/mysite/static/Project Files/test2.html', header_info = misc_page_header, side_bar = side_bar_projects)


@app.route("/stock_api")
def test_api():
        ticker =  request.args.get('stock', default = 'ZUO', type = str)
        #request = urllib.request.urlopen("https://finance.yahoo.com/quote/%s?p=%s") % (ticker)
        return grab_stock(ticker)



