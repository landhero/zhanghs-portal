__author__ = 'Hansheng Zhang'
from flask import Flask
from werkzeug.serving import run_simple
from blueprints import book
app = Flask(__name__)
app.debug = True

@app.route('/')
def root_url():
    return 'This site is to show how stupid I am. <br/> You are not supposed to be here!!'

app.register_blueprint(book.book, url_prefix='/book')

if __name__ == '__main__':
    run_simple('0.0.0.0', 8080, app,
               use_reloader=True, use_debugger=True, use_evalex=True)