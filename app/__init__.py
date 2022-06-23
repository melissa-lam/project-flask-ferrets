import os
import json
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

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
    return render_template('index.html', title="Linus Torvalds", url=os.getenv("URL"))

@app.route('/education')
def education():
    education = get_static_json("static/files/education.json")
    return render_template('education.html', education=education)

@app.route('/hobbies')
def hobbies():
    my_hobbies = ["hiking", "skiing", "kayaking", "skating", "snowboarding", "painting", "watching movies", "reading"]
    return render_template('hobbies.html', my_hobbies=my_hobbies)

@app.route('/experiences')
def experiences():
    experiences = get_static_json("static/files/experiences.json")
    return render_template('experiences.html', experiences=experiences)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

# @app.route('/api/timeline_post/<id>', methods=['DELETE'])
# def get_time_line_post(id):
#     TimelinePost.delete_by_id(id)
#     # post_to_delete = TimelinePost.query.get(id)
#     # mydb.session.delete(post_to_delete)
#     # mydb.session.commit()

#     return "deleted"

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
    


