import os
import copy
import imagehash
from difPy import dif
import configparser
from difflib import SequenceMatcher
from PIL import Image
import random

CONFIG_FILE_NAME = 'locations.ini'
image_database = ''
default_path_for_folders = ''
NUM_TO_SHUFFLE = 0
filename = "locations.ini"

def num_to_shuffle_with():
    return NUM_TO_SHUFFLE

def new_shuffle(config):
    config.set("CONFIG SETTINGS", 'file order seed', str(random.random()))

def initalize():
    file = open(CONFIG_FILE_NAME, 'a+')
    file.close()

    config = configparser.ConfigParser()
    config.read(filename)

    try:config.add_section("IMAGE CATEGORIES")
    except configparser.DuplicateSectionError:pass
    try:config.add_section("CATEGORY PATHS")
    except configparser.DuplicateSectionError:pass

    try:
        config.add_section("CONFIG SETTINGS")
    
        config.set("CONFIG SETTINGS", 'database location', './All Images')
        config.set("CONFIG SETTINGS", 'assign files seperator', '&')
        config.set("CONFIG SETTINGS", 'def path for categories', './Categories')
        config.set("CONFIG SETTINGS", 'file order seed', '1')

    except configparser.DuplicateSectionError:pass
    
    try:os.mkdir(config.get("CONFIG SETTINGS", 'database location'))
    except:pass
    try: os.mkdir(config.get("CONFIG SETTINGS", 'def path for categories'))
    except: pass

    global image_database, default_path_for_folders
    image_database = config.get("CONFIG SETTINGS", 'database location')
    default_path_for_folders = config.get("CONFIG SETTINGS", 'def path for categories')
    
    return config

def add_images(search_dups):
    if(search_dups == 'y'):
        print("Searching duplicate files in the database.")
        dif(image_database, similarity="low", delete=True, silent_del=False)
        
    amount_copied = 0
    for filename in os.listdir(image_database):
        path = image_database + '/' + filename
        
        with Image.open(path).convert('RGB') as image:
            new_file_name = str(imagehash.phash(image))+'.jpg'
            new_path = image_database + '/' + new_file_name
            if(filename != new_file_name):
                print("Saving '"+filename+"' as '"+new_file_name+"'")
                image.save(new_path)

                os.remove(path)
                amount_copied += 1

def all_items_in_category(config, category):
    all_items = []
    for selected in config.items(category):
        all_items.append(selected[0])

    return all_items

def create_custom_folder(config):
    name = input("Enter the folder name: ")
    path = input("Enter the path for the folder or type 'def': ")
    not_allowed = input("Enter the categories it cant be in (use '&'): ").split('&')
    allowed = input("Enter the categories it needs to be in: ").split('&')
    print(allowed)
    all_items = []
    if(path == 'def'): path = default_path_for_folders+'/'+name
    else: path+='/'+name
    print(path)
    try:
        os.mkdir(path)
    except OSError as error: 
        pass #print(error)
    
    #os.startfile(path)
    for item in config.items("IMAGE CATEGORIES"):
        #print("item is:", item, "Category is:", category)
        # check if its in not allowed
        allow = True
        for category_not in not_allowed:
            if(category_not in item[1] and category_not != ''): allow=False

        for category in allowed:
            if(category not in item[1] and category != ''): allow=False
            
        if(allow and item[0] not in all_items):
            all_items.append(item[0])
    
    for image in all_items:
        image_path = image_database+'/'+image+'.jpg'
        new_image_path = path+'/'+image+'.jpg'
        
        with Image.open(image_path).convert('RGB') as image:
                image.save(new_image_path)

    
        
    print(all_items)

