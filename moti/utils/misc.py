def read_string(message):
    """
    This is a coroutine that given a string message reads a the message x chars at a time
    when x has to be sent to it
    To initiate: g = read_string(message), next(message)
    Then to g.send(x) reads the next x bytes of message

    :param message: a string
    :type message: str
    """
    point = 0
    p_2 = 0
    x = yield
    while point < len(message):
        p_2 += x
        x = yield message[point: point + x]
        point = p_2

def camel_from_snake(name):
    """
    :param name: a snake case name
    :type name: str

    :return: name in camel case
    :rtype: str
    """
    return ''.join([word[0].upper() + word[1:] for word in name.split('_')])
