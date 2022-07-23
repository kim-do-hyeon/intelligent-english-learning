# -*- coding: utf-8 -*-

''' Labeling '''

import os
import random
from datetime import datetime
import pandas as pd

from util import check_file_type

path = "example_data"
file_list = os.listdir(path)

print("[*] Select Data File")
for i in range(len(file_list)) :
    print("[{}] {}".format(i + 1, file_list[i]))

while(1) :
    try :
        file_number = int(input("[>>] Input Number : "))
        if file_number < 1 or file_number > len(file_list) :
            print("Out of range. Please input a valid number")
        else : break
    except :
        print("Unknown input value. Please input a valid number")

file_name = file_list[file_number - 1]
print("[*] Selected File : ", file_name)

file_path = "example_data/" + file_name

file_type = check_file_type(file_name)

if file_type != "Unknown" :
    if file_type == "csv" :
        df = pd.read_csv(file_path, encoding='cp949')
    elif file_type == "xlsx" :
        df = pd.read_excel(file_path)
else :
    print("Wrong Input File (Only .csv and .xlsx File)")

''' Extract A Group of Three Words '''
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

''' Labeling '''
# Labeling text file name => 20220723235501_labeling.txt
labeling_file_name = str(datetime.now().strftime("%Y%m%d%H%M%S")) + "_labeling.txt"
f = open(labeling_file_name, 'w')

print("If you know all words then input 1")
print("Otherwise, input 0")
for i in range(len(random_word_list)) :
    print("[{}] {} / {} / {}".format(str(i + 1), random_word_list[i][0], random_word_list[i][1], random_word_list[i][2]))
    while(1) :
        check = input("[>>] ")
        if check != "0" and check != "1" :
            print("Wrong input. Please input only 0 or 1")
        else : break
    print("[{}] {} / {} / {}".format(str(i + 1), random_word_meaning_list[i][0], random_word_meaning_list[i][1], random_word_meaning_list[i][2]))
    query = random_word_list[i][0] + "," + random_word_list[i][1] + "," + random_word_list[i][2] + "," + check + "\n"
    f.write(query)
f.close()
print("[*] Success")