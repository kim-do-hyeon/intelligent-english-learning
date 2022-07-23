# -*- coding: utf-8 -*-

''' Util'''

def check_file_type(file_name):
    if "csv" in  file_name :
        file_type = "csv"
    elif "xlsx" in file_name :
        file_type = "xlsx"
    else :
        file_type = "Unknown"
    return file_type