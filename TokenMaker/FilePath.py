import os

def get_folder():
    return os.getcwd() + r'\TokenMaker'

def get_frame():
    return get_folder() + r'\src\BaseImage.png'

def get_gradation():
    return get_folder() + r'\src\gradation.png'
