from flask import *
import os
import pandas as pd
import random
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
    word_title = get_word_file_list()
    return render_template('word_list.html', word_title = word_title)

@app.route('/word_view/<int:id>')
def word_view(id) :
    file_type, word_file_path, file_name = word_file_check(id + 1)

    if file_type != "Unknown" :
        if file_type == "csv" :
            df = pd.read_csv(word_file_path, encoding='cp949')
        elif file_type == "xlsx" :
            df = pd.read_excel(word_file_path)
        return  render_template('word_view.html', word = df, title = file_name.split(".")[0])

    else :
        flash("Unexpected Error, Please Contact Developer")
        return redirect('/word_list')

@app.route('/word_learn')
def word_learn():
    word_title = get_word_file_list()
    return render_template('word_learn.html', word_title = word_title)

@app.route('/word_learn_view/<int:id>')
def word_learn_view(id) :
    file_type, word_file_path, file_name = word_file_check(id + 1)

    if file_type != "Unknown" :
        if file_type == "csv" :
            df = pd.read_csv(word_file_path, encoding='cp949')
        elif file_type == "xlsx" :
            df = pd.read_excel(word_file_path)
    else :
        flash("Unexpected Error, Please Contact Developer")
        return redirect('/word_learn')
    
    # ''' Extract A Group of Three Words '''
    random_word_list = []
    random_word_meaning_list = []
    for i in range(100) : # Only 100 Group. If you want to more group, then modify the number
        temp_list = []
        temp_mean_list = []
        for j in range(3) :
            random_word_index = random.randint(0, len(df['단어']) - 1)
            while random_word_index in temp_list:
                random_word_index = random.randint(0, len(df['단어']) - 1)
            temp_list.append(df['단어'][random_word_index])
            temp_mean_list.append(df['뜻'][random_word_index])
        random_word_list.append(temp_list)
        random_word_meaning_list.append(temp_mean_list)
    print(random_word_list)
    return  render_template('word_learn_view.html',
                                word = random_word_list,
                                mean = random_word_meaning_list,
                                title = file_name.split(".")[0])

@app.route('/word_exam')
def exam_word() :
    word_title = get_word_file_list()
    return render_template('word_exam.html', word_book_list = word_title)

@app.route('/ajax', methods=['POST'])
def ajax() :
    ''' Get Ajax data'''
    data = request.get_json()
    if 'start' not in data :
        ''' Start Exam '''
        data['start'] = 1
    
    ''' Find Original File Name '''
    word_book_file_name = find_original_file_name(data['title'])
    file_type = check_file_type(word_book_file_name)

    ''' Check File type '''
    if file_type != "Unknown" :
        if file_type == "csv" :
            df = pd.read_csv("word_data/" + word_book_file_name, encoding='cp949')
        elif file_type == "xlsx" :
            df = pd.read_excel("word_data/" + word_book_file_name)
    
    ''' Export Random 3 Words'''
    random_list = []
    for i in range(3) :
        random_word_index = random.randint(0, len(df['단어']) - 1)
        while random_word_index in random_list:
            random_word_index = random.randint(0, len(df['단어']) - 1)
        random_list.append(df['단어'][random_word_index])

    if 'index' in data :
        data['word_index'] = int(data['index']) + 1
        data['word_data'] = random_list
        return jsonify(result = data)
    else :
        data['word_data'] = random_list
        try :
            data['word_index'] = data['word_index'] + 1
        except :
            data['word_index'] = 1
        return jsonify(result = data)


if __name__ == '__main__' :
    app.run(debug=True)