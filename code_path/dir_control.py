
import os

FILES_FOLDER = 'all_files'
NEW_FILES_FOLDER = 'new_files'
DATA_PATH = 'all_data.pickle'

RUN_FILE_PATH = 'run.bat'
CODE_PATH = 'code_path' # relative to run file

def ran_from_bat():
    # this check changes depending on if the code is run from the bat file, or the master file.
    if CODE_PATH in os.getcwd():
        return False
    return True

def get_relative_to_bat(folder):
    return './'+folder

def get_relative_to_code(folder):
    return '../'+folder

def get_relative(folder):
    if(ran_from_bat()):
        return get_relative_to_bat(folder)
    else:
        return get_relative_to_code(folder)

def get_ext(filename, dot=True):
    dat = filename.split('.')
    if dot:
        return '.'+dat[1]
    else: return dat[1]

