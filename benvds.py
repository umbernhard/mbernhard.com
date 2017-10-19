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

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', main_papers=content['main_papers'], personal=content['personal'])

@app.route('/cv.html')
@app.route('/cv')
def cv():
    return 'Hello, World!'

@app.route('/css/<filename>')
@app.route('/images/<filename>')
@app.route('/papers/<filename>')
@app.route('/keys/<filename>')
def folders(filename):
    filename = join('./',request.path[1:])
    return send_file(filename)

if __name__ == '__main__':
    load_folder('./content/')
    app.run(debug=True, host='127.0.0.1', port=8080)