def copy_files_into_folders(config):
    name_and_loc = {} # the name of the category, and its location (path)
    file_and_loc = {} # the image names with the path they are meant to go to

    for item in config.items("CATEGORY PATHS"):
        name_and_loc[item[0]] = item[1].split('&')

    #print(name_and_loc)
    print("Organizing config file.")

    for item in config.items("IMAGE CATEGORIES"):
        for path in item[1].split('&'):
            try:
                file_and_loc[item[0]] += (name_and_loc[path])
            except:
                try:
                    file_and_loc[item[0]] = copy.deepcopy(name_and_loc[path])
                except:
                    print("ERROR: one of these items are missing/dont work in the config file.", path, item[0])

    amount_of_image_categories = len( all_items_in_category(config, "IMAGE CATEGORIES"))

    amount_of_imgs_already_done = 0
    for selected_image in file_and_loc.keys(): # loop through the images
        amount_of_imgs_already_done += 1
        for selected_path in file_and_loc[selected_image]: # loop through the different file paths of the image
            image_path = image_database + '/' + selected_image + '.jpg'
            new_image_path = selected_path + '/' + selected_image + '.jpg'
            try:
                os.mkdir(selected_path)
                print("Saving " + selected_path)
            except OSError as error: 
                pass #print(error)

            with Image.open(image_path).convert('RGB') as image:
                image.save(new_image_path)
                #print("Saving " + new_image_path)
                print(str(amount_of_imgs_already_done) + '/' + str(amount_of_image_categories) + " - Saving: " + new_image_path)

def give_file_path_to_category(config, category):
    try:
        value = config.get("CATEGORY PATHS", category)
    except configparser.NoOptionError:
        location_path = input("Enter the path of " + category + " or type def for a auto-generated path: ")
        if(location_path == 'def'):
            location_path = default_path_for_folders + '/' + category.title()
        config.set("CATEGORY PATHS", category, location_path)

def assign_files(config):
    easy_sorting = input("Do you want the image to be picked automatically? (y/n):")
    if(easy_sorting == 'y'): # if the person wants easy sorting on
        all_files = os.listdir(image_database)
        random.seed(num_to_shuffle_with())
        all_files = random.sample(all_files, len(all_files))
        #random.shuffle(all_files, num_to_shuffle_with)

        for image_file in all_files: # go through all files in image database
            image_file = image_file.split('.')[0] # seperate the extension, for testing later
            
            if image_file not in all_items_in_category(config, "IMAGE CATEGORIES"): # if the image is not in all the images already in the config file
                with Image.open(image_database + '/' + image_file + '.jpg').convert('RGB') as image: 
                    image.show()# then show image to user
                category = input ("Pick a category for "+image_file+", or multiple with '" + str(config.get("CONFIG SETTINGS", 'assign files seperator'))+"' in between\nif you would like to exit, write 'exit': ")
                if(category == 'exit'): break
                if(category[-1] == str(config.get("CONFIG SETTINGS", 'assign files seperator'))): category = category[:-1]

                new_input = ""
                # go through categories, to check for similarites
                for selected in category.split(str(config.get("CONFIG SETTINGS", 'assign files seperator'))):
                    found_it = False # if it finds a similarity to another word enable this
                    for compare_to in all_items_in_category(config, "CATEGORY PATHS"):
                        if(SequenceMatcher(None, selected, compare_to).ratio() > 0.71):
                            new_input+=compare_to + '&'
                            found_it = True
                    if(found_it == False): # if it couldnt find a similarity, it must be a new category, in which case, add that category
                        new_input+=selected+'&'

                # remove final '&'
                new_input = new_input[:-1]

                # check if the old input (making sure the seperator is the same) is the same as the new input
                if((new_input.replace('&', str(config.get("CONFIG SETTINGS", 'assign files seperator')))) != category):
                    yes_or_no = input("did you mean:"+new_input+"? (y/n):")
                    if(yes_or_no == 'y'): category = new_input
                else:
                    category = new_input
                config.set("IMAGE CATEGORIES", image_file, category)
                
                value = config.get("IMAGE CATEGORIES", image_file).split('&')
                for selected in value:
                    if selected not in all_items_in_category(config, "CATEGORY PATHS"):
                        give_file_path_to_category(config, selected)

    elif(easy_sorting == 'n'):
        image_file = input("Add a image file name or type: ")
        category = input ("Pick a category for that image: ")
        
        try: # get the location of the image, and append another location
            value = config.get("IMAGE CATEGORIES", image_file)
            if(category not in value):
                value += '&' + category
                config.set("IMAGE CATEGORIES", image_file, value)

        except configparser.NoOptionError:
            config.set("IMAGE CATEGORIES", image_file, category)

