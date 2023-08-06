"""This is the "pylist_nester.py" module, and it provides one function called
    print_lol() which prints lists that may or may not include nested lists."""

#Make level a default argument with init value 0
#Add indent variable to turn indentation on and off
def print_lol(the_list, indent = False, level = 0):

    """This function takes a positional argument called "the_list", which is any
        Python list (of - possibly - nested lists). Each data item in the provided list
        is (recursively) printed to the screen on its own line.
        The second argument "indent" can have True and False values which in turn switches
        indentation on and off as per the choice of the user.
        A third argument called "level" is used to insert tab-stops when a nested list is encountered."""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            #Adding indentations
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)