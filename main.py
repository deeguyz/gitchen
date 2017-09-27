from flask import Flask
from flask import request
from flask import send_from_directory

import gitchenapi
import json
import imgur
import os

app = Flask(__name__)

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('main', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

@app.route("/upload", methods=["POST"])
def sendUpload():
    if request.method == 'POST':
      f = request.files['file']
      labels = imgur.detect_labels(f.read())
      payload = gitchenapi.getJsonFiles(','.join(labels[:3]))
      template = env.get_template('recipes.html')
      return template.render(results=payload, query=', '.join(labels[:3]))
    # template = env.get_template('index.html')
    # payload = str(request.args['files[]'])
    #print('files[]')


@app.route("/search")
def getIngredients():
    template = env.get_template('recipes.html')
    a = str(request.args['ingredients'])
    payload = gitchenapi.getJsonFiles(a)
    return template.render(results=payload, query=a)

@app.route("/")
def hello():
    template = env.get_template('home.html')
    return template.render()

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

if __name__ == "__main__":
    app.run()
