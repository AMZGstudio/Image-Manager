import os, shutil, imagehash, cv2
from tabnanny import check
import pickle_control, user_input
from dir_control import *
from PIL import Image

COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    
    "GREY": "\033[90m",
    "CYAN": "\033[36m",
    "ENDC": "\033[0m",
    1: "\033[91m",
    2: "\033[93m",
    3: "\033[92m",
    }

def initalize():
    os.system("")  
    try: os.mkdir(get_relative(FILES_FOLDER))
    except: pass
    try: os.mkdir(get_relative(NEW_FILES_FOLDER))
    except: pass
    with open(get_relative(RUN_FILE_PATH), 'w') as file:
        file.write('python '+get_relative_to_bat(CODE_PATH)+'/master_control.py')

    return pickle_control.load_data(get_relative(DATA_PATH))

def generate_hash(filepath):
    img_to_hash = None
    image = None
    filelower = filepath.lower()

    if('jpg' in filelower or 'jpeg' in filelower or 'png' in filelower or 'gif' in filelower):
        img_to_hash = Image.open(filepath)

    elif('mov' in filepath or 'mp4' in filepath):
        vidcap = cv2.VideoCapture(filepath)
        for i in range(40): 
            success, image = vidcap.read()
        img_to_hash = Image.fromarray(image)

    else: print("The file type is illegal! Error thrown in generate hash function.")

    return str(imagehash.average_hash(img_to_hash))

def add_files(files_obj):
    for file in os.listdir(get_relative(NEW_FILES_FOLDER)):
        new_name = generate_hash(get_relative(NEW_FILES_FOLDER)+'/'+file) + get_ext(file)
    
        # show user the file, so they can define it
        os.startfile(os.getcwd()+'/'+get_relative(NEW_FILES_FOLDER)+'/'+file) 
        print("You are viewing: "+NEW_FILES_FOLDER+'/'+new_name)

        # put that definition into the files obj.
        this_file_obj, exit = user_input.user_define_file()
        if exit: break
        files_obj[new_name] = this_file_obj

        # move file to other place.
        shutil.copy(get_relative(NEW_FILES_FOLDER)+'/'+file, get_relative(FILES_FOLDER)+'/'+new_name)
        os.remove(get_relative(NEW_FILES_FOLDER)+'/'+file)

    return files_obj

def print_statistics(file_data):
    for key in file_data.keys():
        print(COLOR["GREY"] + key, end=COLOR["ENDC"])
        print(COLOR["CYAN"]+ " Style: "+file_data[key]['style'], end=COLOR["ENDC"])
        print("")

        for person in file_data[key]['people'].keys():
            print("    -Person "+str(person)+" Gender: "+COLOR["BLUE"]+file_data[key]['people'][person]['g'],end=COLOR["ENDC"])

            try: print(", Dick: "+COLOR[int(file_data[key]['people'][person]['d'])]+str(file_data[key]['people'][person]['d']), end=COLOR['ENDC'])
            except: pass
            try: print(", Pussy: "+COLOR[int(file_data[key]['people'][person]['p'])]+str(file_data[key]['people'][person]['p']), end=COLOR['ENDC'])
            except: pass
            try: print(", Boobs: "+COLOR[int(file_data[key]['people'][person]['b'])]+str(file_data[key]['people'][person]['b']), end=COLOR['ENDC'])
            except: pass
            print("")
    
    amnt_files_folder = len(os.listdir(get_relative(FILES_FOLDER)))
    amnt_new_files_folder = len(os.listdir(get_relative(NEW_FILES_FOLDER)))
    amnt_in_database = len(file_data)

    print("\n")
    print("Amount of files in files folder    : "+COLOR["GREEN"]+str(amnt_files_folder)+COLOR["ENDC"])
    print("Amount of files in the database    : "+COLOR["GREEN"]+str(amnt_in_database)+COLOR["ENDC"])
    print("Amount of files in new files folder: "+COLOR["RED"]+str(amnt_new_files_folder)+COLOR["ENDC"])
    
    print(COLOR["GREY"], file_data, COLOR["ENDC"])

def check_integrity(file_data):
    files_not_in_database = []
    for file in os.listdir(get_relative(FILES_FOLDER)):
        if file not in file_data.keys():
            print(COLOR["RED"]+file+" Is in the files folder, but does not exist in the database."+COLOR["ENDC"])
            files_not_in_database.append(file)

    print(files_not_in_database)
    if (len(files_not_in_database) != 0):
        val = input("Would you like to move all those files into the new files folder? (y/n): ")
        if val == 'y':
            for file in files_not_in_database:
                # move file to other place.
                shutil.copy(get_relative(FILES_FOLDER)+'/'+file, get_relative(NEW_FILES_FOLDER)+'/'+file)
                os.remove(get_relative(FILES_FOLDER)+'/'+file)

def delete_database(file_data):
    val = input("Are you sure you want to delete the database? (y/n): ")
    if val == 'y':
        pickle_control.delete_data(get_relative(DATA_PATH))
        print("Database deleted")
        return {}
    else:
        print("Cancelled")
        return file_data
        
def main():
    file_data = initalize()

    while True:
        choice = user_input.menu()
        if choice == 1:
            file_data = add_files(file_data)
        if choice == 2:
            print_statistics(file_data)
        if choice == 3:
            check_integrity(file_data)
        if choice == 4:
            file_data = delete_database(file_data)
        if choice == 5:
            break
    
        pickle_control.save_data(file_data, get_relative(DATA_PATH))

if __name__ == '__main__':
    main()