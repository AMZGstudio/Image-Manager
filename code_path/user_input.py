

def menu():
    print("1. Add Images To database.")
    print("2. Database statistics.")
    print("3. Find Errors in Database.")
    print("4. Delete the database.")
    print("5. Exit.")
    return int(input("Enter your choice: "))

def user_define_file():
    print("Type: 'exit' to leave\n")
    art_style = input("Enter art category (hentai, 3d, irl, etc): ")
    if art_style == 'exit': return None, True

    val = 0
    people_index = {}
    while True:
        val += 1
        person = input("Person " + str(val) + " is female(f) or male(m): ")

        while (person != 'f' and person != 'm' and person != ''):
            person = input("Oops, enter f, or m: ")

        if (person == ''): break
        if (person == 'f'):
            boobs_scale = input("Rate how visible the boobs are? (1-non visible, 2-visible, 3-focus): ")
            pussy_scale = input("Rate how visible the pussy is? (1-non visible, 2-visible, 3-focus): ")
            people_index[val] = {'b': boobs_scale, 'p':pussy_scale, 'g':'F'}

        if (person == 'm'): 
            dick_scale = int(input("Rate how visible the dick is? (1-non visible, 2-visible, 3-focus): "))
            people_index[val] = {'d': dick_scale, 'g':'M'}

    return {'style':art_style, 'people':people_index}, False