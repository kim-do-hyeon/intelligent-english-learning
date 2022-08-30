from flask import *
import os

app = Flask(__name__)

@app.route('/')
def main_page() :
    return redirect('index')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/word_list')
def word_list():
    path = "example_data"
    file_list = os.listdir(path)
    return render_template('word_list.html', word_title = file_list)

if __name__ == '__main__' :
    app.run(debug=True)