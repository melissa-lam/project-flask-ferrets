import os
import json
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
import re

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                         user=os.getenv("MYSQL_USER"),
                         password=os.getenv("MYSQL_PASSWORD"),
                         host=os.getenv("MYSQL_HOST"),
                         port=3306)

print(mydb)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])


@app.route('/')
def index():
    return render_template('index.html', title="Melissa Lam", url=os.getenv("URL"))


@app.route('/education')
def education():
    # education = get_static_json("static/files/education.json")
    return render_template('education.html')


@app.route('/hobbies')
def hobbies():
    hobbies = get_static_json("static/files/hobbies.json")
    return render_template('hobbies.html', hobbies=hobbies)


@app.route('/experiences')
def experiences():
    # experiences = get_static_json("static/files/experiences.json")
    return render_template('experiences.html')


@app.route('/timeline')
def timeline():
    timeline = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return render_template('timeline.html', title="Timeline", timeline=timeline)


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    # Validation for emails
    email_regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    # Form Validation
    if(name is None or name == ""):
        return "Invalid name", 400

    elif(content is None or content == ""):
        return "Invalid content", 400

    elif(email is None or re.fullmatch(email_regex, email) == None):
        return "Invalid email", 400

    timeline_post = TimelinePost.create(
        name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_post():
    id = request.form["id"]
    TimelinePost.delete_by_id(id)

    return "successfully deleted post"


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


def get_static_json(path):
    return json.load(open(get_static_file(path)))


def get_static_file(path):
    root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(root, path)

