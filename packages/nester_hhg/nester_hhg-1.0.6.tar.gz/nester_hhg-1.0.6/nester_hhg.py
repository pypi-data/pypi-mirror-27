import sys

def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
        for i in the_list:
            if isinstance(i, list):
                print_lol(i, indent, level+1, fh)
            else:
                if indent:
                        for num in range(level):
                                print("\t",end='', file=fh)
                print(i, file=fh)
                
