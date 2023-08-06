def pretty_list(l,ident,level):
    for each_list in l:
        if isinstance(each_list,list):
            pretty_list(each_list,ident,level+1)
        else:
            if ident:
                for i in range(level):
                    print('\t',end='')
            print(each_list)

