from flask_frozen import Freezer
from warnings import simplefilter as filter_warnings
from benvds import app

from os import listdir
from os.path import isfile, join

freezer = Freezer(app)
@freezer.register_generator
def product_url_generator():
    # URLs as strings
    yield '/index.html'
    yield '/cv.html'

    statics = ['./images/', './css/', './papers/', './keys/']

if __name__ == '__main__':
    #filter_warnings('ignore', 'flask_frozen.MissingURLGeneratorWarning')
    freezer.freeze()
