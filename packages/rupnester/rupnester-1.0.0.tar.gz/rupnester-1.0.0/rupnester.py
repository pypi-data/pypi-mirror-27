def processList(array_list):
    for item in array_list:
        if isinstance(item, list):
            processList(item)
        else:
            print(item)