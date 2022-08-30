# -*- coding: utf-8 -*-

''' Util'''
import os

def check_file_type(file_name):
    if "csv" in  file_name :
        file_type = "csv"
    elif "xlsx" in file_name :
        file_type = "xlsx"
    else :
        file_type = "Unknown"
    return file_type

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def get_word_file_list() :
    path = "word_data"
    file_list = os.listdir(path)
    word_title = []
    for i in file_list :
        if i.split('.')[1] == 'csv' or i.split('.')[1] == 'xlsx' :
            temp = i.split('.')[0]
            word_title.append(temp)
    return word_title

def word_file_check(id) :
    path = "word_data"
    file_list = os.listdir(path)
    file_name = file_list[id]
    word_file_path = path + "/" + file_name
    print(word_file_path)

    file_type = check_file_type(file_name)
    return file_type, word_file_path, file_name

def find_original_file_name(after_file_name) :
    path = "word_data"
    file_list = os.listdir(path)
    original = ""
    for i in file_list :
        if i.split(".")[0] == after_file_name :
            original = i
            break
    return original