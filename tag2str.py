def tag2str(i):
    conv = str(i)
    if i < 10:
        string = ['00' + conv]
    elif i < 100:
        string = ['0' + conv]
    else:
        string = conv

    return string
