
# A very simple Flask Hello World app for you to get started with...

from json import loads, dumps
from flask import Flask, request, redirect, url_for
from random import choice

app = Flask(__name__)

MYSITE = "."
STORIES = f"{MYSITE}/stories.txt"
INDEX = f"{MYSITE}/index.html"
TELL_STORY = f'{MYSITE}/tell_story.html'

def load_stories():
    with open(STORIES, "r") as f:
        stories = loads(f.read())
        return stories

def save_stories(stories):
    stories_json = dumps(stories, indent=2).replace(',\n ', '\n,').replace('[\n ', '[')
    with open(STORIES, "w") as f:
        f.write(stories_json)

def create_story(story):
    stories = load_stories()
    new_stories = stories + [story]
    save_stories(new_stories)

def page_index(story):
    with open(INDEX, "r") as f:
        page_template = f.read()
        page = page_template.replace("{STORY}", story)
        return page

@app.route('/')
def route_index(concrete_story=None):
    story = concrete_story if not concrete_story is None else api_get_random_story()
    page = page_index(story)
    return page

@app.route('/tell_story')
def route_tell_story():
    with open(TELL_STORY, 'r') as f:
        return f.read()

@app.route('/send_story', methods=['POST'])
def route_send_story():
    try:
        story = request.form['story']
        create_story(story)
        return redirect(url_for('route_index', concrete_story=story))
    except Exception as e:
        return str(e)

@app.route('/api/get_random_story', methods=['GET'])
def api_get_random_story():
    try:
        stories = load_stories()
        if len(stories) == 0:
            return "No stories yet..."
        return choice(stories)
    except Exception as e:
        return str(e)

@app.route('/api/create_story', methods=['POST'])
def api_create_story():
    try:
        new_story = request.data.decode("utf-8")
        create_story(new_story)
        return 'Ok'
    except Exception as e:
        return str(e)

if __name__ == '__main__':  
   app.run(port=4000)
