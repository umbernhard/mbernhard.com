from flask import Flask, render_template, request, send_file
app = Flask(__name__)

import csv
from os import listdir
from os.path import isfile, join

content = {}

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
                content[name]  = [row for row in reader]
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

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