def print_stats(config):
    amount_of_images_assigned = len(all_items_in_category(config, "IMAGE CATEGORIES"))
    amount_of_image_categories = len( all_items_in_category(config, "CATEGORY PATHS"))
    amount_of_images_total = len(os.listdir(image_database))
    amnt_left_to_assign = amount_of_images_total - amount_of_images_assigned

    print("Stats:\n")
    print("Amount of images in the database: " + str(amount_of_images_total))
    print("Amount of images assigned to categories: " + str(amount_of_images_assigned))
    print("Amount of image categories: " + str(amount_of_image_categories))
    print("Amount of images left to assign: "+str(amnt_left_to_assign))
    print("All the categories are:")
    for category in all_items_in_category(config, "CATEGORY PATHS"):
        print(category)

def verify_integridy_of_config_file(config):
    amount_of_cats_similiar = 0
    amount_of_imgs_not_exists = 0
    category_and_alternative = {}
    for category in all_items_in_category(config, "CATEGORY PATHS"):
        for compare_to in all_items_in_category(config, "CATEGORY PATHS"):
            if(SequenceMatcher(None, category, compare_to).ratio() > 0.71 and category != compare_to and category not in category_and_alternative.values()):
                category_and_alternative[category] = compare_to

    print("\nThe Following Categories Are Similar:")
    for name in category_and_alternative.keys():
        print("'" + name +"' is similar to '" + category_and_alternative[name] +"'")
        amount_of_cats_similiar+=1

    if(amount_of_cats_similiar > 0):
        try_to_fix = input("\nShould we try to fix this? (y/n): ")
        if(try_to_fix == 'y'):
            for category in category_and_alternative.keys():
                which_to_keep = int(input("Press the number you would like to keep:\n1:" + category + ' 2:'+category_and_alternative[category] +'\n: '))
                cat_to_keep = None
                cat_to_del = None

                if(which_to_keep == 1): 
                    cat_to_del = category_and_alternative[category]
                    cat_to_keep = category

                elif(which_to_keep == 2):
                    cat_to_del = category
                    cat_to_keep = category_and_alternative[category]
                
                print(cat_to_del, cat_to_keep)
                config.remove_option("CATEGORY PATHS", cat_to_del)
                for category_group in config.items("IMAGE CATEGORIES"):
                    new_group = category_group[1].split('&')
                    for specific_category in new_group:
                        if(cat_to_del in specific_category):
                            new_group.remove(cat_to_del)
                            new_group.append(cat_to_keep)

                    new_group = '&'.join(new_group)
                    config.set("IMAGE CATEGORIES", category_group[0], new_group)
                    print(new_group)
    else: print("Congratulations, all the categories seem good!")
    for image_name in all_items_in_category(config, "IMAGE CATEGORIES"):
        image_path = image_database + '/' + image_name + '.jpg'
        try:
            img = open(image_path, 'r')
            img.close()
        except:
            amount_of_imgs_not_exists+=1
            print(image_path + ' Does not exists in the database')

    if(amount_of_imgs_not_exists == 0): print("All of the images exist in the database!")  

def find_img_name_in_database():
    path = input("Enter path of image to look for: ")
    with Image.open(path).convert('RGB') as image:
        print("That is called '" + str(imagehash.phash(image))+"'")

def main():
    option = 0
    while option != 9:
        option = int(input("1: Add images to database\n2: Assign Images to categories.\n3: Create a custom folder.\n4: Create folder for every category.\n5: Database statistics.\n6: Check integrity in config file.\n7: Find a filename in the database.\n8: randomize order of files.\n9: Exit.\n\nEnter your choice: "))
        config = initalize()
        global NUM_TO_SHUFFLE
        NUM_TO_SHUFFLE = float(config.get("CONFIG SETTINGS", 'file order seed'))
        #random.seed(num_to_shuffle_with(config))
        if(option == 1):
            answer = input("Search for duplicates in source folder: (y/n): ")
            add_images(answer)
        if(option == 2):
            assign_files(config)
        if(option == 3):
            create_custom_folder(config)
        if(option == 4):
            copy_files_into_folders(config)
        if(option == 5):
            print_stats(config)
        if(option == 6):
            verify_integridy_of_config_file(config)
        if(option == 7):
            find_img_name_in_database()
        if(option == 8):
            new_shuffle(config)

        with open(filename, "w") as config_file:
            config.write(config_file)        
        

if __name__ == '__main__':
    main()