__author__ = 'Hansheng Zhang'

from flask import Blueprint
book = Blueprint('book', __name__)

@book.route('/')
def get_list():
    return "Hansheng has read 0 book(s)!"
