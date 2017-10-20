from flask import Flask, render_template, request, send_file
app = Flask(__name__)

import csv
from os import listdir
from os.path import isfile, join

content = {}

def read_file_keys(obj):
    ret = dict(obj)
    for k in obj:
        if k.startswith("/"):
            with open(obj[k]) as f:
                ret[k[1:]] = f.read()
    return ret


def load_folder(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    for f in files:
        if f.lower().endswith('.html'):
            name = f[:-5]
            with open(join(directory, f)) as fin:
                content[name] = fin.read()
        elif f.lower().endswith('.csv'):
            name = f[:-4]
            with open(join(directory, f)) as fin:
                reader = csv.DictReader(fin, delimiter=',', quotechar='~')
                content[name]  = [read_file_keys(row) for row in reader]
        else:
            name = f
            with open(join(directory, f)) as fin:
                content[name] = fin.read()

load_folder('./content/')


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', main_papers=content['main_papers'], personal=content['personal'])

@app.route('/cv.html')
def cv():
    return render_template('cv.html',
        selected_papers=content['selected_papers'],
        other_papers=content['other_papers'],
        personal_short=content['personal_short'],
        popular_media=content['popular_media'],
        awards=content['awards'],
        education=content['education']
        )

@app.route('/blog')
def blog():
    five_recent = sorted(content['blogposts'], key=lambda x: x['date'], reverse=True)
    if len(five_recent) > 5:
        five_recent = five_recent[0:5]
    return render_template('blog.html', blogposts=five_recent, blog_main=content['blog_main'])

@app.route('/blog/<postid>')
def post(postid):
    items = [x for x in content['blogposts'] if x['id'] == postid]
    return render_template('post.html', item=items[0])

@app.route('/blog-index')
def list():
    recent = sorted(content['blogposts'], key=lambda x: x['date'], reverse=True)
    return render_template('all.html', blogposts=recent, blog_main=content['blog_main'])

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
