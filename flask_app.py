from flask import Flask, redirect, render_template, request, url_for, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os


import processNewsOnline as project1
from utils.configs.settings import DB_USERNAME, DB_PASSWORD, DB_DATABASE, DB_HOST, DB_TABLE, \
    PORT, IS_TEST_INSTANCE
from utils.apis.stocks import grab_stock
from utils.configs import website_data


def grab_distance(city1, city2):
    pass


app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=DB_USERNAME,
    password=DB_PASSWORD,
    hostname=DB_DATABASE,
    databasename=DB_HOST,
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


@app.route("/hello")
def index_hello():
    return "Hello World!"

@app.route("/")
def landing_page_about_me():
    path = os.path.dirname(os.path.abspath(__file__))
    bokeh_file = path + '//templates//news bokeh.html'
    project1_last_update_hours = int((datetime.utcnow().timestamp() - os.path.getmtime(bokeh_file)) / 60 / 60)
    return render_template('index.html', header_info=website_data.index_header, side_bar=website_data.side_bar_index, bokeh_updated_hours_ago=project1_last_update_hours)

@app.route("/aboutMe")
def me_page():
    path = os.path.dirname(os.path.abspath(__file__))
    bokeh_file = path + '//templates//news bokeh.html'
    project1_last_update_hours = int((datetime.utcnow().timestamp() - os.path.getmtime(bokeh_file)) / 60 / 60)
    return render_template('index.html', header_info=website_data.index_header, side_bar=website_data.side_bar_index, bokeh_updated_hours_ago=project1_last_update_hours)

@app.route("/pastExperience")
def exp_page():
    return render_template('pastExperience.html', header_info=website_data.experience_header, side_bar=website_data.side_bar_past_exp)

@app.route("/skills")
def skills_page():
    return render_template('skills.html', header_info=website_data.skills_header, side_bar=website_data.side_bar_skills)

# @app.route("/sideProjects")
# def projects_page_main():
#     return render_template('sideProjects.html', header_info = side_projects_header, side_bar = side_bar_projects)


@app.route("/project1")
def projects_page_1():
    return render_template('news bokeh.html', header_info=website_data.misc_page_header, side_bar=website_data.side_bar_projects)
    #return render_template('/home/shartrich/mysite/static/Project Files/test2.html', header_info = misc_page_header, side_bar = side_bar_projects)


@app.route("/stock_api")
def test_api():
        ticker = request.args.get('stock', default='ZUO', type=str)
        return jsonify(grab_stock(ticker))



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=IS_TEST_INSTANCE, port=PORT)