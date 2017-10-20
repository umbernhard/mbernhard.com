from flask_frozen import Freezer
from warnings import simplefilter as filter_warnings
from benvds import app

import csv

freezer = Freezer(app)
@freezer.register_generator
def product_url_generator():
    # URLs as strings
    yield '/index.html'
    yield '/cv.html'
    yield '/blog.html'
    yield '/blog-index.html'
    with open('content/blogposts.csv') as fin:
        reader = csv.DictReader(fin, delimiter=',', quotechar='~')
        ids = [row['id'] for row in reader]
        for i in ids:
            yield '/blog/'+i+'.html'
            print('/blog/'+i+'.html')


if __name__ == '__main__':
    #filter_warnings('ignore', 'flask_frozen.MissingURLGeneratorWarning')
    freezer.freeze()
