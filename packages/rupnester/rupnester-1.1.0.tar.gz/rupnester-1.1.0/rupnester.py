def processList(array_list, name = ''):
    print("Recusrssion.." + name)
    for item in array_list:
        if isinstance(item, list):
            processList(item)
        else:
            print(item)