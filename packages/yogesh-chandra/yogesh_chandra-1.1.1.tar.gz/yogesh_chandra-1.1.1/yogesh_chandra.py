def lol(l):
    for each_list in l:
        if isinstance(each_list,list):
            print('...')
            lol(each_list)
        else:
            print(each_list, end=',')

