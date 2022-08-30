from flask import *
import os
import pandas as pd
from util import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD"

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

@app.route('/word_view/<int:id>')
def word_view(id) :
    path = "example_data"
    file_list = os.listdir(path)
    file_name = file_list[id]
    word_file_path = path + "/" + file_name
    print(word_file_path)

    file_type = check_file_type(file_name)

    if file_type != "Unknown" :
        if file_type == "csv" :
            df = pd.read_csv(word_file_path, encoding='cp949')
        elif file_type == "xlsx" :
            df = pd.read_excel(word_file_path)
        return  render_template('word_view.html', word = df, title = file_name.split(".")[0])

    else :
        flash("Unexpected Error, Please Contact Developer")
        return redirect('/word_list')


if __name__ == '__main__' :
    app.run(debug=True)