def print_lol(the_list, indent=False, level=0):
        for i in the_list:
            if isinstance(i, list):
                print_lol(i, indent, level+1)
            else:
                if indent:
                    for num in range(level):
                        print("\t",end='')
                print(i)