from flask import *
import os
import pandas as pd
import random
from util import *
from flask_sqlalchemy import SQLAlchemy
from model import db
from model import User
from model import board

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
    if 'check' in data :
        check_previous_index = board.query.filter_by(username=session['username']).all()[-1].index
        board.query.filter_by(index = check_previous_index).update(dict(labeling = data['check']))
        db.session.commit()
    
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
    value = board(username = session['username'],
                            filename = word_book_file_name,
                            word1 = random_list[0],
                            word2 = random_list[1],
                            word3 = random_list[2],
                            labeling = None)
    db.session.add(value)
    db.session.commit()
    
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

@app.route('/join', methods = ['GET', 'POST'])
def join() :
    if request.method == 'GET' :
        return render_template('join.html')
    elif request.method == 'POST' :
        id = request.form['username']
        password = request.form['password']
        if not (id and password) :
            flash("Excpetion Error")
            return redirect('join')
        else :
            user = User(username = id, password = password)
            db.session.add(user)
            db.session.commit()
            flash("Complete Join!")
            return redirect('index')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET' :
        return render_template('login.html')
    elif request.method == 'POST' :
        login_id = request.form['username']
        login_password = request.form['password']
        check_login = User.query.filter_by(username = login_id, password = login_password).first()
        if check_login != None :
            session['login'] = 1
            session['username'] = login_id
            flash("Hello {}!".format(login_id))
            return redirect('index')
        else :
            flash("Fail to Login.")
            return redirect('login')



if __name__ == '__main__' :
    database_dir = os.path.abspath(os.path.dirname(__file__))
    db_file = os.path.join(database_dir, 'db.sqlite3')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
    app.config['SQLALCHEMY_COMMIT_ON_TREARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # db = SQLAlchemy()
    db.init_app(app)
    db.app = app
    db.create_all()


    app.run(debug=True)