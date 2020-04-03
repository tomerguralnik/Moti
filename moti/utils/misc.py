def read_string(message):
    point = 0
    x = yield
    while point < len(message):
        x = yield message[point: point + x]
        point += x