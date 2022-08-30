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