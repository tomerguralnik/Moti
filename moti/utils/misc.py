def read_string(message):
    point = 0
    x = yield
    while point < len(message):
        x = yield message[point: point + x]
        point += x

def camel_from_snake(name):
    return ''.join([word[0].upper() + word[1:] for word in name.split('_')])
